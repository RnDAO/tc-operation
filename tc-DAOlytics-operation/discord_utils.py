from analyzer_init import AnalyzerInit
from tc_messageBroker.rabbit_mq.saga.saga_base import get_saga
import logging


def analyzer_recompute(sagaId):
    analyzer_init = AnalyzerInit()
    (
        analyzer,
        mongo_connection,
        saga_db,
        saga_collection,
    ) = analyzer_init.get_analyzer()

    saga = get_saga_instance(
        sagaId=sagaId,
        connection=mongo_connection,
        saga_db=saga_db,
        saga_collection=saga_collection,
    )
    if saga is None:
        logging.warn(
            f"Warn: Saga not found!, stopping the recompute for sagaId: {sagaId}"
        )
    else:
        guildId = saga.data["guildId"]
        analyzer.recompute_analytics(guildId=guildId)


def analyzer_run_once(sagaId):
    analyzer_init = AnalyzerInit()
    (
        analyzer,
        mongo_connection,
        saga_db,
        saga_collection,
    ) = analyzer_init.get_analyzer()

    saga = get_saga_instance(
        sagaId=sagaId,
        connection=mongo_connection,
        saga_db=saga_db,
        saga_collection=saga_collection,
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

def hellow(text):
    print(f"Hello {text}")