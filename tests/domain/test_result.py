from pact.domain.result import TaskResult


def test_successful_task_result() -> None:
    result = TaskResult(
        success=True,
        output="Chrome opened successfully",
        duration_ms=245.6,
    )

    assert result.success is True
    assert result.output == "Chrome opened successfully"
    assert result.error is None
    assert result.duration_ms == 245.6


def test_failed_task_result() -> None:
    result = TaskResult(
        success=False,
        error="Chrome could not be opened",
        duration_ms=120.3,
    )

    assert result.success is False
    assert result.output is None
    assert result.error == "Chrome could not be opened"
    assert result.duration_ms == 120.3


def test_task_result_duration_is_optional() -> None:
    result = TaskResult(success=True)

    assert result.duration_ms is None
