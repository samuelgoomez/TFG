"""Genera ficheros .bib a partir de los PDFs de las citas."""
import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

import yaml
from crewai import LLM, Agent, Crew, Process, Task

_CONFIG_DIR = Path(__file__).parent / "config"


def _cargar_config(nombre_fichero: str, clave: str) -> dict:
    with open(_CONFIG_DIR / nombre_fichero, encoding="utf-8") as f:
        return yaml.safe_load(f)[clave]

_DOI_RE = re.compile(r'\b(10\.\d{4,9}/[^\s,;)>\]"\']+)', re.IGNORECASE)
_ARXIV_RE = re.compile(r'arXiv[:\s]+(\d{4}\.\d{4,5})', re.IGNORECASE)
_YEAR_RE = re.compile(r'\b(19|20)\d{2}\b')
_MERGED_WORDS_RE = re.compile(r'^[A-Z][a-z]+[A-Z]')  # detecta palabras fusionadas tipo CamelCase


def _leer_texto_pdf(ruta: Path) -> str:
    try:
        import pdfplumber
        paginas = []
        with pdfplumber.open(ruta) as pdf:
            for page in pdf.pages[:3]:
                t = page.extract_text(x_tolerance=1)
                if t:
                    paginas.append(t)
        return "\n".join(paginas)
    except Exception:
        return ""


def _extraer_doi(texto: str) -> str | None:
    # el margen con el arXiv ID a veces sale invertido letra a letra (texto girado en el PDF)
    m = _DOI_RE.search(texto) or _DOI_RE.search(texto[::-1])
    return m.group(1).rstrip('.,;)>]"\'') if m else None


def _extraer_arxiv_doi(texto: str) -> str | None:
    """Convierte un ID de arXiv en DOI estándar."""
    m = _ARXIV_RE.search(texto) or _ARXIV_RE.search(texto[::-1])
    return f"10.48550/arXiv.{m.group(1)}" if m else None


