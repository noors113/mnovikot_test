from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from src.core.config import settings
from starlette.middleware.cors import CORSMiddleware

from src.api.errors.http_error import common_error_handler
from src.api.errors.validation_error import http422_error_handler
from src.api.routes import router as api_router
from src.core.exceptions import CommonErrorException


# if settings.SENTRY_DSN:
#     sentry_sdk.init(
#         dsn=settings.SENTRY_DSN,
#         traces_sample_rate=1.0,
#         integrations=[
#             StarletteIntegration(),
#             FastApiIntegration(),
#         ],
#     )


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        docs_url=None if not settings.DEBUG else "/docs",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(
        CommonErrorException, common_error_handler
    )
    application.add_exception_handler(
        RequestValidationError, http422_error_handler
    )

    application.include_router(
        api_router,
        prefix=settings.API_PREFIX,
        default_response_class=ORJSONResponse,
    )

    return application


app = get_application()
