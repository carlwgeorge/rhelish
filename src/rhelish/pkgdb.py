import requests


api = 'https://admin.fedoraproject.org/pkgdb/api'


def name_search(query):
    """Search for a package name containing the query string."""
    r = requests.get('{}/packages/*{}*'.format(api, query))
    if r.ok:
        try:
            return [pkg['name'] for pkg in r.json()['packages']]
        except KeyError:
            raise SystemExit('unable to parse json from {}'.format(r.url))
    else:
        raise SystemExit('{} returned a {} status'.format(r.url, r.status_code))
