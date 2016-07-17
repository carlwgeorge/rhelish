import aiohttp


pkgdb = 'https://admin.fedoraproject.org/pkgdb/api'


async def list_packages(query):
    """List packages containing the query string."""

    url = '{}/packages/*{}*'.format(pkgdb, query)
    response = await aiohttp.get(url)
    data = await response.json()

    return [pkg['name'] for pkg in data['packages']]
