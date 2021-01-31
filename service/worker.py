import config
from redis import Redis
from rq import Queue

conn = Redis(config.REDIS_URL)
worker_queue = Queue(connection=conn, default_timeout=600)