from analyzer_init import AnalyzerInit
from tc_messageBroker.rabbit_mq.saga.saga_base import get_saga
from tc_messageBroker import RabbitMQ
from tc_messageBroker.rabbit_mq.queue import Queue
import logging
import functools


def prepare_rabbit_mq(rabbit_creds):
    rabbitmq = RabbitMQ(
        broker_url=rabbit_creds["broker_url"],
        port=rabbit_creds["port"],
        username=rabbit_creds["username"],
        password=rabbit_creds["password"],
    )
    rabbitmq.connect(queue_name=Queue.DISCORD_ANALYZER)

    return rabbitmq


def thread_safe_publish(rebbit_instance):
    """
    do publishing in a thread safe format
    """


def analyzer_recompute(sagaId: str, rabbit_creds: dict[str, any]):
    analyzer_init = AnalyzerInit()
    analyzer, mongo_creds = analyzer_init.get_analyzer()
    rabbitmq = prepare_rabbit_mq(rabbit_creds)

    saga = get_saga_instance(
        sagaId=sagaId,
        connection=mongo_creds["connection_str"],
        saga_db=mongo_creds["db_name"],
        saga_collection=mongo_creds["collection_name"],
    )
    if saga is None:
        logging.warn(
            f"Warn: Saga not found!, stopping the recompute for sagaId: {sagaId}"
        )
    else:
        guildId = saga.data["guildId"]

        def recompute_wrapper(**kwargs):
            analyzer.recompute_analytics(guildId=guildId)

        def publish_wrapper(**kwargs):
            queue_name = kwargs["queue_name"]
            logging.info(f"GUILDID: {guildId}: Publishing for {queue_name}")
            rabbitmq.connection.add_callback_threadsafe(
                functools.partial(
                    rabbitmq.publish,
                    kwargs=kwargs,
                )
            )

        saga.next(
            publish_method=publish_wrapper,
            call_function=recompute_wrapper,
            mongo_creds=mongo_creds,
        )


def analyzer_run_once(sagaId: str, rabbit_creds: dict[str, any]):
    analyzer_init = AnalyzerInit()
    analyzer, mongo_creds = analyzer_init.get_analyzer()
    rabbitmq = prepare_rabbit_mq(rabbit_creds)

    saga = get_saga_instance(
        sagaId=sagaId,
        connection=mongo_creds["connection_str"],
        saga_db=mongo_creds["db_name"],
        saga_collection=mongo_creds["collection_name"],
    )
    if saga is None:
        logging.warn(f"Saga not found!, stopping the run_once for sagaId: {sagaId}")
    else:
        guildId = saga.data["guildId"]

        def run_once_wrapper(**kwargs):
            analyzer.run_once(guildId=guildId)

        def publish_wrapper(**kwargs):
            queue_name = kwargs["queue_name"]
            logging.info(f"GUILDID: {guildId}: Publishing for {queue_name}")
            rabbitmq.connection.add_callback_threadsafe(
                functools.partial(
                    rabbitmq.publish,
                    kwargs=kwargs,
                )
            )

        saga.next(
            publish_method=publish_wrapper,
            call_function=run_once_wrapper,
            mongo_creds=mongo_creds,
        )


def get_saga_instance(sagaId: str, connection: str, saga_db: str, saga_collection: str):
    saga = get_saga(
        sagaId=sagaId,
        connection_url=connection,
        db_name=saga_db,
        collection=saga_collection,
    )
    return saga
