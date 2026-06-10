#!/usr/bin/env python
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

from abstrack.crew import Abstrack
from abstrack.comparacion import generar_excel_comparacion

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
    destino.write_text(str(resultado), encoding="utf-8")
    print(f"\n Abstract guardado en: {destino}")

    excel = generar_excel_comparacion()
    if excel:
        print(f" Excel de comparación actualizado en: {excel}")


def _guardar_introduccion_generada(resultado: str, pdf_path: str | None) -> None:
    """Guarda la introducción generada en introducciones/generadas/."""
    carpeta = Path("introducciones/generadas")
    carpeta.mkdir(parents=True, exist_ok=True)

    if pdf_path:
        nombre = Path(pdf_path).stem
    else:
        nombre = f"interactivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    destino = carpeta / f"{nombre}_generada.md"
    destino.write_text(str(resultado), encoding="utf-8")
    print(f"\n Introducción guardada en: {destino}")


def run():
    """
    Ejecuta el sistema multiagente.

    Modo interactivo, abstract (por defecto):
        abstrack

    Modo interactivo, introducción:
        abstrack --tipo introduccion

    Modo PDF (solo abstract por ahora):
        abstrack --pdf papers/sin_abstract/paper.pdf
    """
    pdf_path = None
    tipo = "abstract"
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

    if tipo == "introduccion" and pdf_path:
        raise SystemExit("Error: el modo PDF para introducción todavía no está implementado.")

    inputs = {
        "topic": "abstract generation",
        "current_year": str(datetime.now().year),
        "pdf_path": pdf_path or "",
    }

    try:
        crew_instance = Abstrack()
        crew_instance.pdf_path = pdf_path
        crew_instance.tipo = tipo
        resultado = crew_instance.crew().kickoff(inputs=inputs)
        if tipo == "introduccion":
            _guardar_introduccion_generada(resultado, pdf_path)
        else:
            _guardar_abstract_generado(resultado, pdf_path)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year),
        "pdf_path": "",
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
    }

    try:
        result = Abstrack().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
