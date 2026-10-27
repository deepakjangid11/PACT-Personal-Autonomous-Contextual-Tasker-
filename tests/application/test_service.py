from pact.application.execution.service import TaskExecutionService
from pact.application.execution.step_executor import StepExecutor
from pact.domain.result import TaskResult
from pact.domain.step import TaskStep
from pact.domain.task import Task, TaskStatus


class FakeStepExecutor(StepExecutor):
    def execute(self, step: TaskStep) -> TaskResult:
        step.start()
        step.complete()

        return TaskResult(
            success=True,
            output=f"Step '{step.description}' completed successfully",
        )


class FailingStepExecutor(StepExecutor):
    def execute(self, step: TaskStep) -> TaskResult:
        step.start()
        step.fail()

        return TaskResult(
            success=False,
            error=f"Step '{step.description}' failed",
        )


def test_execute_task_successfully() -> None:
    task = Task(description="Test task")
    task.add_step("First step")
    task.add_step("Second step")

    service = TaskExecutionService(FakeStepExecutor())

    result = service.execute(task)

    assert result.success is True
    assert result.duration_ms is not None
    assert result.duration_ms >= 0
    assert task.status == TaskStatus.COMPLETED
    assert all(step.status.value == "completed" for step in task.steps)
    assert result.output == "Task 'Test task' completed successfully"


def test_execute_task_with_completed_dependency() -> None:
    dependency_task = Task(description="Dependency task")
    dependency_task.start()
    dependency_task.complete()

    task = Task(description="Dependent task")
    task.add_dependency(dependency_task.id)
    task.add_step("Dependent step")

    service = TaskExecutionService(FakeStepExecutor())

    tasks = {
        dependency_task.id: dependency_task,
        task.id: task,
    }

    result = service.execute(task, tasks)

    assert result.success is True
    assert result.duration_ms is not None
    assert result.duration_ms >= 0
    assert task.status == TaskStatus.COMPLETED


def test_execute_task_fails_when_dependency_is_not_completed() -> None:
    dependency_task = Task(description="Dependency task")

    task = Task(description="Dependent task")
    task.add_dependency(dependency_task.id)
    task.add_step("Dependent step")

    service = TaskExecutionService(FakeStepExecutor())

    tasks = {
        dependency_task.id: dependency_task,
        task.id: task,
    }

    result = service.execute(task, tasks)

    assert result.success is False
    assert result.duration_ms is not None
    assert result.duration_ms >= 0
    assert task.status == TaskStatus.PENDING
    assert result.error is not None
    assert "Cannot start task" in result.error


def test_execute_task_fails_when_step_execution_fails() -> None:
    task = Task(description="Failing task")
    task.add_step("Failing step")

    service = TaskExecutionService(FailingStepExecutor())

    result = service.execute(task)

    assert result.success is False
    assert result.duration_ms is not None
    assert result.duration_ms >= 0
    assert task.status == TaskStatus.FAILED
    assert task.steps[0].status.value == "failed"
    assert result.error is not None
    assert result.error == "Step 'Failing step' failed"
