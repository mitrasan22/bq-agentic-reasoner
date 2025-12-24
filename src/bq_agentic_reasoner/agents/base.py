from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """
    Base class for all deterministic agents.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """
        Execute agent logic and return output.
        """
        raise NotImplementedError
