import configparser
import os
from typing import Any, Iterator, Optional, Sequence, Type

from pydantic import BaseModel
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import (
    SnowparkSessionException,
)


class Database:
    instance: Optional["Database"] = None

    def __init__(self) -> None:
        try:
            self.session = get_active_session()
        except SnowparkSessionException:
            config = configparser.ConfigParser()
            config.read(os.path.expanduser("~/.snowsql/config"))
            session_builder = Session.builder.config("connection_name", "default")
            session_builder.configs(
                dict(
                    account=config["connections"]["accountname"],
                    user=config["connections"]["username"],
                    password=config["connections"]["password"],
                    warehouse=config["connections"].get("warehousename"),
                    database=config["connections"].get("dbname"),
                    schema=config["connections"].get("schemaname"),
                )
            )
            self.session = session_builder.create()

    @classmethod
    def get_instance(self) -> "Database":
        if not self.instance:
            self.instance = Database()
        return self.instance

    def query(
        self,
        model: Type[BaseModel],
        sql: str,
        params: Sequence[Any] | None = None,
    ) -> Iterator[BaseModel]:
        for row in self.session.sql(sql, params).collect():
            yield model.model_validate(row.as_dict())
