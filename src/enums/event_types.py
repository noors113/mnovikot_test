import enum


class EventTypes(enum.Enum):
    WEBHOOK: str = "webhook"
    CONVERSATION_START: str = "conversation_started"
    MESSAGE: str = "message"
