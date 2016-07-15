import click


@click.command()
@click.argument('package')
def cli(package):
    click.echo(package)
