import datetime
from functools import cached_property, lru_cache
import json
from re import I
from typing import Any, Callable, Iterable
from pydantic import BaseModel

from blackneedles.connection import Database


class Service(BaseModel):
    name: str
    database_name: str
    schema_name: str
    owner: str
    compute_pool: str
    dns_name: str | None
    min_instances: int
    max_instances: int
    auto_resume: bool
    created_on: datetime.datetime
    updated_on: datetime.datetime | None
    resumed_on: datetime.datetime | None
    comment: str | None
    owner_role_type: str | None
    query_warehouse: str | None
    is_job: bool = False

    class Config:
        frozen = True

    @property
    def full_name(self):
        return f"{self.schema_name}.{self.name}"

    @property
    def full_path(self):
        return f"{self.database_name}.{self.schema_name}.{self.name}"

    @cached_property
    def status(self) -> str:
        result = Database.get_instance().get_rows(
            "SELECT SYSTEM$GET_SERVICE_STATUS(?) as STATUS",
            (self.full_path,)
        )
        return json.loads(result[0].STATUS)[0]["status"]

    class objects:
        @classmethod
        def from_namespace(
            cls,
            filters: dict[str, Any],
        ) -> Iterable["Service"]:
            return cls.filter(
                lambda s: all(
                    getattr(s, key) == value
                    for key, value in filters.items()
                    if value is not None
                ),
            )

        @classmethod
        def all(cls) -> Iterable["Service"]:
            """List all services from the given database"""
            db = Database.get_instance()
            return db.query(
                Service,
                "CALL __blackneedles__.list_services(?)",
                (db.config["database"],)
            )

        @classmethod
        def filter(
            self,
            callable: Callable[["Service"], bool],
        ) -> Iterable["Service"]:
            """Filter services by the given callable"""
            for service in self.all():
                if callable(service):
                    yield service
