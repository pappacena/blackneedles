import datetime
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

    @property
    def full_name(self):
        return f"{self.schema_name}.{self.name}"

    @property
    def full_path(self):
        return f"{self.database_name}.{self.schema_name}.{self.name}"

    class objects:
        @classmethod
        def all(cls, database_name: str):
            """List all services from the given database"""
            return Database.get_instance().query(
                Service,
                f"CALL {database_name}.__blackneedles__.list_services(?)",
                (database_name,)
            )