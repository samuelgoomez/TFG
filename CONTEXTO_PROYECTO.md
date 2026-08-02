# Contexto del Proyecto — ABSTRACK (TFG Samuel Gómez)

Este fichero resume todo lo implementado en el proyecto para que puedas retomar el trabajo en otro PC pasándoselo a Claude como contexto.

---

## ¿Qué es el proyecto?

Sistema multiagente jerárquico (MAS) construido con **CrewAI** que genera secciones de un artículo científico y las vuelca sobre una plantilla LaTeX real de IEEE, con bibliografía gestionada automáticamente:

- **Abstract**: pipeline genérico de 7 agentes.
- **Introducción**: sigue el modelo **CARS (Swales)** + los **3 ejes de Shaw** (tipo de pregunta de investigación, tipo de contribución, tipo de validación). Pipeline de 10 agentes especializados.

Cada uno tiene dos modos de entrada:

- **Modo interactivo**: el sistema entrevista al autor (por consola o por la web).
- **Modo PDF**: el sistema lee un PDF de un paper (sin abstract / sin introducción) y, en el caso de la introducción, también los PDFs de los papers citados (carpeta `<paper>_citas/`), y extrae la información automáticamente.

Además del texto, el sistema:
- Vuelca el resultado sobre la plantilla oficial de IEEE (`IEEEtran.cls`), adaptada a las Author Guidelines de IEEE Internet of Things Journal.
- Genera la bibliografía real (`.bib`) de los papers citados, con una cascada DOI → arXiv → CrossRef → agente que maqueta la entrada a mano → fallback determinista.
- Enlaza las citas en el texto con `\cite{}` de forma determinista, y marca con `[VERIFICAR]` cualquier mención a un trabajo que no tenga respaldo real en el `.bib` (para que no se cuele una cita inventada sin avisar).
- Puede insertar el resultado en un `.tex` que el autor ya tenga maquetado, en vez de partir siempre de la plantilla en blanco — y si generas primero el abstract y luego la introducción del mismo paper (o al revés), los fusiona automáticamente en un único documento sin que haga falta indicarlo a mano.

---

## Stack tecnológico

| Elemento | Detalle |
|---|---|
| Framework MAS | CrewAI (`Process.hierarchical`, `manager_agent=agente_coordinador`) |
| LLM | Configurable por `.env` (variable `MODEL`). Actualmente `openai/gpt-4.1-mini` (directo contra OpenAI, sin OpenRouter) |
| Gestión de paquetes | `uv` (entorno en `.venv/`) |
| Lectura de PDFs | `pdfplumber` |
| Manipulación de PDFs | `PyMuPDF` (`fitz`) — para eliminar abstracts/introducciones (redacción con rectángulo blanco) al preparar papers de prueba |
| Compilación LaTeX | MiKTeX instalado localmente (`pdflatex`, `bibtex`, `latexmk`) — verificado que compila sin errores con `IEEEtran.cls` |
| Interfaz web | Streamlit (`abstrack-web`) |
| Python | ≥ 3.10, < 3.14 |

---

## Estructura de ficheros del proyecto

