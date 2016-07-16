import os

import click
from configobj import ConfigObj


def do_info(package):
    urls = [
        'http://pkgs.fedoraproject.org/cgit/{}.git'.format(package),
        'https://admin.fedoraproject.org/pkgdb/package/{}'.format(package),
        'https://bodhi.fedoraproject.org/updates/?packages={}'.format(package),
        'http://koji.fedoraproject.org/koji/search?type=package&match=glob&terms={}'.format(package),
        'https://bugzilla.redhat.com/buglist.cgi?bug_status=NEW&bug_status=ASSIGNED&bug_status=ON_QA&component={}'.format(package)
    ]
    return '\n'.join(urls)


def do_search(package):
    from rhelish import pkgdb

    matches = pkgdb.name_search(package)
    return '\n'.join(matches)


def do_table(package):
    from prettytable import PrettyTable
    from rhelish import mdapi

    config_home = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
    config = ConfigObj('{}/{}.ini'.format(config_home, __name__))

    result = PrettyTable(['BRANCH', 'VERSION'])

    for branch in config['fedora']['branches']:
        version = mdapi.get_version(package, branch)
        result.add_row([branch, version])

    result.sortby = 'BRANCH'
    return result


@click.command()
@click.argument('package')
@click.option('--info', '-i', is_flag=True)
@click.option('--search', '-s', is_flag=True)
def cli(package, info, search):

    if info:
        result = do_info(package)

    elif search:
        result = do_search(package)

    else:
        result = do_table(package)

    click.echo(result)
