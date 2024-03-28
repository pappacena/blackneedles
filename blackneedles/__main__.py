from dataclasses import dataclass
from typing import Annotated, Literal
import typer

from blackneedles.commands import service


@dataclass
class GlobalParams:
    app_name: str
    table_style: Literal["rich", "plain"]


app = typer.Typer()
app.add_typer(service.app, name="service")


@app.callback()
def global_options(
    ctx: typer.Context,
    app_name: Annotated[str, typer.Option("--app-name", help="The database or native app name")],
    table_style: Annotated[str, typer.Option("--table-style", help="Output table style")] = "rich",
):
    if ctx.resilient_parsing:
        return
    if table_style not in ("rich", "plain"):
        raise typer.BadParameter("table-style must be either 'rich' or 'plain'")
    if not app_name:
        raise typer.BadParameter("--app-name is required")
    ctx.obj = GlobalParams(
        app_name=app_name,
        table_style=table_style
    )