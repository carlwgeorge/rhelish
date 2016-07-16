import os

import click
from configobj import ConfigObj
from prettytable import PrettyTable

from rhelish import pkgdb, mdapi


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
    else:
        # display versions of package across Fedora and EPEL

        # initialize config
        config_home = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        config = ConfigObj('{}/{}.ini'.format(config_home, __name__))

        table = PrettyTable(['BRANCH', 'VERSION'])
        for branch in config['fedora']['branches']:
            version = mdapi.get_version(package, branch)
            if version:
                table.add_row([branch, version])

        table.sortby = 'BRANCH'
        click.echo(table)
