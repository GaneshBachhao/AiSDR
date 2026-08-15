from .workflow_exception import WorkflowException


class WorkflowStepException(WorkflowException):
    """
    Raised when a workflow step business rule is violated.
    """

    pass