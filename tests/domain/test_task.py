from uuid import UUID

from pact.domain.task import Task, TaskPriority, TaskStatus


def test_task_creation() -> None:
    task = Task(description="Open Chrome")

    assert task.description == "Open Chrome"
    assert task.status == TaskStatus.PENDING
    assert task.priority == TaskPriority.MEDIUM
    assert isinstance(task.id, UUID)
    assert task.created_at is not None
    assert task.completed_at is None


def test_task_status_can_change() -> None:
    task = Task(description="Open Chrome")

    task.status = TaskStatus.RUNNING

    assert task.status == TaskStatus.RUNNING


def test_task_priority_can_change() -> None:
    task = Task(description="Open Chrome")

    task.priority = TaskPriority.HIGH

    assert task.priority == TaskPriority.HIGH


def test_task_can_be_completed() -> None:
    task = Task(description="Open Chrome")

    task.status = TaskStatus.COMPLETED

    assert task.status == TaskStatus.COMPLETED


def test_task_can_be_cancelled() -> None:
    task = Task(description="Open Chrome")

    task.status = TaskStatus.CANCELLED

    assert task.status == TaskStatus.CANCELLED