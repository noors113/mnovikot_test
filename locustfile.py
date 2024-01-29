import datetime
import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    min_wait = 0.2
    max_wait = 5

    # @task
    # def webhook(self):
    #     self.client.post(
    #         "/api/v1/webhooks/viber/",
    #         {
    #             "event": "webhook",
    #             "timestamp": str(
    #                 datetime.datetime.timestamp(datetime.datetime.now())
    #             ),
    #             "chat_hostname": "SN-CHAT-01_",
    #             "message_token": 5916836919477944763
    #         }
    #     )

    @task(9)
    def conversation_start(self):
        self.client.post(
            "/api/v1/webhooks/viber/",
            json={
                "event": "conversation_started",
                "timestamp": str(
                    datetime.datetime.timestamp(datetime.datetime.now())
                ),
                "chat_hostname": "SN-563_",
                "message_token": "5916837284433914371",
                "type": "open",
                "user": {
                    "id": "12345",
                    "name": "Sergey Rùdnev",
                    "avatar": "https://media-direct.cdn.viber.com/download_photo?dlid=MFojMvbS52ZImnxNQUHeU3zomFr47zbnIu6Zj613oDvnQmtgG--p0H_1mI7PPH10Y89AEuUTXTC_7k-j9elWuN6kQ3k1-uJgNEZQ_oJCpt84AB7tGnB4YiFOfeNmFb6bH4sCLw&fltp=jpg&imsz=0000",
                    "language": "en",
                    "country": "RU",
                    "api_version": 8
                },
                "subscribed": False
            }
        )

    @task(1)
    def message(self):
        self.client.post(
            "/api/v1/webhooks/viber/",
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
                    "api_version": 8
                },
                "message": {
                    "text": "/start",
                    "type": "text"
                },
                "silent": False
            }
        )
