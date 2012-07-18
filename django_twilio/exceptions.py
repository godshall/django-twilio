"""Custom exceptions."""


class DjangoTwilioException(RuntimeError):
    """There was an ambiguous exception that occured while handling your
    request.
    """


class InvalidMethodError(DjangoTwilioException):
    """The HTTP method specified is not valid."""
