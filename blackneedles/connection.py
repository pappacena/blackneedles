import configparser
import os
from typing import Any, Iterator, List, Optional, Sequence, Type, TypeVar

from pydantic import BaseModel
from snowflake.snowpark.row import Row
from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSessionException
from snowflake.snowpark.context import get_active_session
from threading import local

threadlocal_data = local()

AnyModel = TypeVar("AnyModel", bound=BaseModel)


class Database:
    def __init__(self, session: Optional[Session] = None) -> None:
        if session is not None:
            self.session = session
            return
        try:
            self.session = get_active_session()
            return
        except SnowparkSessionException:
            pass
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

    @classmethod
    def set_instance(self, instance: "Database") -> None:
        threadlocal_data.database_instance = instance

    def get_rows(self, sql: str, params: Optional[Sequence[Any]] = None) -> List[Row]:
        return self.session.sql(sql, params).collect()

    def query(
        self,
        model: Type[AnyModel],
        sql: str,
        params: Optional[Sequence[Any]] = None,
    ) -> Iterator[AnyModel]:
        for row in self.session.sql(sql, params).collect():
            yield model.model_validate(row.as_dict())

    def use_database(self, database_name: str) -> None:
        self.session.use_database(database_name)
        self.session.use_schema("__blackneedles__")
