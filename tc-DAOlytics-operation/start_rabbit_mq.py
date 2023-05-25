"""
start the project using rabbitMQ
"""
from utils.daolytics_uitls import get_mongo_credentials, get_rabbit_mq_credentials
from utils import CallBackFunctions
from tc_messageBroker.message_broker import RabbitMQ
from tc_messageBroker.rabbit_mq.queue import Queue
from tc_messageBroker.rabbit_mq.event import Event


def analyzer():
    rabbit_mq_creds = get_rabbit_mq_credentials()
    mongo_creds = get_mongo_credentials()

    rabbit_mq = RabbitMQ(
        broker_url=rabbit_mq_creds["broker_url"],
        port=rabbit_mq_creds["port"],
        username=rabbit_mq_creds["username"],
        password=rabbit_mq_creds["password"],
    )

    callback = CallBackFunctions(
        mongo_creds=mongo_creds, rabbit_mq_creds=rabbit_mq_creds
    )

    rabbit_mq.connect(Queue.DISCORD_ANALYZER)

    rabbit_mq.on_event(Event.DISCORD_ANALYZER.RUN, callback.analyzer_recompute)

    rabbit_mq.channel.start_consuming()


if __name__ == "__main__":
    analyzer()
