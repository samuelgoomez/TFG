"""Genera un fichero .tex a partir de la plantilla IEEE con la salida del pipeline."""
import re
from pathlib import Path

from abstrack.bib_writer import insertar_citas, limpiar_marcadores_cita, marcar_citas_sin_respaldo, limpiar_markdown

_TEMPLATE = Path(__file__).parent / "templates" / "ieee_template.tex"

_ABSTRACT_RE = re.compile(r'(\\begin\{abstract\})(.*?)(\\end\{abstract\})', re.DOTALL)
_INTRO_SECTION_RE = re.compile(
    r'(\\section\*?\{[^}]*[Ii]ntrodu(?:c(?:c|ç)i[oó]n|ction)[^}]*\}\s*\n)'
    r'(.*?)'
    r'(?=\\section\*?\{|\\appendices|\\end\{document\})',
    re.DOTALL,
)
_BIBLIOGRAPHY_RE = re.compile(r'\\bibliography\{[^}]*\}')


def _escapar_latex(texto: str) -> str:
    """Escapa los caracteres problemáticos en texto plano insertado en LaTeX."""
    return texto.replace("%", r"\%")


def generar_latex(resultado: str, tipo: str, nombre_base: str, bib_text: str | None = None) -> Path:
    """
    Inserta `resultado` en la sección correspondiente de la plantilla IEEE y
    guarda el .tex resultante.  Si se pasa `bib_text`, añade \\cite{} sobre las
    menciones a los papers que sí tienen entrada en la bibliografía.
    Devuelve la ruta del fichero generado.
    """
    template = _TEMPLATE.read_text(encoding="utf-8")
    resultado = limpiar_markdown(resultado)
    if bib_text:
        resultado = insertar_citas(resultado, bib_text)
        resultado = marcar_citas_sin_respaldo(resultado, bib_text)
    else:
        resultado = limpiar_marcadores_cita(resultado)
    contenido = _escapar_latex(resultado.strip())

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
    if bib_text:
        resultado = insertar_citas(resultado, bib_text)
        resultado = marcar_citas_sin_respaldo(resultado, bib_text)
    else:
        resultado = limpiar_marcadores_cita(resultado)
    texto_nuevo = _escapar_latex(resultado.strip())

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

    if bib_text and not _BIBLIOGRAPHY_RE.search(contenido):
        insercion = f"\\bibliographystyle{{IEEEtran}}\n\\bibliography{{{nombre_base}}}\n\n"
        contenido = re.sub(r'\\end\{document\}', lambda m: insercion + "\\end{document}", contenido, count=1)

    origen.write_text(contenido, encoding="utf-8")
    return origen
