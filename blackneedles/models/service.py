import datetime
from functools import cached_property
import json
from typing import Any, Callable, Iterable, Optional
from pydantic import BaseModel

from blackneedles.connection import Database


class Service(BaseModel):
    name: str
    database_name: str
    schema_name: str
    owner: str
    compute_pool: str
    dns_name: Optional[str]
    min_instances: int
    max_instances: int
    auto_resume: bool
    created_on: datetime.datetime
    updated_on: Optional[datetime.datetime]
    resumed_on: Optional[datetime.datetime]
    comment: Optional[str]
    owner_role_type: Optional[str]
    query_warehouse: Optional[str]
    is_job: bool = False
    spec: Optional[str] = None

    class Config:
        frozen = True

    @property
    def full_name(self):
        return f"{self.schema_name}.{self.name}"

    @full_name.setter
    def full_name(self, value: str):
        self.schema_name, self.name = value.split(".")

    @property
    def full_path(self):
        return f"{self.database_name}.{self.schema_name}.{self.name}"

    @full_path.setter
    def full_path(self, value: str):
        self.database_name, self.schema_name, self.name = value.split(".")

    @cached_property
    def status(self) -> str:
        result = list(
            Database.get_instance().get_rows(
                "CALL __blackneedles__.check_statuS(?)", (self.full_path,)
            )
        )[0]
        return json.loads(result.CHECK_STATUS)[0]["status"]

    def alter_status(self, status: str) -> None:
        status = status.upper()
        valid_status = ["SUSPEND", "RESUME"]
        if status not in valid_status:
            raise ValueError(
                f"Invalid status: {status}. Should be one of {valid_status}"
            )
        Database.get_instance().get_rows(
            "CALL __blackneedles__.alter_service(?, ?)", (self.full_path, status)
        )

    class objects:
        @classmethod
        def get(cls, service_name: str) -> "Service":
            db = Database.get_instance()
            return list(
                db.query(
                    Service,
                    "CALL __blackneedles__.describe_service(?);",
                    (service_name,),
                )
            )[0]

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
                (db.config["database"],),
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
