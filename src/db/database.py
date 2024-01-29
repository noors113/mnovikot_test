from redis import asyncio as aioredis

from src.core.config import settings


def make_kv_session() -> aioredis.Redis:
    return aioredis.from_url(  # type: ignore
        settings.REDIS_DSN.unicode_string(), decode_responses=True, encoding="utf-8"
    )


kv_session: aioredis.Redis = make_kv_session()
