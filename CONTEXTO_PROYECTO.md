# Contexto del Proyecto — ABSTRACK (TFG Samuel Gómez)

Este fichero resume todo lo implementado en el proyecto para que puedas retomar el trabajo en otro PC pasándoselo a Claude como contexto.

---

## ¿Qué es el proyecto?

Sistema multiagente jerárquico (MAS) construido con **CrewAI** que genera secciones de un artículo científico:

- **Apartados 1-2 (abstract)**: genera el **abstract** de un paper. Pipeline genérico de 7 agentes.
- **Apartados 3-4 (introducción)**: genera la **introducción** siguiendo el modelo **CARS (Swales)** + los **3 ejes de Shaw** (tipo de pregunta de investigación, tipo de contribución, tipo de validación). Pipeline de 10 agentes especializados.

Cada uno tiene dos modos de funcionamiento:

- **Modo interactivo**: el sistema hace preguntas al autor y obtiene la información por consola.
- **Modo PDF**: el sistema lee un PDF de un paper (sin abstract / sin introducción) y, en el caso de la introducción, también los PDFs de los papers citados (carpeta `<paper>_citas/`), y extrae la información automáticamente.

---

## Stack tecnológico

| Elemento | Detalle |
|---|---|
| Framework MAS | CrewAI 1.9.3 (`crewai[google-genai,tools]`) |
| LLM | Configurable por `.env` (variable `MODEL`). Actualmente `openrouter/openai/gpt-4o-mini` |
| Gestión de paquetes | `uv` (entorno en `.venv/`) |
| Lectura de PDFs | `pdfplumber` (dep. de crewai) |
| Manipulación de PDFs | `PyMuPDF` (`fitz`) — para eliminar abstracts/introducciones (redacción con rectángulo blanco) |
| Python | ≥ 3.10, < 3.14 |

---

## Estructura de ficheros del proyecto

```
TFG/TFG/
├── pyproject.toml                        ← dependencias y entrypoints
├── CONTEXTO_PROYECTO.md                  ← este fichero
├── .env                                  ← MODEL, API keys (gitignored)
│
├── src/abstrack/
│   ├── crew.py                           ← definición del crew (abstract + introducción)
│   ├── main.py                           ← entrypoint CLI
│   ├── comparacion.py                    ← genera los Excel de comparación
│   ├── config/
│   │   ├── agents.yaml                   ← configuración de agentes
│   │   └── tasks.yaml                    ← configuración de tareas
│   └── tools/
│       └── custom_tools.py               ← leer_pdf, leer_pdfs_carpeta, preguntar_al_autor
│
├── papers/
│   ├── original/                         ← PDFs intactos
│   │   ├── attention_is_all_you_need.pdf (inglés, Vaswani 2017)
│   │   └── redes_neuronales_parkinson.pdf (español, Rodriguez 2023)
│   ├── sin_abstract/                     ← PDFs con abstract eliminado → ENTRADA apartados 1-2
│   │   ├── attention_is_all_you_need.pdf
│   │   └── redes_neuronales_parkinson.pdf
│   └── sin_introduccion/                 ← PDFs con introducción eliminada → ENTRADA apartados 3-4 (modo PDF)
│       ├── attention_is_all_you_need.pdf  (intro de la pág. 2 redactada con fitz)
│       └── attention_is_all_you_need_citas/   ← papers citados reales descargados de arXiv
│           ├── bahdanau_2014_neural_mt_align_translate.pdf  (arXiv:1409.0473)
│           └── sutskever_2014_seq2seq.pdf      (arXiv:1409.3215)
│
├── abstracts/
│   ├── originales/                       ← abstracts reales (referencia para comparar)
│   ├── generados/<paper>_generado.md     ← abstracts producidos por el sistema
│   └── comparacion_abstracts.xlsx        ← Excel de comparación (generado)
│
└── introducciones/
    ├── originales/introduccion_<paper>.md ← introducción real + tabla "Puntos clave esperados (CARS + Shaw)"
    ├── generadas/<paper>_generada.md      ← introducción producida por el sistema
    ├── salida/informe_pdf_intro.md        ← informe validado (7 puntos CARS+Shaw) generado por la fase de adquisición
    └── comparacion_introducciones.xlsx    ← Excel de comparación (generado)
```

---

## APARTADOS 1-2 — Pipeline de Abstract (7 agentes, ESTADO: completo y probado)

| # | Agente | Rol | Modo |
|---|---|---|---|
| 0 | `agente_coordinador` | Manager jerárquico | Ambos |
| 1a | `agente_de_adquisicion_de_informacion` | Pregunta al autor por consola | Interactivo |
| 1b | `agente_de_adquisicion_pdf` | Lee el PDF y extrae 6 puntos clave | PDF |
| 2 | `agente_de_validacion_de_completitud` | Valida (loop hasta VALIDADO) | Ambos |
| 3 | `agente_de_estructuracion_de_contenido` | Esqueleto conceptual | Ambos |
| 4 | `agente_redactor` | Redacta el abstract | Ambos |
| 5 | `agente_de_revision_de_estilo` | Pule forma | Ambos |
| 6 | `agente_de_control_de_calidad` | Verificación final | Ambos |

