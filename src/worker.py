import logging

import httpx
from celery import Celery

from src.core.config import settings

celery = Celery(
    "viber_gateway",
    broker=settings.CELERY_BROKER_URL.unicode_string(),
    backend=settings.CELERY_RESULT_BACKEND.unicode_string(),
)
celery.autodiscover_tasks()

logger = logging.getLogger()


@celery.task(name="send_event", rate_limit="8/s")
def task_send_event(data: dict, celery_id: str):
    try:
        with httpx.Client() as client:
            logger.info(
                f"Sending request to {settings.CHAT_WEBHOOK_API_URL} with "
                f"celery_id={celery_id}"
            )
            # Отправляем запрос на указанный адрес
            response = client.post(
                settings.CHAT_WEBHOOK_API_URL,
                headers={"X-Celery-ID": celery_id},
                json=data,
            )
            logger.info(
                f"Request sent successfully with response={response.json()} "
                f"and status={response.status_code}"
            )
    except Exception as e:
        logger.exception(e)
