"""
Base Agent

Foundation for future Agentic AI.
"""

from abc import ABC
from abc import abstractmethod


class BaseAgent(ABC):
    """
    Base class for all AI BDOS agents.

    Every agent is responsible for thinking,
    planning, and executing a specific task.
    """

    # ------------------------------------------------------------------
    # Agent Metadata
    # ------------------------------------------------------------------

    name: str = "BaseAgent"
    version: str = "1.0.0"
    description: str = ""

    @property
    def agent_type(self) -> str:
        """
        Returns the concrete agent type.
        """
        return self.__class__.__name__

    # ------------------------------------------------------------------
    # Agent Lifecycle
    # ------------------------------------------------------------------

    @abstractmethod
    def think(self, context):
        """
        Analyze the current context.
        """
        raise NotImplementedError

    @abstractmethod
    def plan(self, context):
        """
        Create an execution plan.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, context):
        """
        Execute the planned actions.
        """
        raise NotImplementedError