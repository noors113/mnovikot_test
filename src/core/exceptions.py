from fastapi import HTTPException, status


class CommonErrorException(HTTPException):
    def __init__(
        self,
        error: str | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(status_code=status_code, detail=error)
