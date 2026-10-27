from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

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

    def start(self) -> None:
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now(UTC)

    def complete(self) -> None:
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def cancel(self) -> None:
        self.status = TaskStatus.CANCELLED