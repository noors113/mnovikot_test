from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from src.core.exceptions import CommonErrorException
from src.schemas.common import ErrorSchema


async def common_error_handler(_: Request, exc: CommonErrorException) -> ORJSONResponse:
    schema = ErrorSchema(message=exc.detail)
    return ORJSONResponse(schema.model_dump(), status_code=exc.status_code)
