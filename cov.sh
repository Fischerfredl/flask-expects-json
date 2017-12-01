#!/usr/bin/env bash
# installs the coverage tool and runs coverage
# reports to command-line and to htmlcov

set -e

pip install coverage
coverage run --source=flask_expects_json --branch setup.py test
coverage report -m
coverage html
