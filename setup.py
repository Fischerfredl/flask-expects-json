from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='flask-expects-json',
    version='1.0.0',
    description='Decorator for REST endpoints in flask. Validate JSON request data.',
    long_description=readme(),
    url='https://github.com/fischerfredl/flask-expects-json',
    author='Alfred Melch',
    author_email='alfred.melch@gmx.de',
    license='MIT',
    classifiers=[
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'

    ],
    keywords=['flask', 'json', 'validation', 'schema'],
    packages=find_packages(exclude=['tests.*', 'tests']),
    install_requires=[
        'flask>=0.12.2',
        'jsonschema>=2.6.0'
    ],

    test_suite='tests.test_suite',
    tests_require=[],
)
