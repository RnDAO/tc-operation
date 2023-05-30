"""
start the project using rabbitMQ
"""
from utils.daolytics_uitls import (
    get_mongo_credentials,
    get_rabbit_mq_credentials,
    get_neo4j_credentials,
    get_saga_db_location,
    get_sentryio_service_creds
)
from utils import CallBackFunctions
from utils.sentryio_service import set_up_sentryio
from tc_messageBroker.message_broker import RabbitMQ
from tc_messageBroker.rabbit_mq.queue import Queue
from tc_messageBroker.rabbit_mq.event import Event


def analyzer():
    rabbit_mq_creds = get_rabbit_mq_credentials()
    mongo_creds = get_mongo_credentials()
    neo4j_creds = get_neo4j_credentials()
    saga_creds = get_saga_db_location()
    sentry_creds = get_sentryio_service_creds()

    ## sentryio service
    set_up_sentryio(sentry_creds["dsn"], sentry_creds["env"])

    rabbit_mq = RabbitMQ(
        broker_url=rabbit_mq_creds["broker_url"],
        port=rabbit_mq_creds["port"],
        username=rabbit_mq_creds["username"],
        password=rabbit_mq_creds["password"],
    )

    callback = CallBackFunctions(
        mongo_creds=mongo_creds,
        neo4j_creds=neo4j_creds,
        rabbitmq_instance=rabbit_mq,
        saga_mongo_location=saga_creds,
    )

    rabbit_mq.connect(Queue.DISCORD_ANALYZER)

    rabbit_mq.on_event(Event.DISCORD_ANALYZER.RUN, callback.analyzer_recompute)
    rabbit_mq.on_event(Event.DISCORD_ANALYZER.RUN_ONCE, callback.analyzer_run_once)

    if rabbit_mq.channel is None:
        print("Error: was not connected to RabbitMQ broker!")
    else:
        rabbit_mq.channel.start_consuming()


if __name__ == "__main__":
    analyzer()
