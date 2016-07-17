import os
import asyncio

import click
from configobj import ConfigObj

from rhelish.fedora import list_packages
from rhelish.table import get_table


# setup config
config_home = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
config = ConfigObj('{}/{}.ini'.format(config_home, __name__))

# setup cache
cache_home = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
cache_dir = '{}/{}'.format(cache_home, __name__)
os.makedirs(cache_dir, exist_ok=True)


def get_links(package):
    return [
        'http://pkgs.fedoraproject.org/cgit/{}.git'.format(package),
        'https://admin.fedoraproject.org/pkgdb/package/{}'.format(package),
        'https://bodhi.fedoraproject.org/updates/?packages={}'.format(package),
        'http://koji.fedoraproject.org/koji/search?type=package&match=glob&terms={}'.format(package),
        'https://bugzilla.redhat.com/buglist.cgi?bug_status=NEW&bug_status=ASSIGNED&bug_status=ON_QA&component={}'.format(package)
    ]


@click.command()
@click.argument('package')
@click.option('--links', '-l', 'action_links', is_flag=True)
@click.option('--search', '-s', 'action_search', is_flag=True)
def cli(package, action_links, action_search):
    if action_links:
        # simple action
        links = get_links(package)
        output = '\n'.join(links)
    else:
        # async actions
        loop = asyncio.get_event_loop()
        if action_search:
            # search for package names
            matches = loop.run_until_complete(list_packages(package))
            output = '\n'.join(matches)
        else:
            # find all versions across Fedora, EPEL, and RHEL
            output = loop.run_until_complete(get_table(package))
        loop.close()

    click.echo(output)
