from re import A
from typing import Annotated, Any
import typer

from blackneedles.console import print_table
from blackneedles.models.service import Service

app = typer.Typer()


@app.command("list")
def list_all_services(
    ctx: typer.Context,
    schema: Annotated[
        str, typer.Option(help="The schema to list services from")
    ] = None,
    compute_pool: Annotated[
        str, typer.Option(
            "--compute-pool",
            help="The compute pool to list services from"
        )
    ] = None,
):
    services = Service.objects.from_namespace({
        "schema_name": schema,
        "compute_pool": compute_pool,
    })
    services = list(services)

    print_table(
        ctx,
        services,
        [
            "full_name",
            "name",
            "schema_name",
            "owner",
            "compute_pool",
            lambda s: str(s.min_instances),
            lambda s: str(s.max_instances),
            "status",
        ],
        [
            "ID",
            "Name",
            "Schema",
            "Owner",
            "Compute pool",
            "Min",
            "Max",
            "Status"
        ],
    )