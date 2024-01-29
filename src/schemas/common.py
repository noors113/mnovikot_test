import datetime

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    message: str
    time: datetime.datetime = datetime.datetime.now()
