from setuptools import setup
from setuptools import find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyperf-profile',
    version='0.0.1',
    url='https://github.com/PyPerf/pyperf-profile',
    license=license,
    description='Standard interface for python profilers.',
    author='Kevin Conway',
    author_email='kevinjacobconway@gmail.com',
    long_description=readme,
    classifiers=[],
    packages=find_packages(exclude=['tests', 'build', 'dist', 'docs']),
    install_requires=[
        'memory_profiler',
    ]
)
