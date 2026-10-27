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


def test_task_can_start() -> None:
    task = Task(description="Open Chrome")

    task.start()

    assert task.status == TaskStatus.RUNNING


def test_task_can_be_completed() -> None:
    task = Task(description="Open Chrome")

    task.start()
    task.complete()

    assert task.status == TaskStatus.COMPLETED
    assert task.completed_at is not None


def test_task_can_be_cancelled() -> None:
    task = Task(description="Open Chrome")

    task.cancel()

    assert task.status == TaskStatus.CANCELLED


def test_task_priority_can_change() -> None:
    task = Task(description="Open Chrome")

    task.priority = TaskPriority.HIGH

    assert task.priority == TaskPriority.HIGH