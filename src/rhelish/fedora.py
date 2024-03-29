import asyncio

import aiohttp

import rhelish


pkgdb = 'https://admin.fedoraproject.org/pkgdb/api'
mdapi = 'https://apps.fedoraproject.org/mdapi'


async def list_packages(query):
    """List packages containing the query string."""

    url = '{}/packages/*{}*'.format(pkgdb, query)
    response = await aiohttp.get(url)
    data = await response.json()

    return [pkg['name'] for pkg in data['packages']]


async def get_evr(package, branch):

    # some minor remaps
    if branch == 'epel5':
        branch = 'dist-5E-epel'
    elif branch == 'epel6':
        branch = 'dist-6E-epel'

    url = '{}/{}/pkg/{}'.format(mdapi, branch, package)
    response = await aiohttp.get(url)
    if response.status != 200:
        response.close()
        return None

    data = await response.json()
    epoch = data['epoch']
    version = data['version']
    release = data['release']

    return '{}:{}-{}'.format(epoch, version, release)


async def get_evrs(package):

    try:
        branches = rhelish.config['fedora']['branches']
    except KeyError:
        raise SystemExit('cannot parse \'branches\' from \'fedora\' section of config')

    tasks = [
        asyncio.ensure_future(get_evr(package, branch))
        for branch in branches
    ]
    await asyncio.wait(tasks)
    results = [task.result() for task in tasks]

    return zip(branches, results)
