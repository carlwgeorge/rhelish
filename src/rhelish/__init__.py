import os
import asyncio

import click
from configobj import ConfigObj
from prettytable import PrettyTable

from rhelish import pkgdb, mdapi


# setup config
config_home = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
config = ConfigObj('{}/{}.ini'.format(config_home, __name__))

# setup cache
cache_home = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
cache_dir = '{}/{}'.format(cache_home, __name__)
os.makedirs(cache_dir, exist_ok=True)


def do_info(package):
    urls = [
        'http://pkgs.fedoraproject.org/cgit/{}.git'.format(package),
        'https://admin.fedoraproject.org/pkgdb/package/{}'.format(package),
        'https://bodhi.fedoraproject.org/updates/?packages={}'.format(package),
        'http://koji.fedoraproject.org/koji/search?type=package&match=glob&terms={}'.format(package),
        'https://bugzilla.redhat.com/buglist.cgi?bug_status=NEW&bug_status=ASSIGNED&bug_status=ON_QA&component={}'.format(package)
    ]
    return '\n'.join(urls)


async def do_search(package):
    matches = await pkgdb.name_search(package)
    return '\n'.join(matches)


async def do_table(package):
    config_home = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
    config = ConfigObj('{}/{}.ini'.format(config_home, __name__))
    branches =  config['fedora']['branches']
    output = PrettyTable(['BRANCH', 'VERSION'])

    tasks = [
        asyncio.ensure_future(mdapi.get_evr(package, branch))
        for branch in branches
    ]
    await asyncio.wait(tasks)
    results = [task.result() for task in tasks]

    for pair in zip(branches, results):
        output.add_row(pair)

    output.sortby = 'BRANCH'
    return output


@click.command()
@click.argument('package')
@click.option('--info', '-i', is_flag=True)
@click.option('--search', '-s', is_flag=True)
def cli(package, info, search):
    if info:
        output = do_info(package)
    else:
        loop = asyncio.get_event_loop()
        if search:
            output = loop.run_until_complete(do_search(package))
        else:
            output = loop.run_until_complete(do_table(package))
        loop.close()
    click.echo(output)
