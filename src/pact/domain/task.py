from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pact.domain.dependency import TaskDependency
from pact.domain.step import TaskStep


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass(slots=True)
class Task:
    description: str
    id: UUID = field(default_factory=uuid4)
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = None
    completed_at: datetime | None = None
    steps: list[TaskStep] = field(default_factory=list)
    dependencies: list[TaskDependency] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.description.strip():
            raise ValueError("Task description cannot be empty")

    def add_step(self, description: str) -> TaskStep:
        step = TaskStep(
            description=description,
            order=len(self.steps) + 1,
        )
        self.steps.append(step)
        return step

    def add_dependency(self, depends_on_task_id: UUID) -> TaskDependency:
        dependency = TaskDependency(
            task_id=self.id,
            depends_on_task_id=depends_on_task_id,
        )
        self.dependencies.append(dependency)
        return dependency

    def can_start(self, tasks: dict[UUID, "Task"]) -> bool:
        for dependency in self.dependencies:
            dependency_task = tasks.get(dependency.depends_on_task_id)

            if dependency_task is None:
                raise ValueError(
                    f"Dependency task {dependency.depends_on_task_id} not found"
                )

            if dependency_task.status != TaskStatus.COMPLETED:
                return False

        return True

    def start(self, tasks: dict[UUID, "Task"] | None = None) -> None:
        if self.status != TaskStatus.PENDING:
            raise ValueError(f"Cannot start task from {self.status.value} state")

        if self.dependencies:
            if tasks is None:
                raise ValueError("Task dependencies must be provided before starting")

            if not self.can_start(tasks):
                raise ValueError(
                    "Cannot start task because dependencies are not completed"
                )

        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now(UTC)

    def complete(self) -> None:
        if self.status != TaskStatus.RUNNING:
            raise ValueError(f"Cannot complete task from {self.status.value} state")

        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def fail(self) -> None:
        if self.status != TaskStatus.RUNNING:
            raise ValueError(f"Cannot fail task from {self.status.value} state")

        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now(UTC)

    def cancel(self) -> None:
        if self.status not in (TaskStatus.PENDING, TaskStatus.RUNNING):
            raise ValueError(f"Cannot cancel task from {self.status.value} state")

        self.status = TaskStatus.CANCELLED
        self.completed_at = datetime.now(UTC)
