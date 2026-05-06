# Autor: Samuel Gómez
import os
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Crew, Process, Task, LLM
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from typing import List
from abstrack.tools.custom_tools import ask_human_tool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Abstrack():
    """Abstrack crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @property
    def llm(self) -> LLM:
        return LLM(
            model=os.getenv("MODEL"),
            verbose=True
        )

    def agente_coordinador(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_coordinador'],
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )
    @agent
    def agente_de_adquisicion_de_informacion(self) -> Agent:
        return Agent(
            config=self.agents_config['agente_de_adquisicion_de_informacion'],
            llm=self.llm,
            tools=[ask_human_tool],
            verbose=True
        )

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

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def tarea_adquisicion(self) -> Task:
        return Task(
            config=self.tasks_config['tarea_adquisicion'],
        )

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

    @crew
    def crew(self) -> Crew:
        """Creates the Abstrack crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.hierarchical,
            manager_agent=self.agente_coordinador(),
            verbose=True,
        )
