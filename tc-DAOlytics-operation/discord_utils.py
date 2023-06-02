from analyzer_init import AnalyzerInit
from tc_messageBroker.rabbit_mq.saga.saga_base import get_saga
import logging


def analyzer_recompute(sagaId):
    analyzer_init = AnalyzerInit()
    analyzer, mongo_creds = analyzer_init.get_analyzer()

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
            logging.info(f"PUBLISHING FOR GUILD: {guildId}, kwargs: {kwargs}")

        analyzer.recompute_analytics(guildId=guildId)
        saga.next(
            publish_method=publish_wrapper,
            call_function=recompute_wrapper,
            mongo_creds=mongo_creds,
        )


def analyzer_run_once(sagaId):
    analyzer_init = AnalyzerInit()
    analyzer, mongo_creds = analyzer_init.get_analyzer()

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
        analyzer.run_once(guildId=guildId)


def get_saga_instance(sagaId: str, connection: str, saga_db: str, saga_collection: str):
    saga = get_saga(
        sagaId=sagaId,
        connection_url=connection,
        db_name=saga_db,
        collection=saga_collection,
    )
    return saga