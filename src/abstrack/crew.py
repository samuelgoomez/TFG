# Autor: Samuel Gómez
import os
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Crew, Process, Task, LLM
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from typing import List
from abstrack.tools.custom_tools import ask_human_tool, read_pdf_tool, read_pdfs_folder_tool

@CrewBase
class Abstrack():
    """Abstrack crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Ruta al PDF; si es None, el sistema usa el modo interactivo (preguntas al autor)
    pdf_path: str = None

    # Carpeta con los PDFs citados (solo modo introducción + PDF)
    citas_path: str = ""

    # Tipo de contenido a generar: "abstract" (por defecto) o "introduccion"
    tipo: str = "abstract"

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
            tools=[ask_human_tool],
            verbose=True
        )

    # ── Agente modo PDF ────────────────────────────────────────────────────────
    @agent
    def agente_de_adquisicion_pdf(self) -> Agent:
        config = dict(self.agents_config['agente_de_adquisicion_pdf'])
        if self.pdf_path:
            extra = (
                f"\n    RUTA OBLIGATORIA DEL PAPER PRINCIPAL: {self.pdf_path}\n"
                "    Llama a 'leer_pdf' con exactamente esa ruta. No uses ninguna otra."
            )
            if self.citas_path:
                extra += (
                    f"\n    CARPETA DE PAPERS CITADOS: {self.citas_path}\n"
                    "    Llama a 'leer_pdfs_carpeta' con exactamente esa ruta para leer los papers citados."
                )
            config['goal'] = config['goal'] + extra
        return Agent(
            config=config,
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
        )

    @task
    def tarea_estructuracion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_estructuracion'],
        )

    @task
    def tarea_redaccion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_redaccion'],
        )

    @task
    def tarea_revision(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_revision'],
        )

    @task
    def tarea_control_calidad(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_control_calidad'],
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
        return Task(
            config=self.tasks_config['tarea_validacion_intro'],
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
        """Creates the Abstrack crew"""

        agentes_interactivo = [
            self.agente_de_adquisicion_de_informacion(),
            self.agente_de_validacion_de_completitud(),
            self.agente_de_estructuracion_de_contenido(),
            self.agente_redactor(),
            self.agente_de_revision_de_estilo(),
            self.agente_de_control_de_calidad(),
        ]

        agentes_pdf = [
            self.agente_de_adquisicion_pdf(),
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
        agentes_intro_pdf = [self.agente_de_adquisicion_pdf()] + agentes_intro_comunes

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
            tareas = [self.tarea_adquisicion_pdf()] + [
                self.tarea_validacion(),
                self.tarea_estructuracion(),
                self.tarea_redaccion(),
                self.tarea_revision(),
                self.tarea_control_calidad(),
            ]
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
