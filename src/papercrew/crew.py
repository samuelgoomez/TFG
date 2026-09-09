# Autor: Samuel Gómez Grande
import os
import re
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Crew, Process, Task, LLM
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from typing import List
from papercrew.tools.custom_tools import (
    ask_human_tool,
    read_pdf_tool,
    read_pdfs_folder_tool,
    read_informe_tool,
)


# El validador a veces da por buena una vaguedad tipo "alta tasa de aciertos" como si
# fuera un dato numérico. Este guardrail lo comprueba por código en vez de fiarse de él.
def _resultados_tienen_dato_numerico(texto):
    """Busca la sección de Resultados en `texto` y dice si contiene una cifra.
    Devuelve None si no encuentra la sección (no concluyente), True/False si sí."""
    match = re.search(
        r"(?:\d\.\s*)?Resultados\s*:?\s*\n?(.*?)(?=\n\s*(?:\d\.\s*)?(?:Conclusi[oó]n|Restricciones)\b|\Z)",
        texto,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    seccion = match.group(1)
    return bool(re.search(r"\d", seccion) or "[SIN DATO NUMÉRICO]" in seccion.upper())


def _verificar_resultados_con_dato_numerico(salida):
    texto = salida.raw if hasattr(salida, "raw") else str(salida)
    encontrado = _resultados_tienen_dato_numerico(texto)
    if encontrado is None or encontrado is True:
        # No se encontró la sección con el formato esperado (no forzamos el rechazo para
        # no romper el pipeline por un simple cambio de formato), o sí tiene un dato real.
        return (True, salida)

    # El validador sí trae un apartado de Resultados en su reformulación, pero sin
    # ninguna cifra visible. Antes de rechazar, se comprueba el informe real en disco:
    # el validador tiende a parafrasear al reescribirlo y puede perder la cifra aunque
    # el autor sí la haya dado (el fichero refleja literalmente lo que dijo).
    from pathlib import Path
    ruta_informe = Path("papers/salida/informe_entrevista.md")
    if ruta_informe.is_file():
        if _resultados_tienen_dato_numerico(ruta_informe.read_text(encoding="utf-8")):
            return (True, salida)

    return (
        False,
        "El punto de Resultados no tiene ningún dato concreto y medible (cifra, porcentaje, "
        "comparación numérica). Delega de nuevo en el Agente de Adquisición de Información para "
        "conseguir un dato numérico real. Si el autor insiste en que no dispone de ninguna cifra, "
        "no te la inventes ni cambies de tema o de estudio: usa el marcador \"[SIN DATO NUMÉRICO]\" "
        "tal como indica la descripción de esta tarea.",
    )

@CrewBase
class PaperCrew():
    """PaperCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Ruta al PDF; si es None, el sistema usa el modo interactivo (preguntas al autor)
    pdf_path: str = None

    # Carpeta con los PDFs citados (solo modo introducción + PDF)
    citas_path: str = ""

    # Tipo de contenido a generar: "abstract" (por defecto) o "introduccion"
    tipo: str = "abstract"

    # Idioma de redacción del texto generado (lo elige el usuario, no lo decide el LLM)
    idioma: str = "Español"

    # Callback opcional: se llama con un TaskOutput cada vez que una tarea termina
    task_callback: object = None

    @property
    def llm(self) -> LLM:
        return LLM(
            model=os.getenv("MODEL"),
        )

    # ── Agente coordinador (común a ambos modos) ──────────────────────────────
    def agente_coordinador(self) -> Agent:
        config_key = 'agente_coordinador_intro' if self.tipo == "introduccion" else 'agente_coordinador'
        return Agent(
            config=self.agents_config[config_key],
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )

    # ── Agentes modo interactivo ──────────────────────────────────────────────
    @agent
    def agente_de_adquisicion_de_informacion(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_de_adquisicion_de_informacion'],
            llm=self.llm,
            tools=[ask_human_tool, read_informe_tool],
            verbose=True
        )

    # ── Agente modo PDF ────────────────────────────────────────────────────────
    @agent
    def agente_de_adquisicion_pdf(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_de_adquisicion_pdf'],
            llm=self.llm,
            tools=[read_pdf_tool, read_pdfs_folder_tool],
            verbose=True
        )

    # ── Agentes compartidos ───────────────────────────────────────────────────
    @agent
    def agente_de_validacion_de_completitud(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_de_validacion_de_completitud'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def agente_de_estructuracion_de_contenido(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_de_estructuracion_de_contenido'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def agente_redactor(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_redactor'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def agente_de_revision_de_estilo(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_de_revision_de_estilo'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def agente_de_control_de_calidad(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_de_control_de_calidad'],
            llm=self.llm,
            verbose=True
        )

    # ── Agentes modo introducción (especialistas CARS + editor) ──────────────
    @agent
    def agente_especialista_territorio(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_especialista_territorio'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def agente_especialista_hueco(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_especialista_hueco'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def agente_especialista_idea(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_especialista_idea'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def agente_especialista_contribuciones(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_especialista_contribuciones'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def agente_especialista_evaluacion(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_especialista_evaluacion'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def agente_especialista_estructura_documento(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_especialista_estructura_documento'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def agente_editor_intro(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_editor_intro'],
            llm=self.llm,
            verbose=True
        )

    # ── Agente de maquetación bibliográfica (usado por bib_writer.py, fuera del pipeline) ──
    @agent
    def agente_bibliografico(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_bibliografico'],
            llm=self.llm,
            verbose=False
        )

    # ── Agente recortador (usado por bib_writer.py, fuera del pipeline) ──────
    @agent
    def agente_recortador(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_recortador'],
            llm=self.llm,
            verbose=False
        )

    # ── Tareas modo interactivo ───────────────────────────────────────────────
    @task
    def tarea_adquisicion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_adquisicion'],
        )

    # ── Tarea modo PDF (sin @task para que no entre en self.tasks) ────────────
    def tarea_adquisicion_pdf(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_adquisicion_pdf'],
        )

    # ── Tareas compartidas ────────────────────────────────────────────────────
    @task
    def tarea_validacion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_validacion'],
            guardrail=_verificar_resultados_con_dato_numerico,
        )

    # Variante sin bucle para modo PDF: acepta "No especificado" como válido.
    # Recibe la tarea de adquisición como contexto para que el validador tenga el informe extraído.
    def tarea_validacion_pdf(self, tarea_adquisicion: Task) -> Task:
        return Task(
            config=self.tasks_config['tarea_validacion_pdf'],
            context=[tarea_adquisicion],
        )

    @task
    def tarea_estructuracion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_estructuracion'],
            context=[self.tarea_validacion()],
        )

    @task
    def tarea_redaccion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_redaccion'],
            context=[self.tarea_validacion(), self.tarea_estructuracion()],
        )

    @task
    def tarea_revision(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_revision'],
            context=[self.tarea_redaccion()],
        )

    @task
    def tarea_control_calidad(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_control_calidad'],
            context=[self.tarea_validacion(), self.tarea_revision()],
        )

    # ── Tareas modo introducción ──────────────────────────────────────────────
    @task
    def tarea_adquisicion_intro(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_adquisicion_intro'],
        )

    @task
    def tarea_validacion_intro(self) -> Task:
        tarea_previa = self.tarea_adquisicion_pdf_intro() if self.pdf_path else self.tarea_adquisicion_intro()
        # En modo PDF los documentos son fijos: la variante sin bucle de re-lectura evita que el
        # coordinador re-delegue con el mismo input y quede atrapado en el guard de CrewAI hasta max_iter.
        config_key = 'tarea_validacion_pdf_intro' if self.pdf_path else 'tarea_validacion_intro'
        return Task(
            config=self.tasks_config[config_key],
            context=[tarea_previa],
        )

    @task
    def tarea_bloque_territorio(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_bloque_territorio'],
            context=[self.tarea_validacion_intro()],
        )

    @task
    def tarea_bloque_hueco(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_bloque_hueco'],
            context=[self.tarea_validacion_intro(), self.tarea_bloque_territorio()],
        )

    @task
    def tarea_bloque_idea(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_bloque_idea'],
            context=[self.tarea_validacion_intro(), self.tarea_bloque_hueco()],
        )

    @task
    def tarea_bloque_contribuciones(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_bloque_contribuciones'],
            context=[self.tarea_validacion_intro(), self.tarea_bloque_idea()],
        )

    @task
    def tarea_bloque_evaluacion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_bloque_evaluacion'],
            context=[self.tarea_validacion_intro()],
        )

    @task
    def tarea_bloque_estructura_documento(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_bloque_estructura_documento'],
            context=[self.tarea_validacion_intro()],
        )

    @task
    def tarea_fusion_intro(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_fusion_intro'],
            context=[
                self.tarea_validacion_intro(),
                self.tarea_bloque_territorio(),
                self.tarea_bloque_hueco(),
                self.tarea_bloque_idea(),
                self.tarea_bloque_contribuciones(),
                self.tarea_bloque_evaluacion(),
                self.tarea_bloque_estructura_documento(),
            ],
        )

    @task
    def tarea_control_calidad_intro(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_control_calidad_intro'],
            context=[self.tarea_fusion_intro()],
        )

    # ── Tarea modo PDF para introducción (sin @task para que no entre en self.tasks) ──
    def tarea_adquisicion_pdf_intro(self) -> Task:
        if not hasattr(self, '_tarea_adquisicion_pdf_intro_cache'):
            self._tarea_adquisicion_pdf_intro_cache = Task(
                config=self.tasks_config['tarea_adquisicion_pdf_intro'],
            )
        return self._tarea_adquisicion_pdf_intro_cache

    # ── Crew ──────────────────────────────────────────────────────────────────
    @crew
    def crew(self) -> Crew:
        """Creates the PaperCrew crew"""

        agentes_interactivo = [
            self.agente_de_adquisicion_de_informacion(),
            self.agente_de_validacion_de_completitud(),
            self.agente_de_estructuracion_de_contenido(),
            self.agente_redactor(),
            self.agente_de_revision_de_estilo(),
            self.agente_de_control_de_calidad(),
        ]

        # pdf_path se inyecta aquí y no en el método factory porque @agent cachea la instancia
        # antes de que self.pdf_path esté asignado; se parchea .goal sobre la instancia ya creada.
        agente_pdf = self.agente_de_adquisicion_pdf()
        if self.pdf_path:
            prefijo = (
                f"INSTRUCCIÓN PRIORITARIA (anula cualquier otra indicación sobre la ruta):\n"
                f"La ruta del PDF para esta sesión es: {self.pdf_path}\n"
                f"Llama a 'leer_pdf' con esa ruta exacta de forma inmediata, sin pedir confirmación al coordinador.\n\n"
            )
            sufijo = (
                f"\n\nRECORDATORIO FINAL: usa siempre '{self.pdf_path}' como ruta del PDF. "
                "No preguntes por la ruta; ya la tienes arriba."
            )
            if self.citas_path:
                sufijo += (
                    f"\nPara los papers citados usa 'leer_pdfs_carpeta' con la ruta '{self.citas_path}'."
                )
            if not agente_pdf.goal.startswith("INSTRUCCIÓN PRIORITARIA"):
                agente_pdf.goal = prefijo + agente_pdf.goal + sufijo

        agentes_pdf = [
            agente_pdf,
            self.agente_de_validacion_de_completitud(),
            self.agente_de_estructuracion_de_contenido(),
            self.agente_redactor(),
            self.agente_de_revision_de_estilo(),
            self.agente_de_control_de_calidad(),
        ]

        # ── Equipo CARS para la introducción (común a entrevista y PDF) ───────
        agentes_intro_comunes = [
            self.agente_de_validacion_de_completitud(),
            self.agente_especialista_territorio(),
            self.agente_especialista_hueco(),
            self.agente_especialista_idea(),
            self.agente_especialista_contribuciones(),
            self.agente_especialista_evaluacion(),
            self.agente_especialista_estructura_documento(),
            self.agente_editor_intro(),
            self.agente_de_control_de_calidad(),
        ]

        agentes_intro_interactivo = [self.agente_de_adquisicion_de_informacion()] + agentes_intro_comunes
        agentes_intro_pdf = [agente_pdf] + agentes_intro_comunes

        tareas_cars_intro = [
            self.tarea_validacion_intro(),
            self.tarea_bloque_territorio(),
            self.tarea_bloque_hueco(),
            self.tarea_bloque_idea(),
            self.tarea_bloque_contribuciones(),
            self.tarea_bloque_evaluacion(),
            self.tarea_bloque_estructura_documento(),
            self.tarea_fusion_intro(),
            self.tarea_control_calidad_intro(),
        ]

        if self.pdf_path and self.tipo == "introduccion":
            agentes = agentes_intro_pdf
            tareas = [self.tarea_adquisicion_pdf_intro()] + tareas_cars_intro
        elif self.pdf_path:
            agentes = agentes_pdf
            tarea_adq_pdf = self.tarea_adquisicion_pdf()
            tareas = [tarea_adq_pdf,
                      self.tarea_validacion_pdf(tarea_adq_pdf),
                      self.tarea_estructuracion(),
                      self.tarea_redaccion(),
                      self.tarea_revision(),
                      self.tarea_control_calidad()]
        elif self.tipo == "introduccion":
            agentes = agentes_intro_interactivo
            tareas = [self.tarea_adquisicion_intro()] + tareas_cars_intro
        else:
            agentes = agentes_interactivo
            tareas = [self.tarea_adquisicion()] + [
                self.tarea_validacion(),
                self.tarea_estructuracion(),
                self.tarea_redaccion(),
                self.tarea_revision(),
                self.tarea_control_calidad(),
            ]

        crew_kwargs = dict(
            agents=agentes,
            tasks=tareas,
            process=Process.hierarchical,
            manager_agent=self.agente_coordinador(),
            verbose=True,
        )
        if self.task_callback:
            crew_kwargs["task_callback"] = self.task_callback
        return Crew(**crew_kwargs)
