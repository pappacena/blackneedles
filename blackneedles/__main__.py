from dataclasses import dataclass
import os
from typing import Annotated, Literal, Optional
import typer
import sqlparse  # type: ignore

from blackneedles.commands import service
from blackneedles.connection import Database


@dataclass
class GlobalParams:
    table_style: Literal["rich", "plain"]


app = typer.Typer()
app.add_typer(service.app, name="service")


@app.command("install")
def install_procedures(
    ctx: typer.Context,
    grant_target: Annotated[
        Optional[str], typer.Option(help="To whom should we grant permission?")
    ] = None,
):
    """Installs in database the procedures needed for monitoring services."""
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


@app.command("uninstall")
def uninstall_procedures(
    ctx: typer.Context,
    grant_target: Annotated[
        Optional[str], typer.Option(help="To whom should we grant permission?")
    ] = None,
):
    """Removes from snowflake any procedures created by the install command."""
    here = os.path.dirname(__file__)
    db = Database.get_instance()
    procedures_file = os.path.join(here, "procedures", "uninstall.sql")
    with open(procedures_file) as f:
        sql = f.read()
    for statement in sqlparse.split(sql):
        print(f"** Executing the following statement:\n{statement}")
        print(db.get_rows(statement))


@app.callback()
def global_options(
    ctx: typer.Context,
    table_style: Annotated[
        str, typer.Option("--table-style", help="Output table style")
    ] = "rich",
):
    if ctx.resilient_parsing:
        return
    if table_style not in ("rich", "plain"):
        raise typer.BadParameter("table-style must be either 'rich' or 'plain'")
    ctx.obj = GlobalParams(
        table_style=table_style,  # type: ignore
    )
