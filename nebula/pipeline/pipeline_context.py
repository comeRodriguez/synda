from pprint import pprint

from dataclasses import dataclass


@dataclass
class StepResult:
    step_type: str
    input_data: any
    output_data: any
    metadata: dict[str, any] = None


@dataclass
class PipelineContext:
    current_data: any
    history: list[StepResult]

    def add_step_result(self, step_type: str, input_data: any, output_data: any, metadata: dict[str, any] = None):
        step_result = StepResult(
            step_type=step_type,
            input_data=input_data,
            output_data=output_data,
            metadata=metadata or {}
        )
        self.history.append(step_result)
        self.current_data = output_data

        pprint(f"Step result from {step_type}: {step_result}")
