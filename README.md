# PaperCrew

Sistema multiagente construido con [CrewAI](https://crewai.com) que asiste en la redacción de abstracts e introducciones de artículos científicos. La introducción se genera siguiendo el modelo CARS de Swales y los ejes de Shaw; ambas secciones se integran automáticamente en una plantilla LaTeX oficial (IEEEtran), con la bibliografía generada y verificada mediante una cascada de búsqueda por DOI, arXiv y CrossRef.

El sistema admite dos modos de adquisición de información (entrevista interactiva al autor, o extracción automática desde un PDF) y dos formas de uso (interfaz web o línea de comandos).

## Requisitos previos

- Python >= 3.10, < 3.14
- [uv](https://docs.astral.sh/uv/) instalado globalmente
- Clave de API de OpenAI con crédito disponible

## Instalación

```bash
git clone <url-del-repositorio>
cd TFG
uv sync
```

Crea un fichero `.env` en la raíz del proyecto:

```
MODEL=openai/gpt-4.1-mini
OPENAI_API_KEY=sk-...
```

## Uso

### Interfaz web (recomendada)

```bash
uv run papercrew-web
```

Abre `http://localhost:8501`. Desde ahí se configura el tipo de texto a generar, el modo de entrada, el idioma y los ficheros de entrada, y se descargan los resultados al finalizar.

### Línea de comandos

```bash
# Abstract en modo interactivo
uv run papercrew

# Abstract desde PDF
uv run papercrew --pdf papers/sin_abstract/paper.pdf

# Introducción en modo interactivo
uv run papercrew --tipo introduccion

# Introducción desde PDF (con carpeta de citas)
uv run papercrew --tipo introduccion --pdf papers/sin_introduccion/paper.pdf

# Elegir idioma de salida (por defecto: Español)
uv run papercrew --pdf papers/sin_abstract/paper.pdf --idioma Inglés

# Insertar el resultado en un .tex ya maquetado
uv run papercrew --pdf papers/sin_abstract/paper.pdf --tex-existente ruta/a/mi_paper.tex
```

## Estructura del proyecto

```
src/papercrew/
  agents.yaml / tasks.yaml   Configuración de los agentes y tareas (CrewAI)
  crew.py                    Definición del crew y los pipelines
  bib_writer.py              Cascada de búsqueda bibliográfica y verificación de citas
  latex_writer.py            Generación e inserción en documentos LaTeX
  comparacion.py             Excel de comparación contenido real / generado
  main.py                    Entrada por línea de comandos
  app.py                     Entrada por interfaz web (Streamlit)

papers/       PDFs de entrada (originales, sin abstract, sin introducción, citas)
abstracts/    Abstracts generados, LaTeX resultante y comparación
introducciones/  Introducciones generadas, LaTeX resultante y comparación
```

Para más detalle sobre la arquitectura, el módulo de generación bibliográfica y los agentes, consulta la memoria del TFG.
