from abc import ABC, abstractmethod

from pact.domain.result import TaskResult
from pact.domain.step import TaskStep


class StepExecutor(ABC):
    @abstractmethod
    def execute(self, step: TaskStep) -> TaskResult:
        """Execute a task step and return its result."""
