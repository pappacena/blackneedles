import configparser
import os
from typing import Any, Iterator, Optional, Sequence, Type, TypeVar

from pydantic import BaseModel
from snowflake.snowpark.row import Row
from snowflake.snowpark import Session
from threading import local

threadlocal_data = local()

AnyModel = TypeVar("AnyModel", bound=BaseModel)


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
            role=os.getenv("SNOWFLAKE_ROLE") or config["connections"].get("rolename"),
        )
        session_builder = Session.builder.config("connection_name", "default")
        session_builder.configs(self.config)
        self.session = session_builder.create()

    @classmethod
    def get_instance(self) -> "Database":
        if not hasattr(threadlocal_data, "database_instance"):
            threadlocal_data.database_instance = Database()
        return threadlocal_data.database_instance

    def get_rows(
        self, sql: str, params: Optional[Sequence[Any]] = None
    ) -> Iterator[Row]:
        return self.session.sql(sql, params).collect()

    def query(
        self,
        model: Type[AnyModel],
        sql: str,
        params: Optional[Sequence[Any]] = None,
    ) -> Iterator[AnyModel]:
        for row in self.session.sql(sql, params).collect():
            yield model.model_validate(row.as_dict())
