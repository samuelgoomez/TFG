#!/usr/bin/env python
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

from abstrack.crew import Abstrack
from abstrack.comparacion import (
    generar_excel_comparacion_abstracts,
    generar_excel_comparacion_introducciones,
)
from abstrack.latex_writer import generar_latex
from abstrack.bib_writer import generar_bib, limpiar_marcadores_cita

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def _guardar_abstract_generado(resultado: str, pdf_path: str | None) -> None:
    """Guarda el abstract generado en abstracts/generados/ con el nombre del paper."""
    carpeta = Path("abstracts/generados")
    carpeta.mkdir(parents=True, exist_ok=True)

    if pdf_path:
        nombre = Path(pdf_path).stem
    else:
        nombre = f"interactivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    destino = carpeta / f"{nombre}_generado.md"
    destino.write_text(str(resultado), encoding="utf-8-sig")
    print(f"\n Abstract guardado en: {destino}")

    latex = generar_latex(str(resultado), "abstract", nombre)
    print(f" LaTeX guardado en: {latex}")

    excel = generar_excel_comparacion_abstracts()
    if excel:
        print(f" Excel de comparación actualizado en: {excel}")


def _guardar_introduccion_generada(resultado: str, pdf_path: str | None, citas_path: str = "") -> None:
    """Guarda la introducción generada en introducciones/generadas/."""
    carpeta = Path("introducciones/generadas")
    carpeta.mkdir(parents=True, exist_ok=True)

    if pdf_path:
        nombre = Path(pdf_path).stem
    else:
        nombre = f"interactivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    resultado = str(resultado)
    destino = carpeta / f"{nombre}_generada.md"
    destino.write_text(limpiar_marcadores_cita(resultado), encoding="utf-8-sig")
    print(f"\n Introducción guardada en: {destino}")

    bib_text = None
    if citas_path:
        bib = generar_bib(citas_path, nombre, "introduccion")
        if bib:
            print(f" Bibliografía guardada en: {bib}")
            bib_text = bib.read_text(encoding="utf-8")

    latex = generar_latex(resultado, "introduccion", nombre, bib_text)
    print(f" LaTeX guardado en: {latex}")

    excel = generar_excel_comparacion_introducciones()
    if excel:
        print(f" Excel de comparación actualizado en: {excel}")


def run():
    """
    Ejecuta el sistema multiagente.

    Modo interactivo, abstract (por defecto):
        abstrack

    Modo interactivo, introducción:
        abstrack --tipo introduccion

    Modo PDF, abstract:
        abstrack --pdf papers/sin_abstract/paper.pdf

    Modo PDF, introducción (requiere los papers citados en papers/sin_introduccion/<paper>_citas/):
        abstrack --tipo introduccion --pdf papers/sin_introduccion/paper.pdf

    Elegir el idioma de redacción (por defecto Español):
        abstrack --pdf papers/sin_abstract/paper.pdf --idioma Inglés
    """
    pdf_path = None
    tipo = "abstract"
    idioma = "Español"
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

    try:
        crew_instance = Abstrack()
        crew_instance.pdf_path = pdf_path
        crew_instance.citas_path = citas_path
        crew_instance.tipo = tipo
        crew_instance.idioma = idioma
        resultado = crew_instance.crew().kickoff(inputs=inputs)
        if tipo == "introduccion":
            _guardar_introduccion_generada(resultado, pdf_path, citas_path)
        else:
            _guardar_abstract_generado(resultado, pdf_path)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year),
        "pdf_path": "",
        "idioma": "Español",
    }
    try:
        Abstrack().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    try:
        Abstrack().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year),
        "pdf_path": "",
        "idioma": "Español",
    }
    try:
        Abstrack().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": "",
        "pdf_path": "",
        "idioma": "Español",
    }

    try:
        result = Abstrack().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
