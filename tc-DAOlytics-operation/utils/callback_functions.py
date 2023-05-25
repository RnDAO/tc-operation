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
        rabbit_mq_creds: dict[str, any],
        neo4j_creds: dict[str, any],
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

        rabbit_mq_creds : dict[str, any]
            rabbitMQ credentials,
            a dictionary representive of
             `broker_url` : str
             `port` : int
             `username` : str
             `password` : str
        """
        self._rabbit_mq_creds = rabbit_mq_creds
        self._mongo_creds = mongo_creds
        self._neo4j_creds = neo4j_creds
        self.mongo_connection = self._get_mongo_connection(mongo_creds)

        self.rabbit_mq = self._initialize_rabbit_mq()
        self.analyzer = self._initialize_analyzer()

        self.guildId = None

    def _get_mongo_connection(self, mongo_creds: dict[str, any]):
        user = mongo_creds["user"]
        password = mongo_creds["password"]
        host = mongo_creds["host"]
        port = mongo_creds["port"]

        connection = f"mongodb://{user}:{password}@{host}:{port}"

        return connection

    def _initialize_rabbit_mq(self):
        """
        initialize the rabbitMQ instance
        """
        rabbit_mq = RabbitMQ(
            broker_url=self._rabbit_mq_creds["broker_url"],
            port=self._rabbit_mq_creds["port"],
            username=self._rabbit_mq_creds["username"],
            password=self._rabbit_mq_creds["password"],
        )

        return rabbit_mq

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

        return analyzer

    def analyzer_recompute(self, body: dict[str, any]):
        self.guildId = body["data"]["guildId"]

        saga = get_saga(guildId=self.guildId)

        saga.next(
            publish_method=self.rabbit_mq.publish,
            call_function=self._callback_recompute,
            mongo_connection=self.mongo_connection,
        )

    def _callback_recompute(self):
        self.analyzer.recompute_analytics(guildId=self.guildId)
