from setuptools import setup, find_packages

setup(
    name='flask-expects-json',
    version='0.0.1',
    description='Decorator for REST endpoints in flask. Validate JSON request data.',
    url='https://github.com/fischerfredl/flask-expects-json',
    author='Alfred Melch',
    author_email='alfred.melch@gmx.de',
    license='MIT',
    classifiers=[],
    keywords='',
    packages=find_packages(exclude=['tests.*', 'tests']),
    install_requires=['flask', 'jsonschema'],

    test_suite='tests.test_suite',
    tests_require=[],
)
