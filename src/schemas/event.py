import pydantic

from src.enums.event_types import EventTypes
from src.schemas.user import EventUserSchema


class BaseEventSchema(pydantic.BaseModel):
    event: EventTypes
    timestamp: str
    chat_hostname: str
    message_token: str


class ConversationStartedEventSchema(BaseEventSchema):
    type: str
    user: EventUserSchema
    subscribed: bool


class MessageSchema(pydantic.BaseModel):
    text: str
    type: str


class MessageEventSchema(BaseEventSchema):
    sender: EventUserSchema
    message: MessageSchema
    silent: bool
