from uuid import UUID, uuid4

import pytest

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
    assert task.dependencies == []


def test_task_rejects_empty_description() -> None:
    with pytest.raises(ValueError, match="Task description cannot be empty"):
        Task(description="")


def test_task_rejects_whitespace_description() -> None:
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
    assert task.completed_at is not None


def test_task_can_fail() -> None:
    task = Task(description="Open Chrome")

    task.start()
    task.fail()

    assert task.status == TaskStatus.FAILED
    assert task.completed_at is not None


def test_task_cannot_start_after_completed() -> None:
    task = Task(description="Open Chrome")

    task.start()
    task.complete()

    with pytest.raises(
        ValueError,
        match="Cannot start task from completed state",
    ):
        task.start()


def test_task_cannot_complete_from_pending() -> None:
    task = Task(description="Open Chrome")

    with pytest.raises(
        ValueError,
        match="Cannot complete task from pending state",
    ):
        task.complete()


def test_task_cannot_fail_from_pending() -> None:
    task = Task(description="Open Chrome")

    with pytest.raises(
        ValueError,
        match="Cannot fail task from pending state",
    ):
        task.fail()


def test_task_cannot_cancel_after_completed() -> None:
    task = Task(description="Open Chrome")

    task.start()
    task.complete()

    with pytest.raises(
        ValueError,
        match="Cannot cancel task from completed state",
    ):
        task.cancel()


def test_task_cannot_complete_after_cancelled() -> None:
    task = Task(description="Open Chrome")

    task.cancel()

    with pytest.raises(
        ValueError,
        match="Cannot complete task from cancelled state",
    ):
        task.complete()


def test_task_cannot_complete_after_failed() -> None:
    task = Task(description="Open Chrome")

    task.start()
    task.fail()

    with pytest.raises(
        ValueError,
        match="Cannot complete task from failed state",
    ):
        task.complete()


def test_task_priority_can_change() -> None:
    task = Task(description="Open Chrome")

    task.priority = TaskPriority.HIGH

    assert task.priority == TaskPriority.HIGH


def test_task_has_no_dependencies_by_default() -> None:
    task = Task(description="Install Python")

    assert task.dependencies == []


def test_task_can_add_dependency() -> None:
    task = Task(description="Create virtual environment")
    dependency_task_id = uuid4()

    dependency = task.add_dependency(dependency_task_id)

    assert len(task.dependencies) == 1
    assert dependency.task_id == task.id
    assert dependency.depends_on_task_id == dependency_task_id


def test_task_can_add_multiple_dependencies() -> None:
    task = Task(description="Install project dependencies")
    first_task_id = uuid4()
    second_task_id = uuid4()

    first_dependency = task.add_dependency(first_task_id)
    second_dependency = task.add_dependency(second_task_id)

    assert task.dependencies == [first_dependency, second_dependency]
    assert len(task.dependencies) == 2


def test_task_with_no_dependencies_can_start() -> None:
    task = Task(description="Open Chrome")

    assert task.can_start({})


def test_task_can_start_when_all_dependencies_are_completed() -> None:
    dependency_task = Task(description="Install Python")

    dependency_task.start()
    dependency_task.complete()

    task = Task(description="Create virtual environment")
    task.add_dependency(dependency_task.id)

    tasks = {
        dependency_task.id: dependency_task,
        task.id: task,
    }

    assert task.can_start(tasks)


def test_task_cannot_start_when_dependency_is_pending() -> None:
    dependency_task = Task(description="Install Python")

    task = Task(description="Create virtual environment")
    task.add_dependency(dependency_task.id)

    tasks = {
        dependency_task.id: dependency_task,
        task.id: task,
    }

    assert not task.can_start(tasks)


def test_task_cannot_start_when_dependency_failed() -> None:
    dependency_task = Task(description="Install Python")

    dependency_task.start()
    dependency_task.fail()

    task = Task(description="Create virtual environment")
    task.add_dependency(dependency_task.id)

    tasks = {
        dependency_task.id: dependency_task,
        task.id: task,
    }

    assert not task.can_start(tasks)


def test_task_cannot_start_when_dependency_cancelled() -> None:
    dependency_task = Task(description="Install Python")

    dependency_task.cancel()

    task = Task(description="Create virtual environment")
    task.add_dependency(dependency_task.id)

    tasks = {
        dependency_task.id: dependency_task,
        task.id: task,
    }

    assert not task.can_start(tasks)


def test_task_can_start_after_dependency_is_completed() -> None:
    dependency_task = Task(description="Install Python")
    task = Task(description="Create virtual environment")

    task.add_dependency(dependency_task.id)

    tasks = {
        dependency_task.id: dependency_task,
        task.id: task,
    }

    with pytest.raises(
        ValueError,
        match="Cannot start task because dependencies are not completed",
    ):
        task.start(tasks)

    dependency_task.start()
    dependency_task.complete()

    task.start(tasks)

    assert task.status == TaskStatus.RUNNING
    assert task.started_at is not None


def test_task_with_dependencies_requires_dependency_context() -> None:
    dependency_task = Task(description="Install Python")
    task = Task(description="Create virtual environment")

    task.add_dependency(dependency_task.id)

    with pytest.raises(
        ValueError,
        match="Task dependencies must be provided before starting",
    ):
        task.start()


def test_task_rejects_missing_dependency() -> None:
    dependency_id = uuid4()

    task = Task(description="Create virtual environment")
    task.add_dependency(dependency_id)

    with pytest.raises(
        ValueError,
        match=f"Dependency task {dependency_id} not found",
    ):
        task.can_start({})
