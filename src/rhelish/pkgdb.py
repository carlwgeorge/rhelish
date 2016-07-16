import requests


api = 'https://admin.fedoraproject.org/pkgdb/api'


def name_search(query):
    """Search for a package name containing the query string."""

    url = '{}/packages/*{}*'.format(api, query)
    response = requests.get(url)
    if response.ok:
        data = response.json()
        try:
            return [pkg['name'] for pkg in data['packages']]
        except KeyError:
            raise SystemExit('unable to parse json from {}'.format(response.url))
    else:
        raise SystemExit('{} returned a {} status'.format(response.url, response.status_code))
