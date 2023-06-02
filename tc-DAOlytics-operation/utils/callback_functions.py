from rndao_analyzer import RnDaoAnalyzer
from tc_messageBroker.message_broker import RabbitMQ
from tc_messageBroker.rabbit_mq.saga.saga_base import get_saga
from redis import Redis
from rq import Queue
import logging


class CallBackFunctions:
    """
    the callback function for analyzer jobs
    """

    def __init__(
        self,
        mongo_creds: dict[str, any],
        rabbitmq_instance: RabbitMQ,
        neo4j_creds: dict[str, any],
        saga_mongo_location: dict[str, str],
        redis_creds: dict[str, any],
    ) -> None:
        """
        callback functions needed to used for DAOlytics

        Parameters:
        -----------
        mongo_connection : dict[str, any]
            mongodb credentials
            a dictionary representive of
             `mongo_user`: str
             `mongo_password` : str
             `mongo_host` : str
             `mongo_port` : int

        rabbitmq_instance : RabbitMQ
            rabbitMQ instance to use its publish method
        saga_mongo_location : dict[str, str]
            the location of saga instance in mongo database
            must have the dict keys of `db_name` and `collection_name`
        """
        self._mongo_creds = mongo_creds
        self._neo4j_creds = neo4j_creds
        self.redis_creds = redis_creds

        # self._mongo_creds = {}
        self._mongo_creds["connection_str"] = self._get_mongo_connection(mongo_creds)
        self._mongo_creds["db_name"] = saga_mongo_location["db_name"]
        self._mongo_creds["collection_name"] = saga_mongo_location["collection_name"]

        self.reddis_q = Queue(connection=self._initialize_redis())

        self.rabbit_mq = rabbitmq_instance
        self.analyzer = self._initialize_analyzer()

        self.guildId = None

    def _get_mongo_connection(self, mongo_creds: dict[str, any]):
        user = mongo_creds["user"]
        password = mongo_creds["password"]
        host = mongo_creds["host"]
        port = mongo_creds["port"]

        connection = f"mongodb://{user}:{password}@{host}:{port}"

        return connection

    def _initialize_redis(self):
        """
        initialize the redis connection

        """
        redis = Redis(
            host=self.redis_creds["host"],
            port=self.redis_creds["port"],
            password=self.redis_creds["pass"],
        )
        return redis

    def _initialize_analyzer(self):
        """
        initialize the analyzer configs
        - MongoDB database
        - Neo4J database
        """
        analyzer = RnDaoAnalyzer()

        analyzer.set_mongo_database_info(
            mongo_db_host=self._mongo_creds["host"],
            mongo_db_password=self._mongo_creds["password"],
            mongo_db_port=self._mongo_creds["port"],
            mongo_db_user=self._mongo_creds["user"],
        )

        analyzer.set_neo4j_database_info(neo4j_creds=self._neo4j_creds)

        analyzer.database_connect()

        return analyzer

    def analyzer_recompute(self, body: dict[str, any]):
        self.sagaId = body["content"]["uuid"]

        saga = self._get_saga_instance(sagaId=self.sagaId)

        if saga is not None:
            self.guildId = saga.data["guildId"]
            saga.next(
                publish_method=self.rabbit_mq.publish,
                call_function=self._callback_recompute,
                mongo_creds=self._mongo_creds,
            )
        else:
            logging.warn(f"Stopping the recompute job for guild: {self.guildId}")

    def analyzer_run_once(self, body: dict[str, any]):
        self.sagaId = body["content"]["uuid"]

        saga = self._get_saga_instance(sagaId=self.sagaId)

        if saga is not None:
            self.guildId = saga.data["guildId"]
            saga.next(
                publish_method=self.rabbit_mq.publish,
                call_function=self._callback_run_once,
                mongo_creds=self._mongo_creds,
            )
        else:
            logging.warn(f"Stopping the run_once job for guild: {self.guildId}")

    def _callback_recompute(self):
        logging.info(f"Callback recompute for {self.guildId} started!")
        self.reddis_q.enqueue(self.analyzer.recompute_analytics(guildId=self.guildId))

    def _callback_run_once(self):
        logging.info(f"Callback run_once for {self.guildId} started!")
        self.reddis_q.enqueue(self.analyzer.run_once(guildId=self.guildId))

    def _get_saga_instance(self, sagaId: str):
        saga = get_saga(
            sagaId=sagaId,
            connection_url=self._mongo_creds["connection_str"],
            db_name=self._mongo_creds["db_name"],
            collection=self._mongo_creds["collection_name"],
        )
        return saga
