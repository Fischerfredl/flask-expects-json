from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read


setup(
    name='flask-expects-json',
    description='Decorator for REST endpoints in flask. Validate request data and store in g',
    long_description=readme(),
    url='https://github.com/fischerfredl/flask-expects-json',
    download_url='https://github.com/fischerfredl/flask-expects-json/archive/0.1.tar.gz',

    version='0.1',
    license='MIT',

    author='Alfred Melch',
    author_email='alfred.melch@gmx.de',

    packages=find_packages(exclude=['tests.*', 'tests']),

    # dependencies
    install_requires=['flask', 'jsonschema'],
    dependency_links=[],

    test_suite='tests.test_suite',
    tests_require=[],
)
