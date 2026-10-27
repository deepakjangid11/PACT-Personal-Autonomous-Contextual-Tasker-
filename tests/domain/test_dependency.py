from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest

from pact.domain.dependency import TaskDependency


def test_task_dependency_creation() -> None:
    task_id = uuid4()
    dependency_id = uuid4()

    dependency = TaskDependency(
        task_id=task_id,
        depends_on_task_id=dependency_id,
    )

    assert dependency.task_id == task_id
    assert dependency.depends_on_task_id == dependency_id


def test_task_dependency_rejects_self_dependency() -> None:
    task_id = uuid4()

    with pytest.raises(ValueError, match="A task cannot depend on itself"):
        TaskDependency(
            task_id=task_id,
            depends_on_task_id=task_id,
        )


def test_task_dependency_is_immutable() -> None:
    task_id = uuid4()
    dependency_id = uuid4()

    dependency = TaskDependency(
        task_id=task_id,
        depends_on_task_id=dependency_id,
    )

    with pytest.raises(FrozenInstanceError):
        dependency.task_id = uuid4()  # type: ignore[misc]
