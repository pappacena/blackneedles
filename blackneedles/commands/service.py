from typing import Annotated, List, Optional
import typer

from blackneedles.console import print_table
from blackneedles.models.service import Service

app = typer.Typer(short_help="Manage services in Snowpark Container Services.")


@app.command("list")
def list_all_services(
    ctx: typer.Context,
    schema: Annotated[
        Optional[str], typer.Option(help="The schema to list services from")
    ] = None,
    compute_pool: Annotated[
        Optional[str],
        typer.Option("--compute-pool", help="The compute pool to list services from"),
    ] = None,
):
    """Gives the list of services and its current status"""
    services = Service.objects.from_namespace(
        {
            "schema_name": schema,
            "compute_pool": compute_pool,
        }
    )
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
        ["ID", "Name", "Schema", "Owner", "Compute pool", "Min", "Max", "Status"],
    )


@app.command("describe")
def describe_service(
    ctx: typer.Context,
    service_names: Annotated[
        List[str], typer.Argument(..., help="The name of the service to describe")
    ],
):
    """Describe a given service name."""
    services = [Service.objects.get(name) for name in service_names]
    print_table(
        ctx,
        services,
        [
            "full_path",
            "compute_pool",
            "status",
            "spec",
        ],
        [
            "ID",
            "Compute pool" "Status",
            "spec",
        ],
    )


@app.command("alter")
def alter_status(
    ctx: typer.Context,
    service_name: Annotated[
        str, typer.Argument(..., help="The name of the service to describe")
    ],
    action: Annotated[
        str, typer.Argument(..., help="Service state to change [SUSPEND, RESUME]")
    ],
):
    """Changes the status of a given service."""
    service = Service.objects.get(service_name)
    service.alter_status(action)
    typer.echo(f"Service {service_name} is now {action}")