```
abstrack/
├── pyproject.toml                        ← dependencias y entrypoints (abstrack, abstrack-web, train, replay, test)
├── CONTEXTO_PROYECTO.md                  ← este fichero
├── escenarios_de_prueba.md               ← respuestas listas para copiar/pegar en modo interactivo
├── .env                                  ← MODEL, OPENAI_API_KEY (gitignored)
│
├── src/abstrack/
│   ├── crew.py                           ← definición del crew (abstract + introducción, interactivo + PDF)
│   ├── main.py                           ← entrypoint CLI (--pdf, --tipo, --idioma, --tex-existente)
│   ├── app.py                            ← interfaz web Streamlit
│   ├── latex_writer.py                   ← generar_latex / actualizar_latex_existente / generar_o_actualizar_latex
│   ├── bib_writer.py                     ← generar_bib, insertar_citas, marcar_citas_sin_respaldo, ajustar_limite_palabras...
│   ├── comparacion.py                    ← genera los Excel de comparación
│   ├── config/
│   │   ├── agents.yaml                   ← configuración de agentes (17 en total)
│   │   └── tasks.yaml                    ← configuración de tareas
│   ├── templates/
│   │   └── ieee_template.tex             ← plantilla oficial IEEEtran (bare_jrnl.tex), con marcadores %%ABSTRACT%%/%%INTRODUCTION%%/%%BIBNAME%%
│   └── tools/
│       └── custom_tools.py               ← preguntar_al_autor, leer_pdf, leer_pdfs_carpeta, leer_informe_actual
│
├── papers/
│   ├── original/                         ← PDFs intactos
│   ├── sin_abstract/                     ← PDFs con abstract eliminado → entrada modo PDF (abstract)
│   ├── sin_introduccion/                 ← PDFs con introducción eliminada → entrada modo PDF (introducción)
│   │   └── <paper>_citas/                ← PDFs de los papers realmente citados por ese paper
│   └── salida/informe_entrevista.md / informe_pdf.md  ← informe de la entrevista/extracción (abstract)
│
├── abstracts/
│   ├── originales/, generados/<paper>_generado.md, latex/<paper>.tex(+.bib), comparacion_abstracts.xlsx
│
├── introducciones/
│   ├── originales/, generadas/<paper>_generada.md, latex/<paper>.tex(+.bib)
│   ├── salida/informe_intro.md / informe_pdf_intro.md
│   └── comparacion_introducciones.xlsx
│
└── evidencias/                           ← PDF real compilado con MiKTeX, prueba de que el .tex generado compila y cita bien
```

---

## Pipeline de Abstract (7 agentes) — completo y probado

| # | Agente | Rol | Modo |
|---|---|---|---|
| 0 | `agente_coordinador` | Manager jerárquico | Ambos |
| 1a | `agente_de_adquisicion_de_informacion` | Entrevista al autor | Interactivo |
| 1b | `agente_de_adquisicion_pdf` | Lee el PDF y extrae 6 puntos clave | PDF |
| 2 | `agente_de_validacion_de_completitud` | Valida (loop hasta VALIDADO) | Ambos |
| 3 | `agente_de_estructuracion_de_contenido` | Esqueleto conceptual | Ambos |
| 4 | `agente_redactor` | Redacta el abstract | Ambos |
| 5 | `agente_de_revision_de_estilo` | Pule forma | Ambos |
| 6 | `agente_de_control_de_calidad` | Verificación final | Ambos |

Flujo: Adquisición → Validación (loop) → Estructuración → Redacción → Revisión → Control de calidad → `abstracts/generados/<paper>_generado.md` + `.tex`.

---

## Pipeline de Introducción CARS + Shaw (10 agentes) — completo y probado

| # | Agente | Rol | Modo |
|---|---|---|---|
| 0 | `agente_coordinador_intro` | Manager jerárquico | Ambos |
| 1a | `agente_de_adquisicion_de_informacion` | Entrevista al autor (7 puntos) | Interactivo |
| 1b | `agente_de_adquisicion_pdf` | Lee `leer_pdf` (paper) + `leer_pdfs_carpeta` (citas) | PDF |
| 2 | `agente_de_validacion_de_completitud` | Valida los 7 puntos CARS+Shaw (loop hasta VALIDADO) | Ambos |
| 3 | `agente_especialista_territorio` | Bloque "Territorio" | Ambos |
| 4 | `agente_especialista_hueco` | Bloque "Hueco" (solo cita papers de la carpeta de citas; marca `[VERIFICAR]` si no hay evidencia) | Ambos |
| 5 | `agente_especialista_idea` | Bloque "Idea/Enfoque" | Ambos |
| 6 | `agente_especialista_contribuciones` | Bloque "Contribuciones" (lista en viñetas) | Ambos |
| 7 | `agente_especialista_evaluacion` | Bloque "Evaluación" | Ambos |
| 8 | `agente_especialista_estructura_documento` | Bloque "Estructura del Documento" | Ambos |
| 9 | `agente_editor_intro` | Fusiona los 6 bloques, comprueba ejes de Shaw | Ambos |
| 10 | `agente_de_control_de_calidad` | Verificación global final | Ambos |

