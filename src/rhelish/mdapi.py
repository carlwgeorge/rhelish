import requests


api = 'https://apps.fedoraproject.org/mdapi'


def get_version(package, branch):
    """Find the version of a package in a branch."""

    # some minor remaps
    if branch == 'epel5':
        branch = 'dist-5E-epel'
    elif branch == 'epel6':
        branch = 'dist-6E-epel'

    url = '{}/{}/pkg/{}'.format(api, branch, package)
    response = requests.get(url)
    if response.ok:
        data = response.json()
        try:
            epoch = data['epoch']
            version = data['version']
            release = data['release']
        except KeyError:
            raise KeyError('unexpected json from {}'.format(response.url))
        return '{}:{}-{}'.format(epoch, version, release)
    else:
        return None