def _bibtex_por_doi(doi: str) -> str | None:
    try:
        url = f"https://doi.org/{urllib.parse.quote(doi, safe='/')}"
        req = urllib.request.Request(
            url,
            headers={"Accept": "application/x-bibtex", "User-Agent": "Abstrack/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except Exception:
        return None


def _doi_por_titulo(titulo: str) -> str | None:
    """Busca en CrossRef por título. Solo acepta resultados con score alto."""
    try:
        q = urllib.parse.quote(titulo[:120])
        url = f"https://api.crossref.org/works?query.title={q}&rows=1"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Abstrack/1.0 (mailto:abstrack@tfg.local)"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        items = data.get("message", {}).get("items", [])
        if items and items[0].get("score", 0) >= 50:
            return items[0].get("DOI")
    except Exception:
        pass
    return None


def _extraer_titulo(texto: str) -> str | None:
    """Extrae el título del paper descartando líneas con palabras fusionadas o sin espacios."""
    venue_re = re.compile(
        r'(arXiv|ICLR|ICML|NeurIPS|CVPR|ICCV|ECCV|ACL|EMNLP|AAAI|IJCAI|IEEE|ACM'
        r'|conference|workshop|published|submitted|preprint|proceedings)',
        re.IGNORECASE,
    )
    for line in texto.split("\n")[:40]:
        line = line.strip()
        if len(line) < 20 or len(line) > 200:
            continue
        # Descartar líneas con demasiados caracteres sin espacios (palabras fusionadas)
        words = line.split()
        if not words or max(len(w) for w in words) > 30:
            continue
        if venue_re.search(line):
            continue
        return line
    return None


def _clave(nombre: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "", nombre)[:20] or "ref"


def _forzar_clave(bibtex: str, clave: str) -> str:
    """doi.org/CrossRef devuelven claves largas tipo URL (p.ej. https://doi.org/...);
    las sustituimos por la nuestra para poder usarla en \\cite{} en el texto."""
    return re.sub(r"^(@\w+\{)[^,]+,", rf"\1{clave},", bibtex, count=1)


def _bibtex_via_agente(texto: str, clave: str, nombre_fichero: str) -> str | None:
    """Cuando no hay DOI ni resultado fiable en CrossRef, delega en el
    'Agente de Maquetación Bibliográfica' (agents.yaml/tasks.yaml) la lectura
    del texto del paper para extraer título, autores, año y venue.
    Devuelve la entrada BibTeX ya maquetada, o None si el agente falla."""
    try:
        agent_config = _cargar_config("agents.yaml", "agente_bibliografico")
        task_config = _cargar_config("tasks.yaml", "tarea_generar_bibtex")

        agente = Agent(
            config=agent_config,
            llm=LLM(model=os.getenv("MODEL")),
            verbose=False,
        )
        descripcion = task_config["description"].replace(
            "{nombre_fichero}", nombre_fichero
        ).replace("{texto_pdf}", texto[:6000])
        tarea = Task(
            description=descripcion,
            expected_output=task_config["expected_output"],
            agent=agente,
        )
        salida = Crew(agents=[agente], tasks=[tarea], process=Process.sequential).kickoff()
        datos = json.loads(str(salida).strip())
        return (
            f"@article{{{clave},\n"
            f"  title   = {{{datos['title']}}},\n"
            f"  author  = {{{datos['author']}}},\n"
            f"  year    = {{{datos['year']}}},\n"
            f"  journal = {{{datos['venue']}}},\n"
            f"  note    = {{Entrada maquetada por agente -- verificar}}\n"
            f"}}\n"
        )
    except Exception:
        return None


def _bibtex_fallback(texto: str, clave: str, nombre_fichero: str) -> str:
    year_m = _YEAR_RE.search(texto[:3000])
    year = year_m.group() if year_m else "????"
    titulo = _extraer_titulo(texto) or nombre_fichero
    return (
        f"@article{{{clave},\n"
        f"  title   = {{{titulo}}},\n"
        f"  author  = {{[VERIFICAR AUTORES]}},\n"
        f"  year    = {{{year}}},\n"
        f"  journal = {{[VERIFICAR REVISTA O CONFERENCIA]}},\n"
        f"  note    = {{Entrada generada automaticamente -- verificar}}\n"
        f"}}\n"
    )


def generar_bib(citas_path: str, nombre_base: str, tipo: str) -> Path | None:
    """
    Genera un .bib con entradas para cada PDF en citas_path.
    Estrategia: DOI en texto → arXiv ID → CrossRef por título (score >= 50) → fallback.
    Devuelve la ruta del fichero .bib o None si no hay citas.
    """
    directorio = Path(citas_path)
    if not directorio.is_dir():
        return None

    pdfs = sorted(directorio.glob("*.pdf"))
    if not pdfs:
        return None

    entradas = []
    claves_usadas: set[str] = set()

    for pdf in pdfs:
        texto = _leer_texto_pdf(pdf)

        clave_base = _clave(pdf.stem)
        clave = clave_base
        n = 2
        while clave in claves_usadas:
            clave = f"{clave_base}{n}"
            n += 1
        claves_usadas.add(clave)

        bibtex_externo = None

        # 1. DOI explícito en el texto
        doi = _extraer_doi(texto)
        if doi:
            bibtex_externo = _bibtex_por_doi(doi)

        # 2. ID de arXiv en el texto
        if not bibtex_externo:
            doi_arxiv = _extraer_arxiv_doi(texto)
            if doi_arxiv:
                bibtex_externo = _bibtex_por_doi(doi_arxiv)

        # 3. Búsqueda por título en CrossRef (solo si score alto)
        if not bibtex_externo:
            titulo = _extraer_titulo(texto)
            if titulo:
                doi_cr = _doi_por_titulo(titulo)
                if doi_cr:
                    bibtex_externo = _bibtex_por_doi(doi_cr)

        if bibtex_externo:
            bibtex = _forzar_clave(bibtex_externo, clave)
        else:
            # 4. Agente de maquetación bibliográfica (lee el texto y extrae los metadatos)
            bibtex = _bibtex_via_agente(texto, clave, pdf.stem)
            # 5. Fallback determinista si el agente también falla
            if not bibtex:
                bibtex = _bibtex_fallback(texto, clave, pdf.stem)

        entradas.append(bibtex)

    carpeta = Path("abstracts/latex") if tipo == "abstract" else Path("introducciones/latex")
    carpeta.mkdir(parents=True, exist_ok=True)

    destino = carpeta / f"{nombre_base}.bib"
    destino.write_text("\n".join(entradas), encoding="utf-8")
    return destino


_ENTRY_KEY_RE = re.compile(r'^@\w+\{([^,]+),', re.MULTILINE)
_AUTHOR_FIELD_RE = re.compile(r'author\s*=\s*\{([^}]*)\}')
_YEAR_FIELD_RE = re.compile(r'year\s*=\s*\{(\d{4})\}')


def _referencias_citables(bib_text: str) -> list[tuple[str, str, str]]:
    """Devuelve (apellido primer autor, año, clave) por cada entrada del .bib
    que tenga autor real (se descartan las de fallback, con [VERIFICAR AUTORES])."""
    referencias = []
    for entrada in bib_text.split("\n\n"):
        clave_m = _ENTRY_KEY_RE.search(entrada)
        autor_m = _AUTHOR_FIELD_RE.search(entrada)
        year_m = _YEAR_FIELD_RE.search(entrada)
        if not (clave_m and autor_m and year_m):
            continue
        primer_autor = autor_m.group(1).split(" and ")[0]
        if "VERIFICAR" in primer_autor:
            continue
        apellido = primer_autor.split(",")[0].strip()
        if apellido:
            referencias.append((apellido, year_m.group(1), clave_m.group(1)))
    return referencias


def insertar_citas(texto: str, bib_text: str) -> str:
    """Busca menciones tipo 'Bahdanau et al. (2014)' en el texto y les añade
    '\\cite{clave}' detrás, usando las referencias que sí tienen autor/año reales."""
    for apellido, year, clave in _referencias_citables(bib_text):
        patron = re.compile(
            rf'{re.escape(apellido)}(\s+et\s+al\.?)?\s*\({year}\)'
        )
        texto = patron.sub(lambda m: f"{m.group(0)}~\\cite{{{clave}}}", texto)
    return texto
