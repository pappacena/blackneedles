from typing import List
from pydantic import BaseModel
import typer

from rich.console import Console
from rich.table import Table


def print_table(
    ctx: typer.Context,
    data: List[BaseModel],
    attributes: List[str],
    headers: List[str],
    title: str | None,
) -> None:
    if ctx.obj.table_style == "rich":
        table = Table(title=title)
    else:
        table = Table(
            title=title,
            box=None,
            show_header=True,
            show_edge=False,
            show_lines=False,
        )

    for header in headers:
        table.add_column(header)
    for row in data:
        values = []
        for val in attributes:
            if isinstance(val, tuple):
                values.append(val[0](getattr(row, val[1])))
            else:
                values.append(getattr(row, val))
        table.add_row(*values)
    console = Console()
    console.print(table)