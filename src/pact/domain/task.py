from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4


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
    completed_at: datetime | None = None

    def start(self) -> None:
        self.status = TaskStatus.RUNNING
    
    def complete(self) -> None:
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now(UTC)

    def cancel(self) -> None:
        self.status = TaskStatus.CANCELLED