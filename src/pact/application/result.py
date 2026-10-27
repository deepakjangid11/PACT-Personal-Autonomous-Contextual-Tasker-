from dataclasses import dataclass

from pact.domain.result import TaskResult


@dataclass(slots=True)
class TaskExecutionResult:
    task_result: TaskResult
    task_id: str
