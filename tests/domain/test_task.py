from uuid import UUID

from pact.domain.step import StepStatus
from pact.domain.task import Task, TaskPriority, TaskStatus


def test_task_creation() -> None:
    task = Task(description="Open Chrome")

    assert task.description == "Open Chrome"
    assert task.status == TaskStatus.PENDING
    assert task.priority == TaskPriority.MEDIUM
    assert isinstance(task.id, UUID)
    assert task.created_at is not None
    assert task.started_at is None
    assert task.completed_at is None
    assert task.steps == []


def test_task_rejects_empty_description() -> None:
    import pytest

    with pytest.raises(ValueError, match="Task description cannot be empty"):
        Task(description="")


def test_task_rejects_whitespace_description() -> None:
    import pytest

    with pytest.raises(ValueError, match="Task description cannot be empty"):
        Task(description="   ")


def test_task_can_add_step() -> None:
    task = Task(description="Search Python course")

    step = task.add_step("Open Chrome")

    assert len(task.steps) == 1
    assert step.description == "Open Chrome"
    assert step.order == 1
    assert step.status == StepStatus.PENDING


def test_task_steps_are_ordered() -> None:
    task = Task(description="Search Python course")

    first_step = task.add_step("Open Chrome")
    second_step = task.add_step("Open Google")
    third_step = task.add_step("Search Python course")

    assert task.steps == [first_step, second_step, third_step]
    assert first_step.order == 1
    assert second_step.order == 2
    assert third_step.order == 3


def test_task_can_start() -> None:
    task = Task(description="Open Chrome")

    task.start()

    assert task.status == TaskStatus.RUNNING
    assert task.started_at is not None


def test_task_can_be_completed() -> None:
    task = Task(description="Open Chrome")

    task.start()
    task.complete()

    assert task.status == TaskStatus.COMPLETED
    assert task.started_at is not None
    assert task.completed_at is not None


def test_task_can_be_cancelled() -> None:
    task = Task(description="Open Chrome")

    task.cancel()

    assert task.status == TaskStatus.CANCELLED


def test_task_priority_can_change() -> None:
    task = Task(description="Open Chrome")

    task.priority = TaskPriority.HIGH

    assert task.priority == TaskPriority.HIGH