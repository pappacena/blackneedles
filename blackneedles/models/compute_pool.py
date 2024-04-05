import datetime
from typing import Callable, Iterable, Optional
from pydantic import BaseModel

from blackneedles.connection import Database


class ComputePool(BaseModel):
    name: str
    state: str
    min_nodes: int
    max_nodes: int
    instance_family: str
    num_services: int
    num_jobs: int
    auto_suspend_secs: int
    auto_resume: bool
    active_nodes: int
    idle_nodes: int
    created_on: datetime.datetime
    resumed_on: Optional[datetime.datetime]
    updated_on: Optional[datetime.datetime]
    owner: str
    comment: Optional[str]
    is_exclusive: bool
    application: Optional[str]

    class Config:
        frozen = True

    class objects:
        @classmethod
        def all(cls) -> Iterable["ComputePool"]:
            """List all services from the given database"""
            db = Database.get_instance()
            return db.query(ComputePool, "SHOW COMPUTE POOLS")

        @classmethod
        def filter(
            self,
            callable: Callable[["ComputePool"], bool],
        ) -> Iterable["ComputePool"]:
            """Filter compute pool by the given callable"""
            for service in self.all():
                if callable(service):
                    yield service
