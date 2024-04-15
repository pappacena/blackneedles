import os
from typing import Optional

import sqlparse  # type: ignore

from blackneedles.connection import Database


def db_install(grant_target: Optional[str] = None) -> None:
    here = os.path.dirname(__file__)
    db = Database.get_instance()
    procedures_file = os.path.join(here, "procedures", "monitoring_procedures.sql")
    with open(procedures_file) as f:
        sql = f.read()
    for statement in sqlparse.split(sql):
        print(f"** Executing the following statement:\n{statement}")
        print(db.get_rows(statement))

    if grant_target is not None:
        print(f"Granting permissions: {grant_target}")
        grant_file = os.path.join(here, "procedures", "grant_permissions.sql")
        with open(grant_file) as f:
            sql = f.read()
        for statement in sqlparse.split(sql):
            statement = statement.format(grant_target=grant_target)
            print(f"** Executing the following statement:\n{statement}")
            print(db.get_rows(statement))


def db_uninstall() -> None:
    here = os.path.dirname(__file__)
    db = Database.get_instance()
    procedures_file = os.path.join(here, "procedures", "uninstall.sql")
    with open(procedures_file) as f:
        sql = f.read()
    for statement in sqlparse.split(sql):
        print(f"** Executing the following statement:\n{statement}")
        print(db.get_rows(statement))
