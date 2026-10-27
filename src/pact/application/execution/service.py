from time import perf_counter
from uuid import UUID

from pact.application.execution.executor import TaskExecutor
from pact.application.execution.step_executor import StepExecutor
from pact.domain.result import TaskResult
from pact.domain.task import Task


class TaskExecutionService(TaskExecutor):
    def __init__(self, step_executor: StepExecutor) -> None:
        self.step_executor = step_executor

    def execute(
        self,
        task: Task,
        tasks: dict[UUID, Task] | None = None,
    ) -> TaskResult:
        start_time = perf_counter()

        try:
            task.start(tasks)

            for step in task.steps:
                result = self.step_executor.execute(step)

                if not result.success:
                    if task.status.value == "running":
                        task.fail()

                    return TaskResult(
                        success=False,
                        error=result.error,
                        duration_ms=(perf_counter() - start_time) * 1000,
                    )

            task.complete()

            return TaskResult(
                success=True,
                output=f"Task '{task.description}' completed successfully",
                duration_ms=(perf_counter() - start_time) * 1000,
            )

        except Exception as exc:
            if task.status.value == "running":
                task.fail()

            return TaskResult(
                success=False,
                error=str(exc),
                duration_ms=(perf_counter() - start_time) * 1000,
            )
