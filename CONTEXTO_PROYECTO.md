# Contexto del Proyecto — ABSTRACK (TFG Samuel Gómez)

Este fichero resume todo lo implementado en el proyecto para que puedas retomar el trabajo en otro PC pasándoselo a Claude como contexto.

---

## ¿Qué es el proyecto?

Sistema multiagente jerárquico (MAS) construido con **CrewAI** que genera el **abstract** de un artículo científico. Tiene dos modos de funcionamiento:

- **Modo interactivo**: el sistema hace preguntas al autor y obtiene la información por consola.
- **Modo PDF** (añadido en esta sesión): el sistema lee un PDF de un paper (sin abstract) y extrae la información automáticamente.

---

## Stack tecnológico

| Elemento | Detalle |
|---|---|
| Framework MAS | CrewAI 1.9.3 (`crewai[google-genai,tools]`) |
| LLM | Configurable por `.env` (variable `MODEL`) |
| Gestión de paquetes | `uv` |
| Lectura de PDFs | `pdfplumber` (ya instalado como dep. de crewai) |
| Manipulación de PDFs | `PyMuPDF` (`fitz`) — para eliminar abstracts |
| Python | ≥ 3.10, < 3.14 |

---

## Estructura de ficheros del proyecto

```
TFG/TFG/
├── pyproject.toml                        ← dependencias y entrypoints
├── CONTEXTO_PROYECTO.md                  ← este fichero
│
├── src/abstrack/
│   ├── crew.py                           ← definición del crew (MODIFICADO)
│   ├── main.py                           ← entrypoint CLI (MODIFICADO)
│   ├── config/
│   │   ├── agents.yaml                   ← configuración de agentes (MODIFICADO)
│   │   └── tasks.yaml                    ← configuración de tareas (MODIFICADO)
│   └── tools/
│       └── custom_tools.py               ← herramientas custom (MODIFICADO)
│
├── papers/
│   ├── original/                         ← PDFs intactos (con abstract)
│   │   ├── attention_is_all_you_need.pdf (inglés, Vaswani 2017)
│   │   └── redes_neuronales_parkinson.pdf (español, Rodriguez 2023)
│   ├── sin_abstract/                     ← PDFs con abstract eliminado → ENTRADA AL SISTEMA
│   │   ├── attention_is_all_you_need.pdf
│   │   └── redes_neuronales_parkinson.pdf
│   └── salida/                           ← informe_entrevista.md generado por el agente
│
└── abstracts/
    ├── originales/                       ← abstracts reales de los papers (para comparar)
    │   ├── abstract_attention_is_all_you_need.md
    │   └── abstract_redes_neuronales_parkinson.md
    └── generados/                        ← abstracts producidos por el sistema (se crean solos)
        └── <nombre_paper>_generado.md
```

---

## Agentes del sistema (7 en total)

| # | Agente | Rol | Modo |
|---|---|---|---|
| 0 | `agente_coordinador` | Manager jerárquico, orquesta el flujo | Ambos |
| 1a | `agente_de_adquisicion_de_informacion` | Hace preguntas al autor por consola | Solo interactivo |
| 1b | `agente_de_adquisicion_pdf` | Lee el PDF y extrae los 6 puntos clave | Solo PDF |
| 2 | `agente_de_validacion_de_completitud` | Valida que la info es suficiente (loop hasta VALIDADO) | Ambos |
| 3 | `agente_de_estructuracion_de_contenido` | Organiza el esqueleto conceptual | Ambos |
| 4 | `agente_redactor` | Escribe el abstract en prosa académica | Ambos |
| 5 | `agente_de_revision_de_estilo` | Pule forma sin cambiar fondo | Ambos |
| 6 | `agente_de_control_de_calidad` | Verificación final | Ambos |

---

## Flujo de ejecución

```
[PDF / Preguntas]
       ↓
1. Adquisición  ──────────────────────────────────────────────────────────────┐
       ↓                                                                       │
2. Validación → si NO VALIDADO → vuelve a Adquisición con lagunas detectadas ─┘
       ↓ (VALIDADO)
3. Estructuración
       ↓
4. Redacción
       ↓
5. Revisión de estilo
       ↓
6. Control de calidad
       ↓
[abstract_final guardado en abstracts/generados/<nombre>_generado.md]
```

---

## Herramientas custom (`src/abstrack/tools/custom_tools.py`)

```python
# Modo interactivo
@tool("preguntar_al_autor")
def ask_human_tool(pregunta: str) -> str:
    # Imprime la pregunta y recoge respuesta por consola (input())

# Modo PDF
@tool("leer_pdf")
def read_pdf_tool(ruta_pdf: str) -> str:
    # Usa pdfplumber para extraer todo el texto del PDF
```

---

## Cómo se selecciona el modo en crew.py

```python
class Abstrack():
    pdf_path: str = None  # Se asigna externamente antes de llamar a crew()

    @crew
    def crew(self) -> Crew:
        if self.pdf_path:
            # Modo PDF: usa agente_de_adquisicion_pdf + tarea_adquisicion_pdf
            agentes = [agente_de_adquisicion_pdf(), ...]
            tareas  = [tarea_adquisicion_pdf(), ...]
        else:
            # Modo interactivo: usa self.agents y self.tasks (auto-recopilados por @agent/@task)
            agentes = self.agents
            tareas  = [tarea_adquisicion(), ...]
```

---

## Cómo se lanza

Desde la raíz del proyecto (`TFG/TFG/`), con PowerShell:

```powershell
# Modo interactivo
uv run abstrack

# Modo PDF — inglés
uv run abstrack --pdf papers/sin_abstract/attention_is_all_you_need.pdf

# Modo PDF — español
uv run abstrack --pdf papers/sin_abstract/redes_neuronales_parkinson.pdf
```

Si el comando no se reconoce, instalar primero en modo editable:
```powershell
uv pip install -e .
```

---

## Salidas generadas

| Fichero | Dónde | Qué contiene |
|---|---|---|
| `informe_entrevista.md` | `papers/salida/` | Los 6 puntos extraídos (input al redactor) |
| `<paper>_generado.md` | `abstracts/generados/` | Abstract final generado por el sistema |

---

## Papers de prueba

### Paper 1 — Inglés
- **Título**: Attention Is All You Need (Vaswani et al., 2017)
- **arXiv**: 1706.03762
- **Abstract original**: `abstracts/originales/abstract_attention_is_all_you_need.md`

### Paper 2 — Español
- **Título**: Aplicación de Redes Neuronales Artificiales para la Clasificación de AVDs en Parkinson
- **Autores**: Rodriguez Montero et al., 2023
- **Revista**: Revista Mexicana de Ingeniería Biomédica, Vol. 44, No. 4
- **Abstract original**: `abstracts/originales/abstract_redes_neuronales_parkinson.md`

Los PDFs en `papers/sin_abstract/` tienen el abstract eliminado programáticamente con PyMuPDF (redacción con rectángulo blanco sobre la zona del abstract).

---

## Próximos pasos pendientes del TFG

- [ ] Ejecutar el sistema en modo PDF con los dos papers y obtener los abstracts generados
- [ ] Comparar `abstracts/generados/` con `abstracts/originales/` (comparación manual o con métricas como ROUGE/BLEU)
- [ ] Posible: añadir un agente de comparación automática si se decide no hacerlo manualmente
