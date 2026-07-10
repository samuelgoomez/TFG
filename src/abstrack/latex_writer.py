"""Genera un fichero .tex a partir de la plantilla IEEE con la salida del pipeline."""
from pathlib import Path

_TEMPLATE = Path(__file__).parent / "templates" / "ieee_template.tex"


def _escapar_latex(texto: str) -> str:
    """Escapa los caracteres problemáticos en texto plano insertado en LaTeX."""
    return texto.replace("%", r"\%")


def generar_latex(resultado: str, tipo: str, nombre_base: str) -> Path:
    """
    Inserta `resultado` en la sección correspondiente de la plantilla IEEE y
    guarda el .tex resultante.  Devuelve la ruta del fichero generado.
    """
    template = _TEMPLATE.read_text(encoding="utf-8")
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

    latex = latex.replace("%%BIBNAME%%", nombre_base)

    carpeta.mkdir(parents=True, exist_ok=True)
    destino = carpeta / f"{nombre_base}.tex"
    destino.write_text(latex, encoding="utf-8")
    return destino
