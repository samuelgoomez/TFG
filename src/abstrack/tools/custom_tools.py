from crewai.tools import tool

@tool("Preguntar al Autor")
def ask_human_tool(pregunta: str) -> str:
    """
    Usa esta herramienta cuando necesites hacerle una pregunta directa al autor del artículo.
    Recibe como parámetro la pregunta que quieres hacer, y devuelve la respuesta del autor.
    """
    print(f"\n🤖 [El Agente te pregunta]: {pregunta}")
    respuesta = input("Tu respuesta: ")
    return respuesta
