import requests


api = 'https://apps.fedoraproject.org/mdapi'


def get_version(package, branch):
    """Find the version of a package in a branch."""

    # some minor remaps
    if branch == 'epel5':
        branch = 'dist-5E-epel'
    elif branch == 'epel6':
        branch = 'dist-6E-epel'

    r = requests.get('{}/{}/pkg/{}'.format(api, branch, package))
    if r.ok:
        result = r.json()
        try:
            epoch = result['epoch']
            version = result['version']
            release = result['release']
            return '{}:{}-{}'.format(epoch, version, release)
        except KeyError:
            raise KeyError('unexpected json from {}'.format(r.url))
    else:
        return None
