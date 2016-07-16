import click

from rhelish import pkgdb


@click.command()
@click.argument('package')
@click.option('--search', '-s', is_flag=True)
@click.option('--info', '-i', is_flag=True)
def cli(package, search, info):
    if search:
        # search Fedora pkgdb for package
        results = pkgdb.name_search(package)
        click.echo('\n'.join(results))
    elif info:
        # display helpful links for package
        urls = [
            'http://pkgs.fedoraproject.org/cgit/{}.git'.format(package),
            'https://admin.fedoraproject.org/pkgdb/package/{}'.format(package),
            'https://bodhi.fedoraproject.org/updates/?packages={}'.format(package),
            'http://koji.fedoraproject.org/koji/search?type=package&match=glob&terms={}'.format(package),
            'https://bugzilla.redhat.com/buglist.cgi?bug_status=NEW&bug_status=ASSIGNED&bug_status=ON_QA&component={}'.format(package)
        ]
        click.echo('\n'.join(urls))
