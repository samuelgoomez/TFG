#!/usr/bin/env python
"""Genera/actualiza los Excel con los pares real / generado de abstracts e introducciones.

Uso:
    uv run python generar_comparacion.py
"""
from abstrack.comparacion import (
    generar_excel_comparacion_abstracts,
    generar_excel_comparacion_introducciones,
)

if __name__ == "__main__":
    excel_abstracts = generar_excel_comparacion_abstracts()
    if excel_abstracts:
        print(f"Excel de abstracts generado en: {excel_abstracts}")
    else:
        print("No hay pares abstract real / abstract generado disponibles todavia.")

    excel_intro = generar_excel_comparacion_introducciones()
    if excel_intro:
        print(f"Excel de introducciones generado en: {excel_intro}")
    else:
        print("No hay pares introduccion real / introduccion generada disponibles todavia.")
