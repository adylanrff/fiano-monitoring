import config
from redis import Redis
from rq import Queue
from monkeypatch import notion_patch

notion_patch.monkey_patch()
conn = Redis(config.REDIS_URL)
worker_queue = Queue(connection=conn, default_timeout=600)