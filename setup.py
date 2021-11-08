from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='flask-expects-json',
    version='1.7.0',
    description='Decorator for REST endpoints in flask. Validate JSON request data.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/fischerfredl/flask-expects-json',
    author='Alfred Melch',
    author_email='dev@melch.pro',
    license='MIT',
    classifiers=[
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['flask', 'json', 'validation', 'schema', 'jsonschema'],
    packages=find_packages(exclude=['tests.*', 'tests']),
    install_requires=[
        'flask>=1.0.2',
        'jsonschema>=3.0.1'
    ],
    extras_require={
        "async": ["flask[async]>=2.0.0"],
    },
    test_suite='tests.test_suite'
)
