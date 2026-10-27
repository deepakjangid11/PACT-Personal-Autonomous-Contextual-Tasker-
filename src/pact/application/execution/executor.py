from abc import ABC, abstractmethod
from uuid import UUID

from pact.domain.result import TaskResult
from pact.domain.task import Task


class TaskExecutor(ABC):
    @abstractmethod
    def execute(
        self,
        task: Task,
        tasks: dict[UUID, Task] | None = None,
    ) -> TaskResult:
        """Execute a task and return its result."""
