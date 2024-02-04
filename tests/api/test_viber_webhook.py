import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.api.routes import webhook
from tests.mocks import AioRedisMock, StorageMock

client = TestClient(webhook.router)


class TestViberWebhook:

    def test_process_viber_webhook_with_webhook_event(self):
        response = client.post(
            "/viber/",
            json={
                "event": "webhook",
                "timestamp": str(datetime.datetime.timestamp(datetime.datetime.now())),
                "chat_hostname": "SN-CHAT-01_",
                "message_token": "5916836919477944763",
            },
        )
        assert response.status_code == 200
        assert response.json() == {"message": "success"}

    def test_process_viber_webhook_with_conversation_start_event(self):
        response = client.post(
            "/viber/",
            json={
                "event": "conversation_started",
                "timestamp": str(datetime.datetime.timestamp(datetime.datetime.now())),
                "chat_hostname": "SN-563_",
                "message_token": "5916837284433914371",
                "type": "open",
                "user": {
                    "id": "12345",
                    "name": "Sergey Rùdnev",
                    "avatar": "https://media-direct.cdn.viber.com/download_photo?dlid=MFojMvbS52ZImnxNQUHeU3zomFr47zbnIu6Zj613oDvnQmtgG--p0H_1mI7PPH10Y89AEuUTXTC_7k-j9elWuN6kQ3k1-uJgNEZQ_oJCpt84AB7tGnB4YiFOfeNmFb6bH4sCLw&fltp=jpg&imsz=0000",
                    "language": "en",
                    "country": "RU",
                    "api_version": 8,
                },
                "subscribed": False,
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "min_api_version": 8,
            "type": "text",
            "text": "Добро пожаловать! Это сообщение по-умолчанию, обратитесь к менеджерам, чтоб его изменить.",
            "sender": {"name": "Автоматический ответ", "avatar": None},
        }

    def test_process_viber_webhook_with_message_event(self):
        with (
            patch(
                "src.services.storage.kv_session", return_value=AioRedisMock()
            ) as mock_make_kv_session,
            patch(
                "src.api.routes.webhook.StoragePool", return_value=StorageMock()
            ) as mocked_storage,
            patch(
                "src.api.routes.webhook.task_send_event", MagicMock()
            ) as mocked_celery_task,
        ):
            response = client.post(
                "/viber/",
                json={
                    "event": "message",
                    "timestamp": str(
                        datetime.datetime.timestamp(datetime.datetime.now())
                    ),
                    "chat_hostname": "SN-CALLBACK-21_",
                    "message_token": "5916837654388304302",
                    "sender": {
                        "id": "12345",
                        "name": "Sergey Rùdnev",
                        "avatar": "https://media-direct.cdn.viber.com/download_photo?dlid=MFojMvbS52ZImnxNQUHeU3zomFr47zbnIu6Zj613oDvnQmtgG--p0H_1mI7PPH10Y89AEuUTXTC_7k-j9elWuN6kQ3k1-uJgNEZQ_oJCpt84AB7tGnB4YiFOfeNmFb6bH4sCLw&fltp=jpg&imsz=0000",
                        "language": "en",
                        "country": "RU",
                        "api_version": 8,
                    },
                    "message": {"text": "/start", "type": "text"},
                    "silent": False,
                },
            )
        assert response.status_code == 200
        assert "X-Celery-ID".lower() in response.headers.keys()

        mocked_storage.assert_called_once()
        mocked_celery_task.apply_async.assert_called_once()

    def test_process_viber_webhook_with_message_event_but_no_redis_connection(self):
        response = client.post(
            "/viber/",
            json={
                "event": "message",
                "timestamp": str(datetime.datetime.timestamp(datetime.datetime.now())),
                "chat_hostname": "SN-CALLBACK-21_",
                "message_token": "5916837654388304302",
                "sender": {
                    "id": "12345",
                    "name": "Sergey Rùdnev",
                    "avatar": "https://media-direct.cdn.viber.com/download_photo?dlid=MFojMvbS52ZImnxNQUHeU3zomFr47zbnIu6Zj613oDvnQmtgG--p0H_1mI7PPH10Y89AEuUTXTC_7k-j9elWuN6kQ3k1-uJgNEZQ_oJCpt84AB7tGnB4YiFOfeNmFb6bH4sCLw&fltp=jpg&imsz=0000",
                    "language": "en",
                    "country": "RU",
                    "api_version": 8,
                },
                "message": {"text": "/start", "type": "text"},
                "silent": False,
            },
        )
        assert response.status_code == 200

    def test_process_viber_webhook_with_existing_task(self):
        with (
            patch(
                "src.services.storage.kv_session", return_value=AioRedisMock()
            ) as mock_make_kv_session,
            patch(
                "src.api.routes.webhook.StoragePool", return_value=StorageMock()
            ) as mocked_storage,
            patch(
                "src.api.routes.webhook.task_send_event", MagicMock()
            ) as mocked_celery_task,
        ):
            test_data = {
                "event": "message",
                "timestamp": str(datetime.datetime.timestamp(datetime.datetime.now())),
                "chat_hostname": "SN-CALLBACK-21_",
                "message_token": "5916837654388304302",
                "sender": {
                    "id": "12345",
                    "name": "Sergey Rùdnev",
                    "avatar": "https://media-direct.cdn.viber.com/download_photo?dlid=MFojMvbS52ZImnxNQUHeU3zomFr47zbnIu6Zj613oDvnQmtgG--p0H_1mI7PPH10Y89AEuUTXTC_7k-j9elWuN6kQ3k1-uJgNEZQ_oJCpt84AB7tGnB4YiFOfeNmFb6bH4sCLw&fltp=jpg&imsz=0000",
                    "language": "en",
                    "country": "RU",
                    "api_version": 8,
                },
                "message": {"text": "/start", "type": "text"},
                "silent": False,
            }
            client.post("/viber/", json=test_data)  # First request to create the task
            response = client.post(
                "/viber/", json=test_data
            )  # Second request with the same task
            assert response.status_code == 200
            assert response.json() == {"message": "Task is already processing"}

    def test_request_with_raise_exception(self):
        with pytest.raises(BaseException):
            response = client.post("/viber/", json={})
            assert response.status_code == 200
            assert response.json() == {}
