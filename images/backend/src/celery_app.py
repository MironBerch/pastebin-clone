from celery import Celery

from core.config import settings

redis = settings.redis

celery_app = Celery(
    'tasks',
    broker=f'redis://{redis.host}:{redis.port}/{redis.db}',
    backend=f'redis://{redis.host}:{redis.port}/{redis.db}',
    include=['services.tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
