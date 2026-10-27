from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class TaskDependency:
    task_id: UUID
    depends_on_task_id: UUID

    def __post_init__(self) -> None:
        if self.task_id == self.depends_on_task_id:
            raise ValueError("A task cannot depend on itself")
