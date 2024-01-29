import pydantic
from pydantic import AnyHttpUrl


class EventUserSchema(pydantic.BaseModel):
    id: str
    name: str
    avatar: AnyHttpUrl
    language: str
    country: str
    api_version: int
