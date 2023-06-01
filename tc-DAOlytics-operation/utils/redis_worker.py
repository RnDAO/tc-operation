import redis
from rq import Worker
from daolytics_uitls import get_redis_credentials

if __name__ == "__main__":
    redis_creds = get_redis_credentials()
    host = redis_creds["host"]
    port = redis_creds["port"]
    password = redis_creds["pass"]

    r = redis.Redis(host=host, port=port, password=password)
    worker = Worker(queues=["default"], connection=r)
    worker.work(with_scheduler=True)
