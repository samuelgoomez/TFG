"""Genera un fichero .tex a partir de la plantilla IEEE con la salida del pipeline."""
import re
from pathlib import Path

from papercrew.bib_writer import insertar_citas, limpiar_marcadores_cita, marcar_citas_sin_respaldo, limpiar_markdown

_TEMPLATE = Path(__file__).parent / "templates" / "ieee_template.tex"

_ABSTRACT_RE = re.compile(r'(\\begin\{abstract\})(.*?)(\\end\{abstract\})', re.DOTALL)
_INTRO_SECTION_RE = re.compile(
    r'(\\section\*?\{[^}]*[Ii]ntrodu(?:c(?:c|ç)i[oó]n|ction)[^}]*\}\s*\n)'
    r'(.*?)'
    r'(?=\\section\*?\{|\\appendices|\\end\{document\})',
    re.DOTALL,
)
_BIBLIOGRAPHY_RE = re.compile(r'\\bibliography\{[^}]*\}')


_ESCAPES_LATEX = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
}


def _escapar_latex(texto: str) -> str:
    """Escapa los caracteres problemáticos en texto plano insertado en LaTeX
    (&, %, $, #, _). Se aplica sobre el texto en bruto, antes de insertar
    ningún \\cite{}, para no escapar por error algo dentro de un comando
    LaTeX ya construido (p.ej. una clave de bibtex con guion bajo)."""
    for original, escapado in _ESCAPES_LATEX.items():
        texto = texto.replace(original, escapado)
    return texto


def generar_latex(resultado: str, tipo: str, nombre_base: str, bib_text: str | None = None) -> Path:
    """
    Inserta `resultado` en la sección correspondiente de la plantilla IEEE y
    guarda el .tex resultante.  Si se pasa `bib_text`, añade \\cite{} sobre las
    menciones a los papers que sí tienen entrada en la bibliografía.
    Devuelve la ruta del fichero generado.
    """
    template = _TEMPLATE.read_text(encoding="utf-8")
    resultado = limpiar_markdown(resultado)
    resultado = _escapar_latex(resultado.strip())
    if bib_text:
        resultado = insertar_citas(resultado, bib_text)
        resultado = marcar_citas_sin_respaldo(resultado, bib_text)
    # Red de seguridad final: si el LLM ha escrito un marcador "[[CITA: ...]]"
    # mal formado (p.ej. sin año real, con "No especificado") que insertar_citas
    # no ha podido reconocer ni convertir a \cite{}, no debe quedar visible.
    contenido = limpiar_marcadores_cita(resultado)

    pendiente = "% [Pendiente de generacion]"

    if tipo == "abstract":
        carpeta = Path("abstracts/latex")
        latex = template.replace("%%ABSTRACT%%", contenido)
        latex = latex.replace("%%INTRODUCTION%%", pendiente)
    else:
        carpeta = Path("introducciones/latex")
        latex = template.replace("%%INTRODUCTION%%", contenido)
        latex = latex.replace("%%ABSTRACT%%", pendiente)

    if bib_text:
        latex = latex.replace("%%BIBNAME%%", nombre_base)
    else:
        latex = latex.replace(
            "\\bibliographystyle{IEEEtran}\n\\bibliography{%%BIBNAME%%}",
            "% Sin bibliografia: no se proporcionaron citas.",
        )

    carpeta.mkdir(parents=True, exist_ok=True)
    destino = carpeta / f"{nombre_base}.tex"
    destino.write_text(latex, encoding="utf-8")
    return destino


def actualizar_latex_existente(
    ruta_tex_existente: str, resultado: str, tipo: str, nombre_base: str, bib_text: str | None = None
) -> Path:
    """
    Toma un .tex que el autor ya tiene maquetado para su paper y actualiza
    únicamente su sección de abstract o de introducción con la salida del
    MAS, dejando el resto del documento (título, autores, otras secciones)
    tal cual estaba. Si se pasa `bib_text` y el documento no tiene ya un
    \\bibliography{}, se lo añade antes de \\end{document}.
    Sobrescribe el propio fichero indicado en `ruta_tex_existente`, para que
    varias ejecuciones seguidas (hoy la introducción, mañana el abstract)
    vayan completando el mismo documento en vez de crear copias sueltas.
    Devuelve la ruta del .tex actualizado (la misma que se le pasó).
    """
    origen = Path(ruta_tex_existente)
    if not origen.is_file():
        raise FileNotFoundError(f"No se encuentra el fichero .tex indicado: {ruta_tex_existente}")

    contenido = origen.read_text(encoding="utf-8")
    resultado = limpiar_markdown(resultado)
    resultado = _escapar_latex(resultado.strip())
    if bib_text:
        resultado = insertar_citas(resultado, bib_text)
        resultado = marcar_citas_sin_respaldo(resultado, bib_text)
    # Red de seguridad final: si el LLM ha escrito un marcador "[[CITA: ...]]"
    # mal formado (p.ej. sin año real, con "No especificado") que insertar_citas
    # no ha podido reconocer ni convertir a \cite{}, no debe quedar visible.
    texto_nuevo = limpiar_marcadores_cita(resultado)

    if tipo == "abstract":
        if not _ABSTRACT_RE.search(contenido):
            raise ValueError(
                "El .tex indicado no tiene una sección \\begin{abstract}...\\end{abstract} que actualizar."
            )
        contenido = _ABSTRACT_RE.sub(lambda m: f"{m.group(1)}\n{texto_nuevo}\n{m.group(3)}", contenido, count=1)
    else:
        if not _INTRO_SECTION_RE.search(contenido):
            raise ValueError(
                "El .tex indicado no tiene una sección de introducción "
                "(\\section{Introduction} o \\section{Introducción}) que actualizar."
            )
        contenido = _INTRO_SECTION_RE.sub(lambda m: f"{m.group(1)}\n{texto_nuevo}\n\n\n", contenido, count=1)

    if bib_text:
        if _BIBLIOGRAPHY_RE.search(contenido):
            # Ya había un \bibliography{} en el documento, pero puede ser el
            # nombre de un .bib de otra ejecucion anterior (otro paper): lo
            # corregimos para que apunte siempre al .bib que se acaba de
            # generar para este texto.
            contenido = _BIBLIOGRAPHY_RE.sub(lambda m: f"\\bibliography{{{nombre_base}}}", contenido, count=1)
        else:
            insercion = f"\\bibliographystyle{{IEEEtran}}\n\\bibliography{{{nombre_base}}}\n\n"
            contenido = re.sub(r'\\end\{document\}', lambda m: insercion + "\\end{document}", contenido, count=1)

    origen.write_text(contenido, encoding="utf-8")
    return origen


def generar_o_actualizar_latex(
    resultado: str, tipo: str, nombre_base: str, bib_text: str | None = None
) -> Path:
    """
    Igual que generar_latex(), pero antes de partir de la plantilla en
    blanco comprueba si ya existe un .tex con el mismo nombre generado
    para el otro tipo de contenido (el abstract si se está generando la
    introducción, o al revés). Si existe, lo actualiza con
    actualizar_latex_existente() en vez de crear un fichero nuevo, para
    que abstract e introducción del mismo paper acaben en un único
    documento sin tener que indicarlo a mano con --tex-existente.
    """
    carpeta_contraria = Path("introducciones/latex") if tipo == "abstract" else Path("abstracts/latex")
    candidato = carpeta_contraria / f"{nombre_base}.tex"
    if candidato.is_file():
        return actualizar_latex_existente(str(candidato), resultado, tipo, nombre_base, bib_text)
    return generar_latex(resultado, tipo, nombre_base, bib_text)
