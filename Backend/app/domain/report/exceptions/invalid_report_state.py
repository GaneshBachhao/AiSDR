from .report_exception import ReportException


class InvalidReportState(ReportException):
    """
    Raised when an invalid report state transition is attempted.
    """

    pass