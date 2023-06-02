"""
start the project using rabbitMQ
"""
from utils.daolytics_uitls import (
    # get_mongo_credentials,
    get_rabbit_mq_credentials,
    # get_neo4j_credentials,
    # get_saga_db_location,
    get_sentryio_service_creds,
    get_redis_credentials,
)

import logging
from utils.sentryio_service import set_up_sentryio
from tc_messageBroker.message_broker import RabbitMQ
from tc_messageBroker.rabbit_mq.queue import Queue
from rq import Queue as RQ_Queue
from tc_messageBroker.rabbit_mq.event import Event
from redis import Redis
from discord_utils import analyzer_recompute, analyzer_run_once
import functools


def analyzer():
    rabbit_mq_creds = get_rabbit_mq_credentials()
    sentry_creds = get_sentryio_service_creds()

    ## sentryio service
    set_up_sentryio(sentry_creds["dsn"], sentry_creds["env"])
    redis_creds = get_redis_credentials()

    rabbit_mq = RabbitMQ(
        broker_url=rabbit_mq_creds["broker_url"],
        port=rabbit_mq_creds["port"],
        username=rabbit_mq_creds["username"],
        password=rabbit_mq_creds["password"],
    )

    redis = Redis(
        host=redis_creds["host"],
        port=redis_creds["port"],
        password=redis_creds["pass"],
    )

    rq_queue = RQ_Queue(connection=redis, default_timeout=1800)

    analyzer_recompute = functools.partial(recompute_wrapper, redis_queue=rq_queue)
    analyzer_run_once = functools.partial(run_once_wrapper, redis_queue=rq_queue)

    rabbit_mq.connect(Queue.DISCORD_ANALYZER, heartbeat=60)

    rabbit_mq.on_event(Event.DISCORD_ANALYZER.RUN, analyzer_recompute)
    rabbit_mq.on_event(Event.DISCORD_ANALYZER.RUN_ONCE, analyzer_run_once)

    if rabbit_mq.channel is None:
        print("Error: was not connected to RabbitMQ broker!")
    else:
        rabbit_mq.channel.start_consuming()


def recompute_wrapper(body: dict[str, any], redis_queue):
    sagaId = body["content"]["uuid"]
    logging.info(f"SAGAID:{sagaId} recompute job Adding to queue")
    redis_queue.enqueue(analyzer_recompute, sagaId)


def run_once_wrapper(body: dict[str, any], redis_queue):
    sagaId = body["content"]["uuid"]
    logging.info(f"SAGAID:{sagaId} run_once job Adding to queue")
    redis_queue.enqueue(analyzer_run_once, sagaId)


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    analyzer()
