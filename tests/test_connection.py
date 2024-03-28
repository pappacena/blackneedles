from unittest.mock import patch

from blackneedles.connection import Database


@patch("blackneedles.connection.Session")
@patch.dict(
    "os.environ",
    {
        "SNOWFLAKE_ACCOUNT": "accountname",
        "SNOWFLAKE_USER": "username",
        "SNOWFLAKE_PASSWORD": "password",
        "SNOWFLAKE_WAREHOUSE": "warehousename",
        "SNOWFLAKE_DATABASE": "dbname",
        "SNOWFLAKE_SCHEMA": "schemaname",
    },
)
def test_connection_building(session_cls):
    db = Database()
    assert db.config == {
        "account": "accountname",
        "user": "username",
        "password": "password",
        "warehouse": "warehousename",
        "database": "dbname",
        "schema": "schemaname",
    }
