from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4


class StepStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class TaskStep:
    description: str
    order: int
    id: UUID = field(default_factory=uuid4)
    status: StepStatus = StepStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.description.strip():
            raise ValueError("Step description cannot be empty")

        if self.order < 1:
            raise ValueError("Step order must be greater than zero")

    def start(self) -> None:
        self.status = StepStatus.RUNNING

    def complete(self) -> None:
        self.status = StepStatus.COMPLETED

    def fail(self) -> None:
        self.status = StepStatus.FAILED
