import os
from codecs import open

from setuptools import find_packages, setup


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION = __import__('journald_exporter_plugins').__version__


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='prometheus-journald-exporter-plugins',
    version=VERSION,
    description='Plugins for Prometheus Journald Exporter.',
    long_description=readme(),
    url='https://github.com/moccu/prometheus-journald-exporter-plugins',
    project_urls={
        'Bug Reports': 'https://github.com/moccu/prometheus-journald-exporter-plugins/issues',
        'Source': 'https://github.com/moccu/prometheus-journald-exporter-plugins',
    },
    author='Andreas Hug',
    author_email='andreas.hug@moccu.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'prometheus-client',
        'python-dateutil',
        'pytz',
    ],
    extras_require={},
    include_package_data=True,
    keywords='prometheus metrics journald logs',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
