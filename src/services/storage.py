from typing import Any, Dict, List

import orjson

from src.core.utils import serialize_orjson
from src.db.database import kv_session


class StoragePool:
    storage = kv_session

    async def insert(
        self, key: str, payload: Any, seconds_ttl: int | None = None
    ) -> None:
        _payload: bytes = serialize_orjson(payload)
        await self.storage.set(key, _payload, ex=seconds_ttl)

    async def get(
        self, key: str, default: Any = None
    ) -> Dict[Any, Any] | List[Any] | Any | str | None:
        _value: str | None = await self.storage.get(name=key)

        if _value:
            _value: Dict | List = orjson.loads(_value)

        return _value or default

    async def clean_key(self, key: str) -> None:
        await self.storage.delete(key)

    async def close(self):
        await self.storage.aclose()