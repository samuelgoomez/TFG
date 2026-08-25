#!/usr/bin/env python
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

from papercrew.crew import PaperCrew
from papercrew.comparacion import (
    generar_excel_comparacion_abstracts,
    generar_excel_comparacion_introducciones,
)
from papercrew.latex_writer import actualizar_latex_existente, generar_o_actualizar_latex
from papercrew.bib_writer import (
    generar_bib,
    limpiar_marcadores_cita,
    marcar_citas_sin_respaldo,
    limpiar_markdown,
    ajustar_limite_palabras,
)
from papercrew.tools.custom_tools import set_informe_path, clear_informe_path

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def _guardar_abstract_generado(resultado: str, pdf_path: str | None, tex_existente: str = "") -> None:
    """Guarda el abstract generado en abstracts/generados/ con el nombre del paper."""
    carpeta = Path("abstracts/generados")
    carpeta.mkdir(parents=True, exist_ok=True)

    if pdf_path:
        nombre = Path(pdf_path).stem
    else:
        nombre = f"interactivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    resultado = limpiar_markdown(str(resultado))

    informe_path = Path("papers/salida/informe_pdf.md" if pdf_path else "papers/salida/informe_entrevista.md")
    informe_texto = informe_path.read_text(encoding="utf-8") if informe_path.exists() else None
    resultado = ajustar_limite_palabras(resultado, informe_texto)

    destino = carpeta / f"{nombre}_generado.md"
    destino.write_text(resultado, encoding="utf-8-sig")
    print(f"\n Abstract guardado en: {destino}")

    if tex_existente:
        latex = actualizar_latex_existente(tex_existente, resultado, "abstract", nombre)
    else:
        latex = generar_o_actualizar_latex(resultado, "abstract", nombre)
    print(f" LaTeX guardado en: {latex}")

    excel = generar_excel_comparacion_abstracts()
    if excel:
        print(f" Excel de comparación actualizado en: {excel}")


def _guardar_introduccion_generada(
    resultado: str, pdf_path: str | None, citas_path: str = "", tex_existente: str = ""
) -> None:
    """Guarda la introducción generada en introducciones/generadas/."""
    carpeta = Path("introducciones/generadas")
    carpeta.mkdir(parents=True, exist_ok=True)

    if pdf_path:
        nombre = Path(pdf_path).stem
    else:
        nombre = f"interactivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    resultado = limpiar_markdown(str(resultado))

    bib_text = None
    if citas_path:
        bib = generar_bib(citas_path, nombre, "introduccion")
        if bib:
            print(f" Bibliografía guardada en: {bib}")
            bib_text = bib.read_text(encoding="utf-8")

    if bib_text:
        resultado = marcar_citas_sin_respaldo(resultado, bib_text)

    destino = carpeta / f"{nombre}_generada.md"
    destino.write_text(limpiar_marcadores_cita(resultado), encoding="utf-8-sig")
    print(f"\n Introducción guardada en: {destino}")

    if tex_existente:
        latex = actualizar_latex_existente(tex_existente, resultado, "introduccion", nombre, bib_text)
    else:
        latex = generar_o_actualizar_latex(resultado, "introduccion", nombre, bib_text)
    print(f" LaTeX guardado en: {latex}")

    excel = generar_excel_comparacion_introducciones()
    if excel:
        print(f" Excel de comparación actualizado en: {excel}")


def run():
    """
    Ejecuta el sistema multiagente.

    Modo interactivo, abstract (por defecto):
        papercrew

    Modo interactivo, introducción:
        papercrew --tipo introduccion

    Modo PDF, abstract:
        papercrew --pdf papers/sin_abstract/paper.pdf

    Modo PDF, introducción (requiere los papers citados en papers/sin_introduccion/<paper>_citas/):
        papercrew --tipo introduccion --pdf papers/sin_introduccion/paper.pdf

    Elegir el idioma de redacción (por defecto Español):
        papercrew --pdf papers/sin_abstract/paper.pdf --idioma Inglés

    Insertar el resultado en un .tex que ya tienes maquetado, en vez de partir de la plantilla en blanco:
        papercrew --pdf papers/sin_abstract/paper.pdf --tex-existente ruta/a/mi_paper.tex
    """
    pdf_path = None
    tipo = "abstract"
    idioma = "Español"
    tex_existente = ""
    args = sys.argv[1:]

    if "--pdf" in args:
        idx = args.index("--pdf")
        if idx + 1 >= len(args):
            raise SystemExit("Error: indica la ruta al PDF tras --pdf")
        pdf_path = args[idx + 1]
        if not os.path.isfile(pdf_path):
            raise SystemExit(f"Error: no se encuentra el fichero '{pdf_path}'")

    if "--tipo" in args:
        idx = args.index("--tipo")
        if idx + 1 >= len(args):
            raise SystemExit("Error: indica el tipo tras --tipo (abstract o introduccion)")
        tipo = args[idx + 1]
        if tipo not in ("abstract", "introduccion"):
            raise SystemExit(f"Error: tipo desconocido '{tipo}'. Usa 'abstract' o 'introduccion'.")

    if "--idioma" in args:
        idx = args.index("--idioma")
        if idx + 1 >= len(args):
            raise SystemExit("Error: indica el idioma tras --idioma")
        idioma = args[idx + 1]

    if "--tex-existente" in args:
        idx = args.index("--tex-existente")
        if idx + 1 >= len(args):
            raise SystemExit("Error: indica la ruta al .tex tras --tex-existente")
        tex_existente = args[idx + 1]
        if not os.path.isfile(tex_existente):
            raise SystemExit(f"Error: no se encuentra el fichero '{tex_existente}'")

    citas_path = ""
    if pdf_path and tipo == "introduccion":
        citas_path = str(Path(pdf_path).with_name(f"{Path(pdf_path).stem}_citas"))

    inputs = {
        "topic": "abstract generation",
        "current_year": str(datetime.now().year),
        "pdf_path": pdf_path or "",
        "citas_path": citas_path,
        "idioma": idioma,
    }

    if not pdf_path:
        ruta_informe = (
            "introducciones/salida/informe_intro.md" if tipo == "introduccion"
            else "papers/salida/informe_entrevista.md"
        )
        set_informe_path(ruta_informe)

    try:
        crew_instance = PaperCrew()
        crew_instance.pdf_path = pdf_path
        crew_instance.citas_path = citas_path
        crew_instance.tipo = tipo
        crew_instance.idioma = idioma
        resultado = crew_instance.crew().kickoff(inputs=inputs)
        if tipo == "introduccion":
            _guardar_introduccion_generada(resultado, pdf_path, citas_path, tex_existente)
        else:
            _guardar_abstract_generado(resultado, pdf_path, tex_existente)
    except Exception as e:
        raise Exception(f"Ha ocurrido un error al ejecutar el crew: {e}")
    finally:
        clear_informe_path()


