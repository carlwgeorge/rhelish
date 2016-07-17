from setuptools import setup


setup(
    name='rhelish',
    version='0.0.1',
    description='query package versions across RHEL, EPEL, and Fedora',
    author='Carl George',
    author_email='carl.george@rackspace.com',
    url='https://github.com/carlwgeorge/rhelish',
    packages=['rhelish'],
    package_dir={'': 'src'},
    install_requires=[
        'click',
        'configobj',
        'prettytable',
        'aiohttp',
        'aiofiles'
    ],
    entry_points={'console_scripts': ['rhelish=rhelish:cli']},
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ]
)
