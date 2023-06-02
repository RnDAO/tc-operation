from rndao_analyzer import RnDaoAnalyzer
from utils.daolytics_uitls import (
    get_mongo_credentials,
    get_saga_db_location,
)


def analyzer_recompute(guildId):
    analyzer_init = AnalyzerInit()
    analyzer = analyzer_init.get_analyzer()
    analyzer.recompute_analytics(guildId=guildId)

def analyzer_run_once(guildId):
    analyzer_init = AnalyzerInit()
    analyzer = analyzer_init.get_analyzer()
    analyzer.run_once(guildId=guildId)
    


 

class AnalyzerInit():
    """
    initialize the analyzer configs
    - MongoDB database
    - Neo4J database
    """

    def get_analyzer(self):
        """
        
        Returns:
        ---------
        analyzer : RnDaoAnalyzer

        
        """
        analyzer = RnDaoAnalyzer()
        mongo_creds = get_mongo_credentials()

        analyzer.set_mongo_database_info(
            mongo_db_host=mongo_creds["host"],
            mongo_db_password=mongo_creds["password"],
            mongo_db_port=mongo_creds["port"],
            mongo_db_user=mongo_creds["user"],
        )

        saga_mongo_location = get_saga_db_location()
        self._mongo_creds["db_name"] = saga_mongo_location["db_name"]
        self._mongo_creds["collection_name"] = saga_mongo_location["collection_name"]

        analyzer.set_neo4j_database_info(neo4j_creds=self._neo4j_creds)

        analyzer.database_connect()

        return analyzer
    

    # def get_mongo_connection(self, mongo_creds: dict[str, any]):
    #     user = mongo_creds["user"]
    #     password = mongo_creds["password"]
    #     host = mongo_creds["host"]
    #     port = mongo_creds["port"]

    #     connection = f"mongodb://{user}:{password}@{host}:{port}"

    #     return connection