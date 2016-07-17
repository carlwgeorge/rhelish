import aiohttp


api = 'https://admin.fedoraproject.org/pkgdb/api'


async def name_search(query):
    """Search for a package name containing the query string."""

    url = '{}/packages/*{}*'.format(api, query)
    response = await aiohttp.get(url)
    data = await response.json()

    return [pkg['name'] for pkg in data['packages']]
