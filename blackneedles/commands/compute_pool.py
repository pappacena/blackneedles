import typer

from blackneedles.console import print_table
from blackneedles.models.compute_pool import ComputePool

app = typer.Typer(short_help="Manage compute pools in Snowpark Container Services.")


@app.command("list")
def list_all(
    ctx: typer.Context,
):
    """Gives the list of compute pools and its current status"""
    compute_pool = list(ComputePool.objects.all())

    print_table(
        ctx,
        compute_pool,
        [
            "name",
            "state",
            lambda c: f"{c.min_nodes} / {c.max_nodes}",
            lambda c: str(c.active_nodes),
            "instance_family",
            lambda c: f"{c.num_services} / {c.num_jobs}",
            "owner",
            "application",
        ],
        [
            "Name",
            "State",
            "# of nodes",
            "Active nodes",
            "# Services / Jobs" "Types",
            "Num Services",
            "Owner",
            "App",
        ],
    )
