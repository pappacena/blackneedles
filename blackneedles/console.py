from typing import Callable, List, Optional, Union
import typer

from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from blackneedles.connection import AnyModel


def print_table(
    ctx: typer.Context,
    data: List[AnyModel],
    attributes: List[Union[str, Callable[[AnyModel], str], str]],
    headers: List[str],
    title: Optional[str] = None,
) -> None:
    with Progress() as progress:
        if ctx.obj.table_style == "rich":
            table = Table(title=title)
            task = progress.add_task("Loading...", total=len(data))
        else:
            table = Table(
                title=title,
                box=None,
                show_header=True,
                show_edge=False,
                show_lines=False,
            )
            task = None

        for header in headers:
            table.add_column(header)
        for row in data:
            values = []
            for val in attributes:
                if not isinstance(val, str):
                    values.append(val(row))
                else:
                    values.append(getattr(row, val))
            table.add_row(*values)
            if task is not None:
                progress.advance(task)
    console = Console()
    console.print(table)