Flujo: Adquisición → Validación (loop) → Estructuración → Redacción → Revisión → Control de calidad → `abstracts/generados/<paper>_generado.md`.

Probado con los 2 papers (inglés y español). `abstracts/comparacion_abstracts.xlsx` generado y revisado.

---

## APARTADOS 3-4 — Pipeline de Introducción CARS + Shaw (10 agentes, ESTADO: implementado, probado parcialmente)

Sustituye por completo el pipeline genérico para `tipo == "introduccion"` (interactivo y PDF). El modo abstract no se toca.

| # | Agente | Rol | Modo |
|---|---|---|---|
| 0 | `agente_coordinador_intro` | Manager jerárquico (variante de `agente_coordinador`) | Ambos |
| 1a | `agente_de_adquisicion_de_informacion` | Entrevista al autor (8 encabezados) | Interactivo |
| 1b | `agente_de_adquisicion_pdf` | Lee `leer_pdf` (paper) + `leer_pdfs_carpeta` (citas) | PDF |
| 2 | `agente_de_validacion_de_completitud` | Valida los 7 puntos CARS+Shaw (loop hasta VALIDADO) | Ambos |
| 3 | `agente_especialista_territorio` | Bloque "Territorio" | Ambos |
| 4 | `agente_especialista_hueco` | Bloque "Hueco" (citas reales, marca `[VERIFICAR]` si falta evidencia) | Ambos |
| 5 | `agente_especialista_idea` | Bloque "Idea/Enfoque" | Ambos |
| 6 | `agente_especialista_contribuciones` | Bloque "Contribuciones" (lista en viñetas) | Ambos |
| 7 | `agente_especialista_evaluacion` | Bloque "Evaluación" (avance, sin resultados numéricos) | Ambos |
| 8 | `agente_especialista_estructura_documento` | Bloque "Estructura del Documento" | Ambos |
| 9 | `agente_editor_intro` | Fusiona los 6 bloques, comprueba ejes de Shaw | Ambos |
| 10 | `agente_de_control_de_calidad` | Verificación global final | Ambos |

### Flujo de tareas (`tareas_cars_intro` en `crew.py`)

```
[Adquisición: tarea_adquisicion_intro / tarea_adquisicion_pdf_intro]
       ↓
tarea_validacion_intro  (loop VALIDADO/NO VALIDADO con agente_de_validacion_de_completitud)
       ↓
tarea_bloque_territorio
       ↓
tarea_bloque_hueco
       ↓
tarea_bloque_idea
       ↓
tarea_bloque_contribuciones
       ↓
tarea_bloque_evaluacion
       ↓
tarea_bloque_estructura_documento
       ↓
tarea_fusion_intro   (agente_editor_intro fusiona los 6 bloques)
       ↓
tarea_control_calidad_intro
       ↓
[introducciones/generadas/<paper>_generada.md]
```

### Fix de fidelidad con `context=` (aplicado en `crew.py`, NO verificado aún en producción)

CrewAI 1.9.3 soporta `Task(context=[otras_tareas])`: inyecta el `output.raw` **verbatim** de las tareas referenciadas en el prompt de la tarea actual (vía `format_task_with_context`), independientemente del relay en lenguaje natural del manager jerárquico. Se añadió:

- `tarea_bloque_territorio`: `context=[tarea_validacion_intro]`
- `tarea_bloque_hueco`: `context=[tarea_validacion_intro, tarea_bloque_territorio]`
- `tarea_bloque_idea`: `context=[tarea_validacion_intro, tarea_bloque_hueco]`
- `tarea_bloque_contribuciones`: `context=[tarea_validacion_intro, tarea_bloque_idea]`
- `tarea_bloque_evaluacion`: `context=[tarea_validacion_intro]`
- `tarea_bloque_estructura_documento`: `context=[tarea_validacion_intro]`
- `tarea_fusion_intro`: `context=[tarea_validacion_intro] + los 6 bloques`
- `tarea_control_calidad_intro`: `context=[tarea_fusion_intro]`

**Limitación conocida**: en `Process.hierarchical`, el agente que ejecuta cada `tarea_bloque_*` es el **manager**, no el especialista. `context=` garantiza que el manager tenga el texto verbatim en su propio prompt, pero el manager aún tiene que retransmitirlo al especialista vía la tool "Delegate work to coworker" (argumento `context` generado por su propio LLM), donde puede seguir parafraseando. Es una mejora parcial, no una solución completa. Si tras la próxima prueba real persisten problemas (pérdida de nombres como "Transformer"/Bahdanau/Sutskever, viñetas, secciones inventadas), la solución de raíz sería dividir en dos crews: una jerárquica (adquisición + validación) y otra **secuencial** para los 6 bloques + fusión + control de calidad (con `agent:` fijo y `context=` encadenado, sin manager de por medio).

