from typing import Union

from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.schemas.common import ErrorSchema


class ErrorFormatter:
    def __init__(self, error_response, default=None):
        self.error_response = error_response
        self.default = default


class ValidationErrorFormatter(ErrorFormatter):
    def format(self):
        if isinstance(self.error_response, dict):
            result = self.error_response.get("detail")
            if not result:
                return self.default

        error_messages = []
        for error in self.error_response:
            error_messages.append(self._format_error(error))

        return "; ".join(error_messages) or self.default

    @staticmethod
    def _format_error(error):
        pydantic_error_keys = ("msg", "loc")
        if isinstance(error, dict):
            if frozenset(pydantic_error_keys).issubset(frozenset(error)):
                location = error["loc"][0]
                if location in ["body", "__root__"] and len(error["loc"]) > 1:
                    location = error["loc"][1]
                message = error["msg"]
                return "{}: {}".format(location, message)
        return str(error)


async def http422_error_handler(
    _: Request, exc: Union[RequestValidationError, ValidationError]
) -> ORJSONResponse:
    schema = ErrorSchema(
        message=ValidationErrorFormatter(
            error_response=exc.errors(),
            default="Response exception return error",
        ).format()
    )
    return ORJSONResponse(
        schema.model_dump(), status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    }
}
