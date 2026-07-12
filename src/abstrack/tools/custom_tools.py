import queue as _queue_module
from crewai.tools import tool

# When running in web mode these are set to Queue objects before starting the pipeline thread.
# In CLI mode they stay None and the tool falls back to input().
_q_questions = None
_q_answers = None


def set_web_queues(q_questions, q_answers):
    global _q_questions, _q_answers
    _q_questions = q_questions
    _q_answers = q_answers


def clear_web_queues():
    global _q_questions, _q_answers
    _q_questions = None
    _q_answers = None


@tool("preguntar_al_autor")
def ask_human_tool(pregunta: str) -> str:
    """
    Usa esta herramienta cuando necesites hacerle una pregunta directa al autor del artículo.
    Recibe como parámetro la pregunta que quieres hacer, y devuelve la respuesta del autor.
    """
    if _q_questions is not None:
        _q_questions.put(pregunta)
        try:
            return _q_answers.get(timeout=600)
        except _queue_module.Empty:
            return "Sin respuesta (tiempo agotado)."
    print(f"\n[El Agente te pregunta]: {pregunta}")
    return input("Tu respuesta: ")


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
