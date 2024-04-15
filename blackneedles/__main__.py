from dataclasses import dataclass
from typing import Annotated, Literal, Optional
import typer
from blackneedles import db_install, db_uninstall

from blackneedles.commands import compute_pool, service


@dataclass
class GlobalParams:
    table_style: Literal["rich", "plain"]


app = typer.Typer()
app.add_typer(service.app, name="service")
app.add_typer(compute_pool.app, name="compute-pool")


@app.command("install")
def install_procedures(
    ctx: typer.Context,
    grant_target: Annotated[
        Optional[str], typer.Option(help="To whom should we grant permission?")
    ] = None,
):
    """Installs in database the procedures needed for monitoring services."""
    db_install(grant_target)


@app.command("uninstall")
def uninstall_procedures(
    ctx: typer.Context,
):
    """Removes from snowflake any procedures created by the install command."""
    db_uninstall()


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
