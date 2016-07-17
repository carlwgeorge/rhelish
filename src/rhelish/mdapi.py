import aiohttp


api = 'https://apps.fedoraproject.org/mdapi'


async def get_evr(package, branch):
    """Get the epoch:version-release string of a package in a Fedora branch."""

    # some minor remaps
    if branch == 'epel5':
        branch = 'dist-5E-epel'
    elif branch == 'epel6':
        branch = 'dist-6E-epel'

    url = '{}/{}/pkg/{}'.format(api, branch, package)
    response = await aiohttp.get(url)
    if response.status != 200:
        response.close()
        return None

    data = await response.json()
    epoch = data['epoch']
    version = data['version']
    release = data['release']

    return '{}:{}-{}'.format(epoch, version, release)
