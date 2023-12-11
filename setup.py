#!/usr/bin/env python
from setuptools import setup, find_packages  # noqa: F401
setup(
    name='requestbin',
    version='0.0.1',
    author='OldTyT',
    author_email='admin@oldtyt.xyz',
    description='HTTP request collector and inspector',
    zip_safe=False,
    include_package_data=True,
    python_requires='>=2.7',
    packages=['requestbin'],
    install_requires=[
        'gevent==1.0.2',
        'ProxyTypes==0.9',
        'nose==1.3.0',
        'wsgiref==0.1.2',
        'feedparser==5.1.3',
        'Flask==0.10.1',
        'Flask-Cors==3.0.2',
        'redis==2.7.6',
        'msgpack-python==0.1.12',
        'python-dateutil==2.1',
        'gunicorn==19.9.0',
        'bugsnag==3.4.2',
        'blinker==1.4',
        'Werkzeug==0.9.3',
        'itsdangerous==0.24',
        'Jinja2==2.7',
        'MarkupSafe==1.0',
        'six==1.16.0'
    ],
)