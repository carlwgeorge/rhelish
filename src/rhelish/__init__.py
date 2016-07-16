import click

from rhelish import pkgdb


@click.command()
@click.argument('package')
@click.option('--search', '-s', is_flag=True)
def cli(package, search):
    if search:
        # search Fedora pkgdb for package
        results = pkgdb.name_search(package)
        click.echo('\n'.join(results))
