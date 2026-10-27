from uuid import UUID

import pytest

from pact.domain.step import StepStatus, TaskStep


def test_step_creation() -> None:
    step = TaskStep(
        description="Open Chrome",
        order=1,
    )

    assert step.description == "Open Chrome"
    assert step.order == 1
    assert isinstance(step.id, UUID)
    assert step.status == StepStatus.PENDING
    assert step.created_at is not None


def test_step_rejects_empty_description() -> None:
    with pytest.raises(ValueError, match="Step description cannot be empty"):
        TaskStep(description="", order=1)


def test_step_rejects_whitespace_description() -> None:
    with pytest.raises(ValueError, match="Step description cannot be empty"):
        TaskStep(description="   ", order=1)


def test_step_rejects_invalid_order() -> None:
    with pytest.raises(ValueError, match="Step order must be greater than zero"):
        TaskStep(description="Open Chrome", order=0)


def test_step_can_start() -> None:
    step = TaskStep(description="Open Chrome", order=1)

    step.start()

    assert step.status == StepStatus.RUNNING


def test_step_can_be_completed() -> None:
    step = TaskStep(description="Open Chrome", order=1)

    step.start()
    step.complete()

    assert step.status == StepStatus.COMPLETED


def test_step_can_fail() -> None:
    step = TaskStep(description="Open Chrome", order=1)

    step.start()
    step.fail()

    assert step.status == StepStatus.FAILED
