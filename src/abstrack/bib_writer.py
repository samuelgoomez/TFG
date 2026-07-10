"""Genera ficheros .bib a partir de los PDFs de las citas."""
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

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
                t = page.extract_text()
                if t:
                    paginas.append(t)
        return "\n".join(paginas)
    except Exception:
        return ""


def _extraer_doi(texto: str) -> str | None:
    m = _DOI_RE.search(texto)
    return m.group(1).rstrip('.,;)>]"\'') if m else None


def _extraer_arxiv_doi(texto: str) -> str | None:
    """Convierte un ID de arXiv en DOI estándar."""
    m = _ARXIV_RE.search(texto)
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

        bibtex = None

        # 1. DOI explícito en el texto
        doi = _extraer_doi(texto)
        if doi:
            bibtex = _bibtex_por_doi(doi)

        # 2. ID de arXiv en el texto
        if not bibtex:
            doi_arxiv = _extraer_arxiv_doi(texto)
            if doi_arxiv:
                bibtex = _bibtex_por_doi(doi_arxiv)

        # 3. Búsqueda por título en CrossRef (solo si score alto)
        if not bibtex:
            titulo = _extraer_titulo(texto)
            if titulo:
                doi_cr = _doi_por_titulo(titulo)
                if doi_cr:
                    bibtex = _bibtex_por_doi(doi_cr)

        # 4. Fallback generado
        if not bibtex:
            bibtex = _bibtex_fallback(texto, clave, pdf.stem)

        entradas.append(bibtex)

    carpeta = Path("abstracts/latex") if tipo == "abstract" else Path("introducciones/latex")
    carpeta.mkdir(parents=True, exist_ok=True)

    destino = carpeta / f"{nombre_base}.bib"
    destino.write_text("\n".join(entradas), encoding="utf-8")
    return destino
