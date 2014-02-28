from setuptools import setup
from setuptools import find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='py-perf',
    version='0.0.1',
    url='https://github.com/rackerlabs/PyPerf',
    license=license,
    description='ZeroVM driven Python profiling environment.',
    author='Kevin Conway',
    author_email='kevinjacobconway@gmail.com',
    long_description=readme,
    classifiers=[],
    packages=find_packages(exclude=['tests', 'build', 'dist', 'docs']),
    install_requires=[
        'memory_profiler',
    ]
)
