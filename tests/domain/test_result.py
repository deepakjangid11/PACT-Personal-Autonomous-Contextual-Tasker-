from pact.domain.result import TaskResult


def test_successful_task_result() -> None:
    result = TaskResult(
        success=True,
        output="Chrome opened successfully",
    )

    assert result.success is True
    assert result.output == "Chrome opened successfully"
    assert result.error is None


def test_failed_task_result() -> None:
    result = TaskResult(
        success=False,
        error="Chrome could not be opened",
    )

    assert result.success is False
    assert result.output is None
    assert result.error == "Chrome could not be opened"