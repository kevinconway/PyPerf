"""Setuptools packaging configuration for pyperf."""

from setuptools import setup
from setuptools import find_packages


with open('README.rst') as f:

    README = f.read()

setup(
    name='py-perf',
    version='0.0.1',
    url='https://github.com/kevinconway/PyPerf',
    license="Apache2",
    description='A service for profiling Python snippets.',
    author='Kevin Conway',
    author_email='kevinjacobconway@gmail.com',
    long_description=README,
    classifiers=[],
    packages=find_packages(exclude=['tests', 'build', 'dist', 'docs']),
    install_requires=[
        'psutil',
        'memory_profiler',
        'daemons',
        'six',
        'amqp',
        'stevedore',
        'confpy',
    ],
    entry_points={
        "pyperf_messages": [
            "profile_request = pyperf.messages:ProfileRequest",
            "profile_result = pyperf.messages:ProfileResult",
            "profile_failure = pyperf.messages:ProfileFailure",
        ],
        "console_scripts": [
            "pyperf-profile = pyperf.cmd.daemons:profiler_main",
            "pyperf-profile-send = pyperf.cmd.daemons:send_request",
            "pyperf-profile-fetch = pyperf.cmd.daemons:fetch_result",
            "pyperf-profile-err = pyperf.cmd.daemons:fetch_error",
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
