from typing import Any

import orjson


def serialize_orjson(content: Any) -> bytes:
    return orjson.dumps(
        content,
        option=(
            orjson.OPT_NON_STR_KEYS
            | orjson.OPT_SERIALIZE_UUID
            | orjson.OPT_SERIALIZE_DATACLASS
        ),
    )


def dict_depth(payload: dict) -> int:
    return 1 + (max(map(dict_depth, payload.values())) if payload else 0)