---

## Agentes de soporte (fuera del pipeline principal, usados por bib_writer.py)

- `agente_bibliografico` — maqueta a mano una entrada BibTeX leyendo el PDF, cuando falla la búsqueda automática por DOI/arXiv/CrossRef.
- `agente_recortador` — reduce un abstract al límite de palabras (el que dio el autor, o 250 por defecto de IEEE IoT-J) sin perder cifras ni la frase final obligatoria, cuando el control de calidad no lo ha ajustado bien.

CrewAI exige que todo agente referenciado en `tasks.yaml` tenga su método correspondiente en `crew.py` (decorado con `@agent`), aunque no forme parte de la lista de tareas del crew principal — si no, `Abstrack()` falla al instanciarse con un `KeyError`.

---

## Escritura en plantilla LaTeX y gestión bibliográfica

- **`generar_latex()`**: inserta el resultado en la plantilla en blanco (`templates/ieee_template.tex`).
- **`actualizar_latex_existente()`**: en vez de partir de la plantilla en blanco, actualiza solo la sección de abstract o introducción de un `.tex` que el autor ya tenga maquetado (sección `\begin{abstract}` o `\section{Introduction}`), dejando el resto del documento intacto. Corrige también el nombre del `.bib` en `\bibliography{}` si apuntaba al de otra ejecución anterior. Se activa con `--tex-existente <ruta>` en CLI o subiendo el archivo en la web.
- **`generar_o_actualizar_latex()`**: antes de generar desde la plantilla en blanco, comprueba si ya existe un `.tex` con el mismo nombre generado para el otro tipo de contenido (abstract vs introducción) — si existe, lo actualiza en vez de crear un fichero nuevo, así que generar primero el abstract y luego la introducción del mismo paper (o al revés) los deja fusionados en un único documento automáticamente, sin usar `--tex-existente` a mano. Es el comportamiento por defecto.
- **`generar_bib()`** (en `bib_writer.py`): para cada PDF de la carpeta de citas, cascada DOI en el texto → ID de arXiv → búsqueda por título en CrossRef (score alto) → Agente de Maquetación Bibliográfica → fallback determinista con los campos marcados `[VERIFICAR]`.
- **`insertar_citas()`**: convierte los marcadores `[[CITA: Apellido, Año]]` que insertan los agentes de redacción en `\cite{clave}` reales, cruzando contra el `.bib`.
- **`marcar_citas_sin_respaldo()`**: red de seguridad final — cualquier mención "Apellido (Año)" en el texto final que no tenga una entrada real en el `.bib` se marca `[VERIFICAR]`, para que ninguna cita inventada por el LLM pase desapercibida.
- **Escapado de LaTeX**: se escapan `&`, `%`, `$`, `#`, `_` en el texto en bruto, antes de insertar ninguna cita (para no escapar por error el guion bajo de una clave de bibtex como `Zeng_2017`).

**Limitación conocida, aceptada**: cuando un paper se publicó primero en arXiv y después formalmente en una conferencia/revista con un año distinto, el texto puede citar el año de la publicación oficial mientras el `.bib` indexa el año del preprint — se marca `[VERIFICAR]` aunque la cita sea correcta (falso positivo). Es preferible a que se cuele una cita falsa sin avisar; se decidió no añadir tolerancia de año porque no aporta lo suficiente para el riesgo/complejidad que añade.

---

## Bucle de validación interactivo (adquisición ↔ validación)

En modo interactivo, si el Agente de Validación de Completitud detecta que faltan datos, el coordinador delega de vuelta en el agente de adquisición para completar la entrevista. Este bucle tuvo un fallo real: el coordinador, al delegar, no siempre retransmitía bien "qué es lo que falta" ni "qué se guardó ya", así que el agente de adquisición a veces repreguntaba cosas ya respondidas.

