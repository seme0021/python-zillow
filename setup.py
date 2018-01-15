"""
The setup and build script for the python-zillow library.
"""

import os

from setuptools import setup, find_packages


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='python-zillow',
    version='0.2.0',
    author='The Python-Zillow Developers',
    author_email='python-zillow@googlegroups.com',
    license='Apache License 2.0',
    url='https://github.com/seme0021/python-zillow',
    download_url='https://github.com/seme0021/python-zillow/tarball/master',
    keywords=['zillow', 'api', 'real estate', 'python'],
    description='A Python wrapper around the Zillow API',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'requests',
        'xmltodict',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
