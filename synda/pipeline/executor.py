from abc import abstractmethod

from synda.model.step import Step, StepStatus
from synda.model.node import Node


class Executor:
    def __init__(self, step_model: Step):
        self.step_model = step_model
        self.config = step_model.get_step_config()

    def execute_and_update_step(self, input_nodes: list[Node]) -> list[Node]:
        try:
            self.step_model.set_running(input_nodes)

            output_nodes = self.execute(input_nodes)

            self.step_model.set_completed(output_nodes)

            return output_nodes
        except Exception as e:
            self.step_model.set_status(StepStatus.ERRORED)
            raise e

    @abstractmethod
    def execute(self, input_data: list[Node]):
        pass
