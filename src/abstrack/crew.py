# Autor: Samuel Gómez
import os
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Crew, Process, Task, LLM
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from typing import List
from abstrack.tools.custom_tools import ask_human_tool, read_pdf_tool

@CrewBase
class Abstrack():
    """Abstrack crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Ruta al PDF; si es None, el sistema usa el modo interactivo (preguntas al autor)
    pdf_path: str = None

    @property
    def llm(self) -> LLM:
        return LLM(
            model=os.getenv("MODEL"),
            verbose=True
        )

    # ── Agente coordinador (común a ambos modos) ──────────────────────────────
    def agente_coordinador(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_coordinador'],
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

    # ── Agente modo PDF (sin @agent para que no entre en self.agents) ─────────
    def agente_de_adquisicion_pdf(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_de_adquisicion_pdf'],
            llm=self.llm,
            tools=[read_pdf_tool],
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

    # ── Crew ──────────────────────────────────────────────────────────────────
    @crew
    def crew(self) -> Crew:
        """Creates the Abstrack crew"""

        tareas_compartidas = [
            self.tarea_validacion(),
            self.tarea_estructuracion(),
            self.tarea_redaccion(),
            self.tarea_revision(),
            self.tarea_control_calidad(),
        ]

        if self.pdf_path:
            agentes = [
                self.agente_de_adquisicion_pdf(),
                self.agente_de_validacion_de_completitud(),
                self.agente_de_estructuracion_de_contenido(),
                self.agente_redactor(),
                self.agente_de_revision_de_estilo(),
                self.agente_de_control_de_calidad(),
            ]
            tareas = [self.tarea_adquisicion_pdf()] + tareas_compartidas
        else:
            agentes = self.agents   # auto-recopilados por @agent
            tareas = [self.tarea_adquisicion()] + tareas_compartidas

        return Crew(
            agents=agentes,
            tasks=tareas,
            process=Process.hierarchical,
            manager_agent=self.agente_coordinador(),
            verbose=True,
        )
