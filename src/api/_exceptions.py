from typing import Optional


class APIError(Exception):
    def __init__(
        self,
        success: bool,
        status: int,
        error: Optional[dict] = None,
        response: Optional[dict] = None,
    ):
        self.success = success
        self.status = status
        self.error = error
        self.response = response
        super().__init__(self.error)


class InternalServerError(APIError):
    def __init__(self, error: Optional[dict] = None, response: Optional[dict] = None):
        super().__init__(
            success=False,
            status=500,
            error=error or {"message": "Internal Server Error"},
            response=response,
        )


class NotFoundError(APIError):
    def __init__(self, error: Optional[dict] = None, response: Optional[dict] = None):
        super().__init__(
            success=False,
            status=404,
            error=error or {"message": "Not Found"},
            response=response,
        )


class BadRequestError(APIError):
    def __init__(self, error: Optional[dict] = None, response: Optional[dict] = None):
        super().__init__(
            success=False,
            status=400,
            error=error or {"message": "Bad Request"},
            response=response,
        )


class UnsupportedModelProviderError(Exception):
    """Exception raised for unsupported model provider."""

    pass


class UnsupportedModelVersionError(Exception):
    """Exception raised for unsupported model version."""

    pass


class JSONSchemaParsingError(Exception):
    """Exception raised for errors during JSON schema parsing."""

    pass


class ModelExecutionError(Exception):
    """Exception raised for errors during model execution."""

    pass


class ModelResponseFormatValidationError(Exception):
    """Exception raised for validation errors from response format."""

    def __init__(self, error="", suggestion=""):
        self.error = error
        self.suggestion = suggestion
        super().__init__(f"{self.error} Suggestion: {self.suggestion}")
