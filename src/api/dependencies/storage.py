from src.services.storage import StoragePool


async def get_kv_storage() -> StoragePool:
    return StoragePool()
