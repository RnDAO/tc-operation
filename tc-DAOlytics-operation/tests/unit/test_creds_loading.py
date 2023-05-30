from utils.daolytics_uitls import (
    get_mongo_credentials,
    get_neo4j_credentials,
    get_rabbit_mq_credentials,
    get_saga_db_location,
)


def test_mongo_creds_keys():
    """
    test whether the keys of dictionaries is created or not
    """
    mongo_creds = get_mongo_credentials()

    credential_keys = list(mongo_creds.keys())

    assert "user" in credential_keys
    assert "password" in credential_keys
    assert "host" in credential_keys
    assert "port" in credential_keys


def test_mongo_creds_values():
    mongo_creds = get_mongo_credentials()

    assert mongo_creds["user"] is not None
    assert mongo_creds["password"] is not None
    assert mongo_creds["host"] is not None
    assert mongo_creds["port"] is not None


def test_rabbit_creds_keys():
    rabbit_creds = get_rabbit_mq_credentials()

    credential_keys = list(rabbit_creds.keys())

    assert "broker_url" in credential_keys
    assert "port" in credential_keys
    assert "password" in credential_keys
    assert "username" in credential_keys


def test_rabbit_creds_values():
    rabbit_creds = get_rabbit_mq_credentials()

    assert rabbit_creds["broker_url"] is not None
    assert rabbit_creds["port"] is not None
    assert rabbit_creds["password"] is not None
    assert rabbit_creds["username"] is not None


def test_no4j_creds_keys():
    neo4j_creds = get_neo4j_credentials()

    credential_keys = list(neo4j_creds.keys())

    assert "user" in credential_keys
    assert "password" in credential_keys
    assert "db_name" in credential_keys
    assert "protocol" in credential_keys
    assert "port" in credential_keys
    assert "host" in credential_keys


def test_neo4j_creds_values():
    neo4j_creds = get_neo4j_credentials()

    assert neo4j_creds["user"] is not None
    assert neo4j_creds["password"] is not None
    assert neo4j_creds["protocol"] is not None
    assert neo4j_creds["port"] is not None
    assert neo4j_creds["db_name"] is not None
    assert neo4j_creds["host"] is not None


def test_saga_location():
    saga_creds = get_saga_db_location()

    assert "db_name" in saga_creds.keys()
    assert "collection_name" in saga_creds.keys()


def test_saga_location_values():
    saga_creds = get_saga_db_location()

    assert saga_creds["db_name"] is not None
    assert saga_creds["collection_name"] is not None
