"""Interfaz web Streamlit para el sistema multiagente Abstrack."""
import os
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import warnings
from datetime import datetime
from pathlib import Path

import streamlit as st

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# ── Estilos ────────────────────────────────────────────────────────────────────

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ── Fondo principal ── */
.stApp { background: #0b1120; }
.stMain { background: #0b1120; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f1929 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    min-width: 290px !important;
    max-width: 320px !important;
}
[data-testid="stSidebar"] .stMarkdown p { color: #94a3b8 !important; }

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #1e1b4b 0%, #1e3a5f 55%, #0c4a6e 100%);
    border: 1px solid rgba(99,102,241,0.25);
    padding: 2rem 2.5rem 1.75rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px -15px rgba(99,102,241,0.3);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    color: #f1f5f9 !important;
    font-size: 1.85rem !important;
    font-weight: 700 !important;
    margin: 0 0 0.4rem !important;
    letter-spacing: -0.3px !important;
    line-height: 1.25 !important;
}
.hero p {
    color: rgba(241,245,249,0.6) !important;
    font-size: 0.88rem !important;
    margin: 0 !important;
    letter-spacing: 0.2px !important;
}
.hero-badges {
    display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap;
}
.badge {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 0.2rem 0.65rem;
    font-size: 0.72rem;
    font-weight: 500;
    color: rgba(241,245,249,0.7);
    letter-spacing: 0.3px;
}

/* ── Mode cards (idle) ── */
.mode-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem; }
.mode-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.5rem;
    transition: border-color 0.2s, background 0.2s;
}
.mode-card:hover { background: rgba(255,255,255,0.06); border-color: rgba(99,102,241,0.4); }
.mode-card .mc-icon { font-size: 1.8rem; margin-bottom: 0.65rem; display: block; }
.mode-card .mc-title {
    color: #e2e8f0 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin: 0 0 0.4rem !important;
}
.mode-card .mc-desc {
    color: #64748b !important;
    font-size: 0.84rem !important;
    line-height: 1.55 !important;
    margin: 0 !important;
}

/* ── Hint box ── */
.hint-box {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 10px;
    padding: 0.85rem 1.25rem;
    color: #a5b4fc;
    font-size: 0.875rem;
    line-height: 1.5;
}

/* ── Result card ── */
.result-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 3px solid #10b981;
    border-radius: 12px;
    padding: 2rem 2.25rem;
    line-height: 1.85;
    font-size: 0.97rem;
    color: #cbd5e1;
}
.result-card p { color: #cbd5e1 !important; }
.result-card h1, .result-card h2, .result-card h3 { color: #f1f5f9 !important; }
.result-card li { color: #cbd5e1 !important; }
.result-card strong { color: #e2e8f0 !important; }

/* ── Result label ── */
.result-label {
    display: flex; align-items: center; gap: 0.75rem;
    margin-bottom: 1rem;
}
.result-label .rl-text {
    font-size: 1.1rem; font-weight: 600; color: #e2e8f0;
}
.result-label .rl-badge {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    color: #34d399;
    border-radius: 20px;
    padding: 0.18rem 0.65rem;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

/* ── Buttons ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #0ea5e9 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 4px 15px rgba(79,70,229,0.3) !important;
    transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
    color: white !important;
}
.stButton > button[kind="primary"]:hover {
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(79,70,229,0.4) !important;
}
.stButton > button:not([kind="primary"]) {
    border-radius: 8px !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: #94a3b8 !important;
    background: rgba(255,255,255,0.04) !important;
}
.stButton > button:not([kind="primary"]):hover {
    border-color: rgba(255,255,255,0.18) !important;
    color: #cbd5e1 !important;
    background: rgba(255,255,255,0.07) !important;
}

/* ── Form submit button ── */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #0ea5e9 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    color: white !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    margin-bottom: 0.75rem !important;
}

/* ── Text area ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
}

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; }
[data-testid="stNotification"] { border-radius: 10px !important; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; margin: 1.25rem 0 !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 10px !important;
}

/* ── Sidebar section label ── */
.sb-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: #334155;
    margin: 0.25rem 0 0.75rem;
    display: block;
}

/* ── Running status chip ── */
.status-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.8rem;
    font-weight: 500;
    color: #a5b4fc;
    margin-bottom: 1rem;
}
.status-dot {
    width: 7px; height: 7px;
    background: #6366f1;
    border-radius: 50%;
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.8); }
}

