from dataclasses import dataclass
from typing import Annotated, Literal, Optional
import typer

from blackneedles.commands import service


@dataclass
class GlobalParams:
    table_style: Literal["rich", "plain"]


app = typer.Typer()
app.add_typer(service.app, name="service")


@app.command("install")
def install_procedures(
    ctx: typer.Context,
    grant: Annotated[
        Optional[str], typer.Option(help="Grant permissions to the procedures")
    ] = None,
):
    print(f"Granting permissions: {grant}")
    print("Not implemented yet... sorry!")
    raise Exception(":(")


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
