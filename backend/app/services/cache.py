import json

import redis

from app.core.config import get_settings

settings = get_settings()
_redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

ANALYSIS_CACHE_TTL_SECONDS = 60 * 60 * 24

def get_cached_analysis(resume_id: str, job_id: str) -> dict | None:
    key = f"analysis:{resume_id}:{job_id}"
    try:
        cached = _redis_client.get(key)
        return json.loads(cached) if cached else None
    except redis.RedisError:
        return None

def set_cached_analysis(resume_id: str, job_id: str, result: dict) -> None:
    key = f"analysis:{resume_id}:{job_id}"
    try:
        _redis_client.setex(key, ANALYSIS_CACHE_TTL_SECONDS, json.dumps(result))
    except redis.RedisError:
        pass