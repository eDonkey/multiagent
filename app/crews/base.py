from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from app.services.toolkit import Tools

try:
    from crewai import Agent, Crew, Process, Task, LLM
except Exception:  # pragma: no cover
    Agent = Crew = Process = Task = LLM = None  # type: ignore


@dataclass
class CrewResult:
    route: str
    message: str
    raw: Any | None = None


class BaseCrewRunner:
    route_name: str = "base"
    model: str = "claude-3-5-haiku-latest"
    goal: str = ""
    backstory: str = ""

    def __init__(self) -> None:
        self.tools = Tools()

    def fallback(self, message: str, context: list[dict[str, str]] | None = None) -> CrewResult:
        return CrewResult(route=self.route_name, message=f"[{self.route_name}] Recibido: {message}")

    def run(self, message: str, context: list[dict[str, str]] | None = None) -> CrewResult:
        if Agent is None or not os.getenv("ANTHROPIC_API_KEY"):
            return self.fallback(message, context)

        llm = LLM(model=self.model)
        agent = Agent(
            role=self.route_name,
            goal=self.goal,
            backstory=self.backstory,
            llm=llm,
            verbose=False,
            allow_delegation=False,
        )
        task = Task(
            description=self.build_task_description(message, context or []),
            expected_output="Respuesta final breve en español para WhatsApp.",
            agent=agent,
        )
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
        result = crew.kickoff()
        return CrewResult(route=self.route_name, message=str(result), raw=result)

    def build_task_description(self, message: str, context: list[dict[str, str]]) -> str:
        context_text = "\n".join(f"{m['role']}: {m['content']}" for m in context)
        return f"Contexto reciente:\n{context_text}\n\nMensaje actual:\n{message}"
