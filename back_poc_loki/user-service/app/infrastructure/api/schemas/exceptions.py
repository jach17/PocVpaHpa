from http import HTTPStatus


class BaseHttpError(Exception):
    def __init__(
        self,
        message,
        information=None,
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        self.message = message
        self.information = information
        self.http_status = http_status

        super().__init__(self.message)


class BusinessError(BaseHttpError):
    """Raised when an error occurs when sending a Slack message."""  # noqa: D400


class CustomServiceError(BaseHttpError):
    """Raised when an error occurs when sending a Slack message."""  # noqa: D400


class ParametersError(BaseHttpError):
    """Raised when an error occurs when sending a Slack message."""  # noqa: D400


class UnauthorizedError(BaseHttpError):
    def __init__(
        self,
        message,
        information=None,
        http_status=HTTPStatus.UNAUTHORIZED,
    ):
        super.__init__(message, information, http_status)


class ForbiddenError(BaseHttpError):
    def __init__(
        self,
        message,
        information=None,
        http_status=HTTPStatus.FORBIDDEN,
    ):
        super.__init__(message, information, http_status)


class NotFoundError(BaseHttpError):
    def __init__(
        self,
        message,
        information=None,
        http_status=HTTPStatus.NOT_FOUND,
    ):
        super.__init__(message, information, http_status)
