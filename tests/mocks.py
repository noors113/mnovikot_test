from typing import Any


class AioRedisMock:
    async def get(self, name: str):
        pass

    async def set(self, key: str, payload: bytes, ex: int):
        pass

    async def delete(self, key: str):
        pass

    async def aclose(self):
        pass


class StorageMock:
    def __init__(self):
        self.storage = dict()

    async def insert(self, key: str, payload: Any, seconds_ttl: int | None = None):
        self.storage[key] = payload

    async def get(self, key: str, default: Any = None):
        return self.storage.get(key, default)

    async def clean_key(self, key: str):
        self.storage.pop(key, None)

    async def close(self):
        pass
