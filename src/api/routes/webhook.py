import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Body
from fastapi.responses import ORJSONResponse
from starlette import status

from src.enums.event_types import EventTypes
from src.schemas.event import (
    BaseEventSchema,
    ConversationStartedEventSchema,
    MessageEventSchema,
)
from src.services.storage import StoragePool
from src.worker import task_send_event

logger = logging.getLogger()
router = APIRouter()


@router.post("/viber/")
async def process_viber_webhook(
    payload: Annotated[
        BaseEventSchema | ConversationStartedEventSchema | MessageEventSchema,
        Body(alias="event_payload"),
    ],
):
    try:
        if payload.event == EventTypes.WEBHOOK:
            return ORJSONResponse(
                {"message": "success"}, status_code=status.HTTP_200_OK
            )
        elif payload.event == EventTypes.CONVERSATION_START:
            return ORJSONResponse(
                {
                    "min_api_version": 8,
                    "type": "text",
                    "text": "Добро пожаловать! Это сообщение по-умолчанию, "
                    "обратитесь к менеджерам, чтоб его изменить.",
                    "sender": {"name": "Автоматический ответ", "avatar": None},
                },
                status_code=status.HTTP_200_OK,
            )
        else:
            kv_storage = StoragePool()
            celery_id = str(uuid.uuid4())
            signature = str(hash(frozenset(payload.model_dump().items())))
            task_exits = await kv_storage.get(signature)
            if task_exits is not None:
                return ORJSONResponse(
                    {"message": "Task is already processing"},
                    status_code=status.HTTP_200_OK,
                )
            await kv_storage.insert(
                signature, {"status": "waiting", "celery_id": celery_id}
            )
            task_send_event.apply_async(
                kwargs={"data": payload.model_dump_json(), "celery_id": celery_id}, coundown=0
            )
            return ORJSONResponse(
                content={"message": "Task started processing"},
                headers={"X-Celery-ID": celery_id},
                status_code=status.HTTP_200_OK,
            )
    except Exception as e:
        logger.exception(e)
        # to return 200 status in any case
        return ORJSONResponse({}, status_code=status.HTTP_200_OK)
