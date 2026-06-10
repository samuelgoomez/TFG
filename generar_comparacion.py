#!/usr/bin/env python
"""Genera/actualiza abstracts/comparacion_abstracts.xlsx con los pares abstract real / abstract generado.

Uso:
    uv run python generar_comparacion.py
"""
from abstrack.comparacion import generar_excel_comparacion

if __name__ == "__main__":
    excel = generar_excel_comparacion()
    if excel:
        print(f"Excel generado en: {excel}")
    else:
        print("No hay pares abstract real / abstract generado disponibles todavia.")
