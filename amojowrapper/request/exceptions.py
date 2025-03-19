class RequestError(Exception):
    """
    Custom exception to handle errors in the request process.

    This exception is raised when a request encounters an error that
    requires special handling or logging. It extends the built-in
    Exception class and carries a message that provides additional
    details about the error.
    """

    def __init__(self, message: str):
        """
        Initialize the RequestError with a message.

        Args:
            message (str): The error message describing the issue.
        """
        self.message = message
