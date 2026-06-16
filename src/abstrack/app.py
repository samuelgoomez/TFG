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


# ── Pipeline runner (hilo secundario) ─────────────────────────────────────────

def _run_pipeline(tipo, pdf_path, citas_path, q_questions, q_answers, q_result):
    from abstrack.tools.custom_tools import set_web_queues, clear_web_queues
    from abstrack.crew import Abstrack

    set_web_queues(q_questions, q_answers)
    try:
        inputs = {
            "topic": "abstract generation",
            "current_year": str(datetime.now().year),
            "pdf_path": pdf_path or "",
            "citas_path": citas_path or "",
        }
        crew = Abstrack()
        crew.pdf_path = pdf_path
        crew.citas_path = citas_path or ""
        crew.tipo = tipo
        resultado = crew.crew().kickoff(inputs=inputs)
        q_result.put(("ok", str(resultado)))
    except Exception as exc:
        q_result.put(("error", str(exc)))
    finally:
        q_questions.put(None)  # señal de fin para la UI
        clear_web_queues()


# ── Helpers ────────────────────────────────────────────────────────────────────

def _init_session():
    defaults = {
        "state": "idle",       # idle | running | waiting | done | error
        "chat": [],            # [{"role": "agent"|"user", "content": str}]
        "resultado": None,
        "error_msg": None,
        "q_questions": None,
        "q_answers": None,
        "q_result": None,
        "thread": None,
        "tmp_dir": None,
        "tipo": "abstract",
        "pdf_path": None,
        "saved_path": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _save_result(resultado: str, tipo: str, pdf_path: str | None):
    """Guarda el resultado en disco y devuelve la ruta."""
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
        Path(pdf_path).stem
        if pdf_path
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
    keys = list(st.session_state.keys())
    for k in keys:
        del st.session_state[k]
    st.rerun()


def _start_pipeline(tipo, modo_pdf, pdf_file, citas_files):
    tmp_dir = None
    pdf_path = None
    citas_path = ""

    if modo_pdf and pdf_file is not None:
        tmp_dir = tempfile.mkdtemp()
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
                # Intentar carpeta _citas junto al PDF subido (vacía)
                citas_path = str(
                    Path(pdf_path).with_name(f"{Path(pdf_path).stem}_citas")
                )

    q_questions: queue.Queue = queue.Queue()
    q_answers: queue.Queue = queue.Queue()
    q_result: queue.Queue = queue.Queue()

    thread = threading.Thread(
        target=_run_pipeline,
        args=(tipo, pdf_path, citas_path, q_questions, q_answers, q_result),
        daemon=True,
    )
    thread.start()

    st.session_state.state = "running"
    st.session_state.tipo = tipo
    st.session_state.pdf_path = pdf_path
    st.session_state.tmp_dir = tmp_dir
    st.session_state.chat = []
    st.session_state.q_questions = q_questions
    st.session_state.q_answers = q_answers
    st.session_state.q_result = q_result
    st.session_state.thread = thread
    st.session_state.resultado = None
    st.session_state.saved_path = None
    st.session_state.error_msg = None


# ── Página principal ────────────────────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Abstrack — Generador de Textos Científicos",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _init_session()

    # ── CSS mínimo ──────────────────────────────────────────────────────────
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { min-width: 280px; max-width: 320px; }
        .result-box { background:#f8f9fa; border-left:4px solid #4CAF50;
                      padding:1.2rem 1.5rem; border-radius:6px; margin-top:1rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## ⚙️ Configuración")
        st.divider()

        state = st.session_state.state

        if state == "idle":
            tipo_label = st.radio("**Tipo de texto**", ["Abstract", "Introducción"], index=0)
            tipo = "abstract" if tipo_label == "Abstract" else "introduccion"

            modo_label = st.radio(
                "**Entrada**",
                ["Interactivo (preguntas al autor)", "Desde PDF"],
                index=0,
            )
            modo_pdf = modo_label == "Desde PDF"

            pdf_file = None
            citas_files = []

            if modo_pdf:
                st.caption("Paper sin abstract/introducción:")
                pdf_file = st.file_uploader(
                    "paper_pdf", type="pdf", label_visibility="collapsed"
                )
                if tipo == "introduccion":
                    st.caption("Papers citados en la introducción (opcional):")
                    citas_files = st.file_uploader(
                        "citas_pdf",
                        type="pdf",
                        accept_multiple_files=True,
                        label_visibility="collapsed",
                    )

            can_start = not modo_pdf or pdf_file is not None
            st.divider()

            if st.button(
                "▶ Iniciar",
                disabled=not can_start,
                use_container_width=True,
                type="primary",
            ):
                _start_pipeline(tipo, modo_pdf, pdf_file, citas_files)
                st.rerun()

        else:
            tipo_str = "Introducción" if st.session_state.tipo == "introduccion" else "Abstract"
            modo_str = "PDF" if st.session_state.pdf_path else "Interactivo"
            st.info(f"**Modo activo:** {tipo_str} · {modo_str}")
            st.divider()

            if state == "done" and st.session_state.saved_path:
                st.success(f"Guardado en:\n`{st.session_state.saved_path}`")

            st.divider()
            if st.button("↩ Nueva ejecución", use_container_width=True):
                _reset()

    # ── Área principal ────────────────────────────────────────────────────────
    st.markdown("# 🎓 Generador de Textos Científicos")
    st.caption(
        "Sistema multiagente basado en el modelo CARS (Swales) y los 3 ejes de Shaw"
    )
    st.divider()

    state = st.session_state.state

    # ── Idle ─────────────────────────────────────────────────────────────────
    if state == "idle":
        col_a, col_b = st.columns(2)
        with col_a:
            st.info(
                "Configura los parámetros en el panel izquierdo y pulsa **▶ Iniciar**."
            )
        with col_b:
            st.markdown(
                """
**Modos disponibles:**
- 📝 **Abstract** · desde preguntas al autor o lectura de PDF
- 📄 **Introducción CARS** · desde preguntas al autor o lectura de PDF + papers citados
                """
            )

    # ── Running / Waiting ─────────────────────────────────────────────────────
    elif state in ("running", "waiting"):
        # Historial de conversación
        for msg in st.session_state.chat:
            role = "assistant" if msg["role"] == "agent" else "user"
            with st.chat_message(role):
                st.write(msg["content"])

        if state == "waiting":
            with st.form("form_respuesta", clear_on_submit=True):
                respuesta = st.text_area(
                    "Tu respuesta:",
                    height=130,
                    placeholder="Escribe tu respuesta aquí...",
                )
                enviado = st.form_submit_button("Enviar →", use_container_width=True)
                if enviado and respuesta.strip():
                    st.session_state.chat.append(
                        {"role": "user", "content": respuesta.strip()}
                    )
                    st.session_state.q_answers.put(respuesta.strip())
                    st.session_state.state = "running"
                    st.rerun()

        elif state == "running":
            with st.spinner("El sistema multiagente está procesando..."):
                try:
                    q = st.session_state.q_questions.get(timeout=2.0)
                    if q is None:
                        # Pipeline terminado
                        status, payload = st.session_state.q_result.get()
                        if status == "ok":
                            st.session_state.resultado = payload
                            st.session_state.state = "done"
                            # Guardar en disco
                            try:
                                dest = _save_result(
                                    payload,
                                    st.session_state.tipo,
                                    st.session_state.pdf_path,
                                )
                                st.session_state.saved_path = str(dest)
                            except Exception:
                                pass
                        else:
                            st.session_state.error_msg = payload
                            st.session_state.state = "error"
                    else:
                        st.session_state.chat.append(
                            {"role": "agent", "content": q}
                        )
                        st.session_state.state = "waiting"
                except queue.Empty:
                    pass
            st.rerun()

    # ── Done ──────────────────────────────────────────────────────────────────
    elif state == "done":
        resultado = st.session_state.resultado

        if st.session_state.chat:
            with st.expander("💬 Ver conversación completa", expanded=False):
                for msg in st.session_state.chat:
                    role = "assistant" if msg["role"] == "agent" else "user"
                    with st.chat_message(role):
                        st.write(msg["content"])

        st.success("✅ Generación completada")
        st.subheader("Resultado")
        st.markdown(resultado)
        st.divider()

        col1, col2 = st.columns([3, 1])
        with col1:
            st.download_button(
                label="⬇ Descargar resultado (.md)",
                data=resultado.encode("utf-8"),
                file_name=(
                    st.session_state.saved_path
                    and Path(st.session_state.saved_path).name
                    or "resultado.md"
                ),
                mime="text/markdown",
                use_container_width=True,
            )
        with col2:
            if st.button("↩ Nueva ejecución", use_container_width=True):
                _reset()

    # ── Error ─────────────────────────────────────────────────────────────────
    elif state == "error":
        st.error(f"Error durante la ejecución:\n\n{st.session_state.error_msg}")
        if st.button("↩ Volver al inicio"):
            _reset()


# ── Punto de entrada para el script de consola ────────────────────────────────

def launch():
    """Lanza el servidor Streamlit. Usado por el script 'abstrack-web'."""
    app_file = str(Path(__file__).resolve())
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", app_file],
        check=True,
    )


if __name__ == "__main__":
    main()
