import configparser
import os
from typing import Any, Iterator, Sequence, Type

from pydantic import BaseModel
from snowflake.snowpark.row import Row
from snowflake.snowpark import Session
from threading import local

threadlocal_data = local()


class Database:
    def __init__(self) -> None:
        self.config = {}
        config = configparser.ConfigParser()
        config.read(os.path.expanduser("~/.snowsql/config"))
        self.config = dict(
            account=os.getenv("SNOWFLAKE_ACCOUNT")
            or config["connections"]["accountname"],
            user=os.getenv("SNOWFLAKE_USER") or config["connections"]["username"],
            password=os.getenv("SNOWFLAKE_PASSWORD")
            or config["connections"]["password"],
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE")
            or config["connections"].get("warehousename"),
            database=os.getenv("SNOWFLAKE_DATABASE")
            or config["connections"].get("dbname"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
            or config["connections"].get("schemaname"),
        )
        session_builder = Session.builder.config("connection_name", "default")
        session_builder.configs(self.config)
        self.session = session_builder.create()

    @classmethod
    def get_instance(self) -> "Database":
        if not hasattr(threadlocal_data, "database_instance"):
            threadlocal_data.database_instance = Database()
        return threadlocal_data.database_instance

    def get_rows(self, sql: str, params: Sequence[Any] | None = None) -> Iterator[Row]:
        return self.session.sql(sql, params).collect()

    def query(
        self,
        model: Type[BaseModel],
        sql: str,
        params: Sequence[Any] | None = None,
    ) -> Iterator[BaseModel]:
        for row in self.session.sql(sql, params).collect():
            yield model.model_validate(row.as_dict())
