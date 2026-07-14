"""Genera un fichero .tex a partir de la plantilla IEEE con la salida del pipeline."""
from pathlib import Path

from abstrack.bib_writer import insertar_citas, limpiar_marcadores_cita, marcar_citas_sin_respaldo

_TEMPLATE = Path(__file__).parent / "templates" / "ieee_template.tex"


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
