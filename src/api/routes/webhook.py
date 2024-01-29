import logging
import uuid
from typing import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi.responses import ORJSONResponse
from starlette import status

from src.api.dependencies.storage import get_kv_storage
from src.enums.event_types import EventTypes
from src.schemas.event import (
    MessageEventSchema,
    ConversationStartedEventSchema,
    BaseEventSchema
)
from src.worker import task_send_event
from src.services.storage import StoragePool

logger = logging.getLogger()
router = APIRouter()


@router.post("/viber/")
async def process_viber_webhook(
    payload: Annotated[
        BaseEventSchema | ConversationStartedEventSchema | MessageEventSchema,
        Body(alias="event_payload")
    ],
    kv_storage: StoragePool = Depends(get_kv_storage)
):
    try:
        if payload.event == EventTypes.WEBHOOK:
            return ORJSONResponse(
                {"message": "success"},
                status_code=status.HTTP_200_OK
            )
        elif payload.event == EventTypes.CONVERSATION_START:
            return ORJSONResponse({
                "min_api_version": 8,
                "type": "text",
                "text": "Добро пожаловать! Это сообщение по-умолчанию, "
                        "обратитесь к менеджерам, чтоб его изменить.",
                "sender": {
                    "name": "Автоматический ответ",
                    "avatar": None
                }
            }, status_code=status.HTTP_200_OK)
        else:
            celery_id = str(uuid.uuid4())
            signature = str(hash(frozenset(payload.model_dump().items())))
            task_exits = await kv_storage.get(signature)
            if task_exits is not None:
                return ORJSONResponse(
                    {"message": "Task is already processing"},
                    status_code=status.HTTP_200_OK
                )
            await kv_storage.insert(
                signature,
                {"status": "waiting", "celery_id": celery_id}
            )
            task_send_event.delay(payload.json(), celery_id)
            return ORJSONResponse(
                content={},
                headers={"X-Celery-ID": celery_id},
                status_code=status.HTTP_200_OK
            )
    except Exception as e:
        logger.exception(e)
        # to return 200 status in any case
        return ORJSONResponse({}, status_code=status.HTTP_200_OK)
