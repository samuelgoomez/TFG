from crewai.tools import tool

@tool("preguntar_al_autor")
def ask_human_tool(pregunta: str) -> str:
    """
    Usa esta herramienta cuando necesites hacerle una pregunta directa al autor del artículo.
    Recibe como parámetro la pregunta que quieres hacer, y devuelve la respuesta del autor.
    """
    print(f"\n[El Agente te pregunta]: {pregunta}")
    respuesta = input("Tu respuesta: ")
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
            texto = pagina.extract_text()
            if texto:
                paginas.append(texto)
    return "\n\n".join(paginas)