Solución aplicada:
- **`preguntar_al_autor` registra automáticamente**, como efecto de código (no depende de que ningún agente lo decida), cada pregunta y respuesta en el informe de la sesión (`papers/salida/informe_entrevista.md` o `introducciones/salida/informe_intro.md`).
- Nueva herramienta **`leer_informe_actual`**, disponible para el agente de adquisición: si le devuelven el control tras una validación fallida, lee ese informe para comprobar por sí mismo qué está cubierto antes de preguntar nada más (está en su propio `goal`, no solo en el prompt de la tarea de validación, para que no dependa de que el coordinador se lo repita bien). **Importante**: solo debe leer el informe al *retomar* tras un rechazo, nunca en el arranque de la entrevista (si lo hace en el arranque, con el informe vacío, el agente se descoloca y no llega a hacer la entrevista real).
- El criterio de validación de Resultados se endureció: exige al menos un dato concreto y medible, no basta una valoración genérica ("funcionó bien") sin cifras detrás.

Confirmado funcionando en ambos pipelines (abstract e introducción) con pruebas reales.

---

## Herramientas custom (`src/abstrack/tools/custom_tools.py`)

```python
@tool("preguntar_al_autor")
def ask_human_tool(pregunta: str) -> str: ...
# input() por consola, o cola de Streamlit en modo web.
# Registra automáticamente cada P/R en el informe de la sesión (set_informe_path()).

@tool("leer_pdf")
def read_pdf_tool(ruta_pdf: str) -> str: ...    # pdfplumber, un solo PDF

@tool("leer_pdfs_carpeta")
def read_pdfs_folder_tool(ruta_carpeta: str) -> str: ...  # concatena todos los PDFs de una carpeta

@tool("leer_informe_actual")
def read_informe_tool(ruta_informe: str) -> str: ...  # lee el informe ya guardado de esta sesión
```

---

## Cómo se lanza

Desde la raíz del proyecto:

```bash
# Abstract — interactivo
uv run abstrack

# Abstract — modo PDF
uv run abstrack --pdf papers/sin_abstract/attention_is_all_you_need.pdf

# Introducción — interactivo
uv run abstrack --tipo introduccion

# Introducción — modo PDF (requiere papers/sin_introduccion/<paper>_citas/)
uv run abstrack --tipo introduccion --pdf papers/sin_introduccion/attention_is_all_you_need.pdf

# Elegir idioma (por defecto Español)
uv run abstrack --pdf papers/sin_abstract/paper.pdf --idioma Inglés

# Insertar en un .tex que ya tienes maquetado, en vez de la plantilla en blanco
uv run abstrack --pdf papers/sin_abstract/paper.pdf --tex-existente ruta/a/mi_paper.tex

# Interfaz web
uv run abstrack-web
```

---

## Estado actual

Ambos pipelines (abstract e introducción), en sus cuatro combinaciones (interactivo/PDF × abstract/introducción), están implementados, probados y funcionando de forma fiable con `gpt-4.1-mini`. La escritura sobre la plantilla IEEE y la generación de bibliografía están verificadas con una compilación real (MiKTeX, `evidencias/attention_is_all_you_need.pdf`), con las citas numeradas correctamente en el texto y en la sección de referencias.

Papers de prueba disponibles: *Attention Is All You Need* (inglés), *Aplicación de RNA para Parkinson* (español), *SimulateIoT* (inglés, IEEE Access — paper largo con citación numérica en el original, usado para probar los límites de contexto y las citas).

## Pendiente

1. **COMFIT y CupCarbon** (dos de los trabajos relacionados que cita SimulateIoT) están detrás de muro de pago (Elsevier y EAI/EUDL respectivamente) y no se han podido conseguir para completar la bibliografía de ese caso de prueba.
2. Ningún cambio de arquitectura pendiente ni bug conocido sin resolver — el resto de limitaciones conocidas (falso positivo de año en citas, precisión no garantizada al 100% del Agente Recortador) se han evaluado y se han dejado así a propósito, no por falta de tiempo.
