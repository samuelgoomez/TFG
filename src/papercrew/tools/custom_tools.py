import queue as _queue_module
from crewai.tools import tool

# When running in web mode these are set to Queue objects before starting the pipeline thread.
# In CLI mode they stay None and the tool falls back to input().
_q_questions = None
_q_answers = None

# Ruta del informe de esta sesión: deja constancia de cada pregunta/respuesta sin depender
# de que ningún agente se acuerde de guardarlo. Se fija antes de arrancar el pipeline (ver crew.py).
_informe_path = None


def set_web_queues(q_questions, q_answers):
    global _q_questions, _q_answers
    _q_questions = q_questions
    _q_answers = q_answers


def clear_web_queues():
    global _q_questions, _q_answers
    _q_questions = None
    _q_answers = None


def set_informe_path(ruta):
    """Fija la ruta del informe de esta sesión y la deja vacía, para que el
    registro en bruto de preguntas y respuestas empiece de cero (y no se
    mezcle con el de una ejecución anterior sobre ese mismo fichero)."""
    global _informe_path
    _informe_path = ruta
    from pathlib import Path

    ruta_path = Path(ruta)
    ruta_path.parent.mkdir(parents=True, exist_ok=True)
    ruta_path.write_text("", encoding="utf-8")


def clear_informe_path():
    global _informe_path
    _informe_path = None


def _registrar_pregunta_respuesta(pregunta: str, respuesta: str) -> None:
    """Añade la pregunta y la respuesta al informe de la sesión, si hay una
    ruta configurada. Es un registro en bruto (no el informe final pulido
    por 6 apartados), pero garantiza que quede constancia de cada respuesta
    sin depender de que ningún agente tenga que guardarla explícitamente."""
    if not _informe_path:
        return
    from pathlib import Path

    ruta = Path(_informe_path)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("a", encoding="utf-8") as f:
        f.write(f"P: {pregunta}\nR: {respuesta}\n\n")


@tool("preguntar_al_autor")
def ask_human_tool(pregunta: str) -> str:
    """
    Usa esta herramienta cuando necesites hacerle una pregunta directa al autor del artículo.
    Recibe como parámetro la pregunta que quieres hacer, y devuelve la respuesta del autor.
    """
    fallo_no_inventar = (
        "[FALLO DE HERRAMIENTA: no se ha podido obtener una respuesta real del autor. "
        "Esto NO es una respuesta del autor: no la interpretes como tal ni inventes o "
        "supongas ningún dato para rellenar este punto. Informa explícitamente de que "
        "la entrevista se ha interrumpido en esta pregunta y detente aquí.]"
    )
    if _q_questions is not None:
        _q_questions.put(pregunta)
        try:
            respuesta = _q_answers.get(timeout=600)
        except _queue_module.Empty:
            respuesta = fallo_no_inventar
    else:
        print(f"\n[El Agente te pregunta]: {pregunta}")
        try:
            respuesta = input("Tu respuesta: ")
        except EOFError:
            respuesta = fallo_no_inventar
    _registrar_pregunta_respuesta(pregunta, respuesta)
    return respuesta


@tool("leer_pdf")
def read_pdf_tool(ruta_pdf: str) -> str:
    """
    Lee y extrae el texto completo de un fichero PDF.
    Recibe la ruta absoluta o relativa al fichero PDF y devuelve todo su contenido en texto plano.
    Úsala para obtener el contenido del artículo científico antes de extraer los puntos clave.
    """
    import pdfplumber
    paginas = []
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text(x_tolerance=1)
            if texto:
                paginas.append(texto)
    return "\n\n".join(paginas)


@tool("leer_pdfs_carpeta")
def read_pdfs_folder_tool(ruta_carpeta: str) -> str:
    """
    Lee y extrae el texto completo de todos los ficheros PDF que haya en una carpeta.
    Recibe la ruta a la carpeta (por ejemplo, la que contiene los papers citados en la introducción de un artículo)
    y devuelve el texto de cada PDF, separado y precedido por el nombre de su fichero.
    Úsala para obtener el contenido de los trabajos relacionados antes de redactar la introducción.
    """
    import pdfplumber
    from pathlib import Path

    carpeta = Path(ruta_carpeta)
    if not carpeta.is_dir():
        return f"La carpeta '{ruta_carpeta}' no existe o no contiene papers citados."

    ficheros = sorted(carpeta.glob("*.pdf"))
    if not ficheros:
        return f"La carpeta '{ruta_carpeta}' no contiene ningún PDF."

    bloques = []
    for fichero in ficheros:
        paginas = []
        with pdfplumber.open(fichero) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text(x_tolerance=1)
                if texto:
                    paginas.append(texto)
        bloques.append(f"### Paper citado: {fichero.name}\n\n" + "\n\n".join(paginas))

    return "\n\n---\n\n".join(bloques)


@tool("leer_informe_actual")
def read_informe_tool(ruta_informe: str) -> str:
    """
    Lee el informe de la entrevista tal como está guardado ahora mismo en disco.
    Recibe la ruta al fichero del informe y devuelve su contenido en texto plano.
    Úsala antes de volver a preguntar nada al autor, para comprobar tú mismo qué
    puntos ya están respondidos y cuáles faltan de verdad, en vez de fiarte de
    lo que te haya resumido otro agente.
    """
    from pathlib import Path

    ruta = Path(ruta_informe)
    if not ruta.is_file():
        return f"Todavía no existe ningún informe guardado en '{ruta_informe}'."
    return ruta.read_text(encoding="utf-8")
