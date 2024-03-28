import typer

from blackneedles.console import print_table
from blackneedles.models import Service

app = typer.Typer()


@app.command()
def list(ctx: typer.Context):
    services = Service.objects.all(ctx.obj.app_name)
    print_table(
        ctx,
        services,
        [
            "full_name",
            "name",
            "schema_name",
            "owner",
            "compute_pool",
            (str, "min_instances"),
            (str, "max_instances")
        ],
        ["ID", "Name", "Schema", "Owner", "Compute pool", "min", "max"],
        "Services"
    )