/* ── Steps feed ── */
.steps-feed { display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 1.25rem; }
.step-item {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.55rem 1rem;
    background: rgba(16,185,129,0.05);
    border: 1px solid rgba(16,185,129,0.15);
    border-radius: 8px;
    font-size: 0.855rem;
    color: #94a3b8;
    animation: fadeIn 0.35s ease;
}
.step-item .si-icon { color: #10b981; font-size: 0.9rem; flex-shrink: 0; }
.step-item .si-text { color: #cbd5e1; }
@keyframes fadeIn { from { opacity:0; transform:translateY(4px); } to { opacity:1; transform:none; } }
</style>
"""


# ── Pipeline runner (hilo secundario) ─────────────────────────────────────────

def _run_pipeline(tipo, pdf_path, citas_path, idioma, q_questions, q_answers, q_result, q_status):
    from abstrack.tools.custom_tools import set_web_queues, clear_web_queues
    from abstrack.crew import Abstrack

    set_web_queues(q_questions, q_answers)

    # En modo jerárquico task_output.agent es siempre el coordinador (manager).
    # Se pre-calcula la lista de agentes esperados por orden de ejecución para
    # mostrar el agente real en cada paso.
    if pdf_path and tipo == "introduccion":
        _task_labels = [
            "Agente de Adquisición desde PDF",
            "Agente de Validación de Completitud",
            "Especialista en Territorio",
            "Especialista en Hueco",
            "Especialista en Idea",
            "Especialista en Contribuciones",
            "Especialista en Evaluación",
            "Especialista en Estructura del Documento",
            "Agente Editor de la Introducción",
            "Agente de Control de Calidad",
        ]
    elif pdf_path:
        _task_labels = [
            "Agente de Adquisición desde PDF",
            "Agente de Validación de Completitud",
            "Agente de Estructuración del Contenido",
            "Agente Redactor",
            "Agente de Revisión de Estilo",
            "Agente de Control de Calidad",
        ]
    elif tipo == "introduccion":
        _task_labels = [
            "Agente de Adquisición de Información",
            "Agente de Validación de Completitud",
            "Especialista en Territorio",
            "Especialista en Hueco",
            "Especialista en Idea",
            "Especialista en Contribuciones",
            "Especialista en Evaluación",
            "Especialista en Estructura del Documento",
            "Agente Editor de la Introducción",
            "Agente de Control de Calidad",
        ]
    else:
        _task_labels = [
            "Agente de Adquisición de Información",
            "Agente de Validación de Completitud",
            "Agente de Estructuración del Contenido",
            "Agente Redactor",
            "Agente de Revisión de Estilo",
            "Agente de Control de Calidad",
        ]

    _task_counter = [0]

    def on_task_done(task_output):
        try:
            idx = _task_counter[0]
            if idx < len(_task_labels):
                label = _task_labels[idx]
            else:
                label = getattr(task_output, 'summary', None) or getattr(task_output, 'agent', 'Tarea completada')
            _task_counter[0] += 1
            q_status.put(str(label))
        except Exception:
            pass

    try:
        inputs = {
            "topic": "abstract generation",
            "current_year": str(datetime.now().year),
            "pdf_path": pdf_path or "",
            "citas_path": citas_path or "",
            "idioma": idioma,
        }
        crew = Abstrack()
        crew.pdf_path = pdf_path
        crew.citas_path = citas_path or ""
        crew.tipo = tipo
        crew.idioma = idioma
        crew.task_callback = on_task_done
        resultado = crew.crew().kickoff(inputs=inputs)
        q_result.put(("ok", str(resultado)))
    except Exception as exc:
        q_result.put(("error", str(exc)))
    finally:
        q_questions.put(None)
        clear_web_queues()


# ── Helpers ────────────────────────────────────────────────────────────────────

def _init_session():
    defaults = {
        "state": "idle",
        "chat": [],
        "resultado": None,
        "error_msg": None,
        "q_questions": None,
        "q_answers": None,
        "q_result": None,
        "q_status": None,
        "steps_done": [],
        "thread": None,
        "tmp_dir": None,
        "tipo": "abstract",
        "pdf_path": None,
        "saved_path": None,
        "latex_path": None,
        "bib_path": None,
        "citas_path": None,
        "tex_existente": None,
        "latex_error": None,
        "bib_error": None,
        "uploader_key": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _save_result(resultado: str, tipo: str, pdf_path: str | None):
    from abstrack.comparacion import (
        generar_excel_comparacion_abstracts,
        generar_excel_comparacion_introducciones,
    )
    if tipo == "introduccion":
        carpeta = Path("introducciones/generadas")
        sufijo = "_generada.md"
        generar_excel = generar_excel_comparacion_introducciones
    else:
        carpeta = Path("abstracts/generados")
        sufijo = "_generado.md"
        generar_excel = generar_excel_comparacion_abstracts

    carpeta.mkdir(parents=True, exist_ok=True)
    nombre = (
        Path(pdf_path).stem if pdf_path
        else f"interactivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    destino = carpeta / f"{nombre}{sufijo}"
    destino.write_text(resultado, encoding="utf-8-sig")
    try:
        generar_excel()
    except Exception:
        pass
    return destino


def _cleanup_tmp():
    tmp = st.session_state.get("tmp_dir")
    if tmp and Path(tmp).exists():
        shutil.rmtree(tmp, ignore_errors=True)


def _reset():
    _cleanup_tmp()
    contador_uploaders = st.session_state.get("uploader_key", 0) + 1
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state["uploader_key"] = contador_uploaders
    st.rerun()


def _start_pipeline(tipo, modo_pdf, pdf_file, citas_files, idioma, tex_file=None):
    tmp_dir = None
    pdf_path = None
    citas_path = ""
    tex_existente = ""

    if tex_file is not None:
        tmp_dir = tmp_dir or tempfile.mkdtemp()
        tex_existente = os.path.join(tmp_dir, tex_file.name)
        with open(tex_existente, "wb") as f:
            f.write(tex_file.getbuffer())

    if modo_pdf and pdf_file is not None:
        tmp_dir = tmp_dir or tempfile.mkdtemp()
        pdf_path = os.path.join(tmp_dir, pdf_file.name)
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        if tipo == "introduccion":
            if citas_files:
                citas_dir = os.path.join(tmp_dir, "citas")
                os.makedirs(citas_dir, exist_ok=True)
                for cf in citas_files:
                    with open(os.path.join(citas_dir, cf.name), "wb") as f:
                        f.write(cf.getbuffer())
                citas_path = citas_dir
            else:
                citas_path = str(Path(pdf_path).with_name(f"{Path(pdf_path).stem}_citas"))

    q_questions: queue.Queue = queue.Queue()
    q_answers:   queue.Queue = queue.Queue()
    q_result:    queue.Queue = queue.Queue()
    q_status:    queue.Queue = queue.Queue()

    thread = threading.Thread(
        target=_run_pipeline,
        args=(tipo, pdf_path, citas_path, idioma, q_questions, q_answers, q_result, q_status),
        daemon=True,
    )
    thread.start()

    st.session_state.update({
        "state": "running", "tipo": tipo, "pdf_path": pdf_path,
        "citas_path": citas_path, "tmp_dir": tmp_dir, "chat": [], "steps_done": [],
        "q_questions": q_questions, "q_answers": q_answers,
        "q_result": q_result, "q_status": q_status,
        "thread": thread, "resultado": None, "saved_path": None,
        "latex_path": None, "bib_path": None, "error_msg": None,
        "tex_existente": tex_existente, "latex_error": None, "bib_error": None,
    })


# ── Página principal ────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Abstrack — Generador de Textos Científicos",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _init_session()
    st.markdown(_CSS, unsafe_allow_html=True)

    state = st.session_state.state

    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<span class="sb-label">⚙ Configuración</span>', unsafe_allow_html=True)

        if state == "idle":
            tipo_label = st.radio("**Tipo de texto**", ["Abstract", "Introducción"], index=0)
            tipo = "abstract" if tipo_label == "Abstract" else "introduccion"

            modo_label = st.radio(
                "**Entrada**",
                ["Interactivo (preguntas al autor)", "Desde PDF"],
                index=0,
            )
            modo_pdf = modo_label == "Desde PDF"

            idioma = st.selectbox("**Idioma de redacción**", ["Español", "Inglés"], index=0)

            pdf_file = None
            citas_files = []

            if modo_pdf:
                st.caption("Paper principal (sin abstract/introducción):")
                pdf_file = st.file_uploader(
                    "paper_pdf", type="pdf", label_visibility="collapsed",
                    key=f"paper_pdf_{st.session_state.uploader_key}",
                )
                if tipo == "introduccion":
                    st.caption("Papers citados (opcional):")
                    citas_files = st.file_uploader(
                        "citas_pdf", type="pdf", accept_multiple_files=True,
                        label_visibility="collapsed",
                        key=f"citas_pdf_{st.session_state.uploader_key}",
                    )

            st.divider()
            st.caption("¿Ya tienes el paper maquetado en LaTeX? Sube el .tex y el resultado se insertará en su sección de abstract o introducción, sin tocar el resto del documento (opcional):")
            tex_file = st.file_uploader(
                "tex_existente", type="tex", label_visibility="collapsed",
                key=f"tex_existente_{st.session_state.uploader_key}",
            )

            can_start = not modo_pdf or pdf_file is not None
            st.divider()

            if st.button("▶ Iniciar", disabled=not can_start, use_container_width=True, type="primary"):
                _start_pipeline(tipo, modo_pdf, pdf_file, citas_files, idioma, tex_file)
                st.rerun()

        else:
            tipo_str = "Introducción" if st.session_state.tipo == "introduccion" else "Abstract"
            modo_str = "PDF" if st.session_state.pdf_path else "Interactivo"
            st.info(f"**Modo activo:** {tipo_str} · {modo_str}")

            if state == "done" and st.session_state.saved_path:
                st.success(f"Guardado en:\n`{st.session_state.saved_path}`")

            st.divider()
            if st.button("↩ Nueva ejecución", use_container_width=True):
                _reset()

    # ── Hero header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <h1>🎓 Generador de Textos Científicos</h1>
        <p>Sistema multiagente para la redacción automatizada de abstracts e introducciones académicas</p>
        <div class="hero-badges">
            <span class="badge">Modelo CARS · Swales</span>
            <span class="badge">3 Ejes de Shaw</span>
            <span class="badge">Multi-agente · CrewAI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Idle ─────────────────────────────────────────────────────────────────
    if state == "idle":
        st.markdown("""
        <div class="mode-grid">
            <div class="mode-card">
                <span class="mc-icon">📝</span>
                <p class="mc-title">Abstract</p>
                <p class="mc-desc">
                    Genera el abstract de un artículo científico mediante una entrevista
                    guiada al autor o mediante la lectura directa del PDF del paper.
                </p>
            </div>
            <div class="mode-card">
                <span class="mc-icon">📄</span>
                <p class="mc-title">Introducción CARS</p>
                <p class="mc-desc">
                    Genera la introducción estructurada en seis bloques: Territorio, Hueco,
                    Idea, Contribuciones, Evaluación y Estructura del documento.
                </p>
            </div>
        </div>
        <div class="hint-box">
            ← Selecciona el tipo de texto y el modo de entrada en el panel izquierdo
            y pulsa <strong>▶ Iniciar</strong> para comenzar.
        </div>
        """, unsafe_allow_html=True)

    # ── Running / Waiting ─────────────────────────────────────────────────────
    elif state in ("running", "waiting"):
        for msg in st.session_state.chat:
            role = "assistant" if msg["role"] == "agent" else "user"
            with st.chat_message(role):
                st.write(msg["content"])

        if state == "waiting":
            with st.form("form_respuesta", clear_on_submit=True):
                respuesta = st.text_area(
                    "Tu respuesta:",
                    height=130,
                    placeholder="Escribe tu respuesta aquí…",
                )
                enviado = st.form_submit_button("Enviar →", use_container_width=True)
                if enviado and respuesta.strip():
                    st.session_state.chat.append({"role": "user", "content": respuesta.strip()})
                    st.session_state.q_answers.put(respuesta.strip())
                    st.session_state.state = "running"
                    st.rerun()

        elif state == "running":
            # Drena la cola de estado para acumular agentes completados
            qs = st.session_state.q_status
            if qs:
                while True:
                    try:
                        agent = qs.get_nowait()
                        st.session_state.steps_done.append(agent)
                    except queue.Empty:
                        break

            st.markdown("""
            <div class="status-chip">
                <span class="status-dot"></span>
                Sistema multiagente procesando…
            </div>
            """, unsafe_allow_html=True)

            # Feed de tareas completadas
            if st.session_state.steps_done:
                items_html = "".join(
                    f'<div class="step-item"><span class="si-icon">✓</span>'
                    f'<span class="si-text">{a}</span></div>'
                    for a in st.session_state.steps_done
                )
                st.markdown(f'<div class="steps-feed">{items_html}</div>', unsafe_allow_html=True)

            with st.spinner(""):
                try:
                    q = st.session_state.q_questions.get(timeout=2.0)
                    if q is None:
                        # Drenar cualquier agente pendiente antes de transicionar
                        if qs:
                            while True:
                                try:
                                    agent = qs.get_nowait()
                                    st.session_state.steps_done.append(agent)
                                except queue.Empty:
                                    break
                        status, payload = st.session_state.q_result.get()
                        if status == "ok":
                            from abstrack.bib_writer import limpiar_marcadores_cita, marcar_citas_sin_respaldo, generar_bib, limpiar_markdown
                            nombre = (
                                Path(st.session_state.pdf_path).stem
                                if st.session_state.pdf_path
                                else f"interactivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                            )
                            payload = limpiar_markdown(payload)
                            bib_text = None
                            if st.session_state.citas_path:
                                try:
                                    bib_dest = generar_bib(st.session_state.citas_path, nombre, st.session_state.tipo)
                                    if bib_dest:
                                        st.session_state.bib_path = str(bib_dest)
                                        bib_text = bib_dest.read_text(encoding="utf-8")
                                except Exception as exc:
                                    st.session_state.bib_error = str(exc)

                            payload_marcado = marcar_citas_sin_respaldo(payload, bib_text) if bib_text else payload
                            payload_limpio = limpiar_marcadores_cita(payload_marcado)
                            st.session_state.resultado = payload_limpio
                            st.session_state.state = "done"
                            try:
                                dest = _save_result(payload_limpio, st.session_state.tipo, st.session_state.pdf_path)
                                st.session_state.saved_path = str(dest)
                            except Exception:
                                pass
                            try:
                                # payload (no payload_limpio): generar_latex/actualizar_latex_existente
                                # necesitan los marcadores [[CITA: ...]] intactos para poder enlazar
                                # las citas con \cite{}.
                                if st.session_state.tex_existente:
                                    from abstrack.latex_writer import actualizar_latex_existente
                                    latex_dest = actualizar_latex_existente(
                                        st.session_state.tex_existente, payload, st.session_state.tipo, nombre, bib_text
                                    )
                                else:
                                    from abstrack.latex_writer import generar_latex
                                    latex_dest = generar_latex(payload, st.session_state.tipo, nombre, bib_text)
                                st.session_state.latex_path = str(latex_dest)
                            except Exception as exc:
                                st.session_state.latex_error = str(exc)
                        else:
                            st.session_state.error_msg = payload
                            st.session_state.state = "error"
                    else:
                        st.session_state.chat.append({"role": "agent", "content": q})
                        st.session_state.state = "waiting"
                except queue.Empty:
                    pass
            st.rerun()

    # ── Done ──────────────────────────────────────────────────────────────────
    elif state == "done":
        resultado = st.session_state.resultado

        if st.session_state.steps_done:
            with st.expander("🤖 Agentes ejecutados", expanded=False):
                for step in st.session_state.steps_done:
                    st.markdown(f"✓ {step}")

        if st.session_state.chat:
            with st.expander("💬 Ver conversación completa", expanded=False):
                for msg in st.session_state.chat:
                    role = "assistant" if msg["role"] == "agent" else "user"
                    with st.chat_message(role):
                        st.write(msg["content"])

        st.success("✅ Generación completada")

        st.markdown("""
        <div class="result-label">
            <span class="rl-text">Resultado</span>
            <span class="rl-badge">listo</span>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(resultado)

        st.divider()
        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
        with col1:
            st.download_button(
                label="⬇ Descargar resultado (.md)",
                data=resultado.encode("utf-8"),
                file_name=(
                    Path(st.session_state.saved_path).name
                    if st.session_state.saved_path else "resultado.md"
                ),
                mime="text/markdown",
                use_container_width=True,
            )
        with col2:
            if st.session_state.latex_path and Path(st.session_state.latex_path).exists():
                latex_content = Path(st.session_state.latex_path).read_text(encoding="utf-8")
                st.download_button(
                    label="⬇ Descargar plantilla IEEE (.tex)",
                    data=latex_content.encode("utf-8"),
                    file_name=Path(st.session_state.latex_path).name,
                    mime="text/x-tex",
                    use_container_width=True,
                )
            elif st.session_state.latex_error:
                st.error(f"No se pudo generar el .tex:\n\n{st.session_state.latex_error}")
        with col3:
            if st.session_state.bib_path and Path(st.session_state.bib_path).exists():
                bib_content = Path(st.session_state.bib_path).read_text(encoding="utf-8")
                st.download_button(
                    label="⬇ Descargar bibliografía (.bib)",
                    data=bib_content.encode("utf-8"),
                    file_name=Path(st.session_state.bib_path).name,
                    mime="text/plain",
                    use_container_width=True,
                )
            elif st.session_state.bib_error:
                st.error(f"No se pudo generar el .bib:\n\n{st.session_state.bib_error}")
        with col4:
            if st.button("↩ Nueva ejecución", use_container_width=True):
                _reset()

    # ── Error ─────────────────────────────────────────────────────────────────
    elif state == "error":
        st.error(f"Error durante la ejecución:\n\n{st.session_state.error_msg}")
        if st.button("↩ Volver al inicio"):
            _reset()


# ── Punto de entrada ───────────────────────────────────────────────────────────

def launch():
    app_file = str(Path(__file__).resolve())
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_file], check=True)


if __name__ == "__main__":
    main()
