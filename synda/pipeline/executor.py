from abc import abstractmethod

from sqlmodel import Session

from synda.model.run import Run
from synda.model.step import Step, StepStatus
from synda.model.node import Node


class Executor:
    def __init__(self, session: Session, run: Run, step_model: Step):
        self.session = session
        self.run = run
        self.step_model = step_model
        self.config = step_model.get_step_config()

    def execute_and_update_step(self, input_nodes: list[Node]) -> list[Node]:
        try:
            self.step_model.set_running(self.session, input_nodes)

            output_nodes = self.execute(input_nodes)
            self._add_ancestors(input_nodes, output_nodes, self.step_model.name)

            self.step_model.set_completed(self.session, output_nodes)

            return output_nodes
        except Exception as e:
            self.step_model.set_status(self.session, StepStatus.ERRORED)
            raise e

    @staticmethod
    def _add_ancestors(
        input_nodes: list[Node], output_nodes: list[Node], step_name: str
    ) -> None:
        for output_node in output_nodes:
            parent_id = output_node.parent_node_id

            if parent_id is None:
                continue

            parent_node = next(
                (node for node in input_nodes if node.id == parent_id), None
            )
            output_node.ancestors = parent_node.ancestors | {step_name: parent_node.id}

    @abstractmethod
    def execute(self, input_data: list[Node]):
        pass
