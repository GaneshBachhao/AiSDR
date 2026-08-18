from .workflow_exception import WorkflowException


class InvalidWorkflowState(WorkflowException):
    """
    Raised when an invalid workflow state transition is attempted.
    """

    pass