---

## Herramientas custom (`src/abstrack/tools/custom_tools.py`)

```python
# Modo interactivo
@tool("preguntar_al_autor")
def ask_human_tool(pregunta: str) -> str: ...   # input() por consola

# Modo PDF
@tool("leer_pdf")
def read_pdf_tool(ruta_pdf: str) -> str: ...    # pdfplumber, un solo PDF

@tool("leer_pdfs_carpeta")
def read_pdfs_folder_tool(ruta_carpeta: str) -> str: ...  # concatena TODOS los PDFs de la carpeta en un solo string
```

---

## Cómo se lanza

Desde la raíz del proyecto (`TFG/TFG/`):

```powershell
# Abstract — interactivo
.venv/Scripts/abstrack.exe

# Abstract — modo PDF
.venv/Scripts/abstrack.exe --pdf papers/sin_abstract/attention_is_all_you_need.pdf

# Introducción — interactivo
.venv/Scripts/abstrack.exe --tipo introduccion

# Introducción — modo PDF (requiere papers/sin_introduccion/<paper>_citas/ con los PDFs citados)
.venv/Scripts/abstrack.exe --tipo introduccion --pdf papers/sin_introduccion/attention_is_all_you_need.pdf
```

---

## Estado de las pruebas con "Attention Is All You Need"

- **Apartados 1-2 (abstract)**: probado, `abstracts/comparacion_abstracts.xlsx` generado.
- **Apartado 3-4 (introducción), modo PDF**:
  - Test 1 (3 PDFs reales grandes): falló por overflow de contexto (128k tokens).
  - Test 2 (PDFs sintéticos pequeños generados con LaTeX): éxito, introducción CARS coherente de 8 párrafos.
  - Test 3 (paper real "Attention Is All You Need" + 2 citas reales de arXiv, Bahdanau 2014 + Sutskever 2014): **éxito técnico** (sin overflow, sin "Maximum iterations"), `comparacion_introducciones.xlsx` generado. Pero **regresión de calidad**: la introducción final (`introducciones/generadas/attention_is_all_you_need_generada.md`) pierde menciones a "Transformer", Bahdanau/Sutskever, el formato de viñetas en Contribuciones, e inventa números de sección falsos ("sección 2"–"sección 8"), pese a que `informe_pdf_intro.md` (informe validado) sí tenía todo correcto.
  - Test 4 (tras aplicar el fix de `context=`): **no completado** — la clave de OpenRouter alcanzó su límite mensual ($4/mes, agotado) y el run falló con error 402 a mitad de ejecución. `informe_pdf_intro.md` se regeneró correctamente (sigue citando bien a Bahdanau/Sutskever), pero `_generada.md` y el Excel siguen siendo del Test 3 (sin verificar el fix).

---

## Pendiente / próximos pasos

1. **Migración a AWS Bedrock en curso** (para evitar el límite de OpenRouter y aprovechar 200k de contexto):
   - Falta: credenciales AWS (Access Key ID + Secret Access Key de un usuario IAM con `AmazonBedrockFullAccess`), región con Bedrock+Claude habilitado (Estocolmo `eu-north-1` no vale; usar Frankfurt `eu-central-1` o N. Virginia `us-east-1`), habilitar "Model access" para Anthropic Claude, y confirmar si los $100 de crédito promocional cubren Bedrock.
   - Modelo recomendado: Claude 3.5 Sonnet (mejor fidelidad a instrucciones + 200k contexto, ~$3-4/ejecución completa → ~25 ejecuciones con 100€).
   - Una vez con credenciales: instalar `boto3`, poner `MODEL=bedrock/<model-id>` + variables `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_REGION_NAME` en `.env`.
   - Alternativa más simple: subir el límite mensual de la clave OpenRouter (€10-15) y seguir con `gpt-4o-mini` sin tocar nada.
2. **Re-ejecutar Test 4** (con OpenRouter con más límite, o con Bedrock) y comparar `_generada.md` contra `informe_pdf_intro.md` y `introduccion_attention_is_all_you_need.md` para verificar si el fix de `context=` corrige la regresión de fidelidad.
3. Si la regresión persiste: implementar la solución de raíz (split en crew jerárquica + crew secuencial) descrita arriba — requiere confirmación del usuario antes de implementar (cambio de arquitectura).
4. Limpiar `introducciones/salida/informe_intro.md` (artefacto de una prueba interactiva antigua, formato pre-CARS) si ya no es necesario.
