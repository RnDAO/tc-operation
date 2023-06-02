from rndao_analyzer import RnDaoAnalyzer
from utils.daolytics_uitls import (
    get_mongo_credentials,
    get_saga_db_location,
    get_neo4j_credentials,
)


class AnalyzerInit:
    """
    initialize the analyzer with its configs
    """

    def __init__(self) -> None:
        pass

    def get_analyzer(self):
        """
        Returns:
        ---------
        analyzer : RnDaoAnalyzer
        mongo_connection : str
        saga_db : str
        saga_collection : str
        """
        analyzer = RnDaoAnalyzer()

        ## credentials
        mongo_creds = get_mongo_credentials()
        neo4j_creds = get_neo4j_credentials()
        saga_mongo_location = get_saga_db_location()
        saga_db = saga_mongo_location["db_name"]
        saga_collection = saga_mongo_location["collection_name"]

        analyzer.set_mongo_database_info(
            mongo_db_host=mongo_creds["host"],
            mongo_db_password=mongo_creds["password"],
            mongo_db_port=mongo_creds["port"],
            mongo_db_user=mongo_creds["user"],
        )
        analyzer.set_neo4j_database_info(neo4j_creds=neo4j_creds)
        analyzer.database_connect()

        mongo_connection = self._get_mongo_connection(mongo_creds=mongo_creds)

        return analyzer, mongo_connection, saga_db, saga_collection

    def _get_mongo_connection(self, mongo_creds: dict[str, any]):
        user = mongo_creds["user"]
        password = mongo_creds["password"]
        host = mongo_creds["host"]
        port = mongo_creds["port"]

        connection = f"mongodb://{user}:{password}@{host}:{port}"

        return connection
