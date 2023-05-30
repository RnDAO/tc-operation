from utils.daolytics_uitls import (
    get_mongo_credentials,
    get_neo4j_credentials,
    get_rabbit_mq_credentials,
)
from utils.callback_functions import CallBackFunctions
from tc_messageBroker.message_broker import RabbitMQ
import pytest


def test_rabbit_mq_connect():
    rabbit_creds = get_rabbit_mq_credentials()
    rabbit_mq = RabbitMQ(
        broker_url=rabbit_creds["broker_url"],
        port=rabbit_creds["port"],
        username=rabbit_creds["username"],
        password=rabbit_creds["password"],
    )

    connect = rabbit_mq.connect("sample_queue")

    ## when no rabbitmq instance is running it should be False
    assert connect is False


@pytest.mark.skip(reason="No Neo4J instance available on github actions")
def test_analyzer_init():
    callback = set_up_callback_class()
    callback._initialize_analyzer()


def set_up_callback_class():
    mongo_creds = get_mongo_credentials()
    neo4j_creds = get_neo4j_credentials()
    rabbit_creds = get_rabbit_mq_credentials()

    rabbit_mq = RabbitMQ(
        broker_url=rabbit_creds["broker_url"],
        port=rabbit_creds["port"],
        username=rabbit_creds["username"],
        password=rabbit_creds["password"],
    )

    rabbit_mq.connect("sample_queue")

    saga_callback_location = {"db_name": "Saga", "collection_name": "saga"}

    callback = CallBackFunctions(
        mongo_creds=mongo_creds,
        neo4j_creds=neo4j_creds,
        rabbitmq_instance=rabbit_mq,
        saga_mongo_location=saga_callback_location,
    )

    return callback
