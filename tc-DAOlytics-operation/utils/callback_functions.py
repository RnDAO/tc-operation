from rndao_analyzer import RnDaoAnalyzer
from tc_messageBroker.message_broker import RabbitMQ
from tc_messageBroker.rabbit_mq.saga.saga_base import get_saga


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
        self.mongo_connection = self._get_mongo_connection(mongo_creds)

        self.rabbit_mq = rabbitmq_instance
        self.analyzer = self._initialize_analyzer()

        self.saga_mongo_location = saga_mongo_location

        self.guildId = None

    def _get_mongo_connection(self, mongo_creds: dict[str, any]):
        user = mongo_creds["user"]
        password = mongo_creds["password"]
        host = mongo_creds["host"]
        port = mongo_creds["port"]

        connection = f"mongodb://{user}:{password}@{host}:{port}"

        return connection

    def _initialize_analyzer(self):
        """
        initialize the analyzer configs
        - MongoDB database
        - Neo4J database
        """
        analyzer = RnDaoAnalyzer()

        analyzer.set_mongo_database_info(
            mongo_db_host=self._mongo_creds["user"],
            mongo_db_password=self._mongo_creds["password"],
            mongo_db_port=self._mongo_creds["port"],
            mongo_db_user=self._mongo_creds["user"],
        )

        analyzer.set_neo4j_database_info(
            neo4j_db_name=self._neo4j_creds["db_name"],
            neo4j_password=self._neo4j_creds["pass"],
            neo4j_url=self._neo4j_creds["url"],
            neo4j_user=self._neo4j_creds["user"],
        )
        analyzer.database_connect()

        return analyzer

    def analyzer_recompute(self, body: dict[str, any]):
        self.guildId = body["data"]["guildId"]

        saga = self._get_saga_instance(guildId=self.guildId)

        saga.next(
            publish_method=self.rabbit_mq.publish,
            call_function=self._callback_recompute,
            mongo_connection=self.mongo_connection,
        )

    def analyzer_run_once(self, body: dict[str, any]):
        self.guildId = body["data"]["guildId"]
        saga = self._get_saga_instance(guildId=self.guildId)

        saga.next(
            publish_method=self.rabbit_mq.publish,
            call_function=self._callback_run_once,
            mongo_connection=self.mongo_connection,
        )

    def _callback_recompute(self):
        self.analyzer.recompute_analytics(guildId=self.guildId)

    def _callback_run_once(self):
        self.analyzer.run_once(guildId=self.guildId)

    def _get_saga_instance(self, guildId):
        saga = get_saga(
            guildId=guildId,
            connection_url=self.mongo_connection,
            db_name=self.saga_mongo_location["db_name"],
            collection=self.saga_mongo_location["collection_name"],
        )
        return saga
