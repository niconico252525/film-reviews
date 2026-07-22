#!/usr/bin/env bash
set -o errexit
set -o pipefail

python -m pip install --disable-pip-version-check -r requirements-production.txt
python manage.py collectstatic --no-input
python manage.py check --deploy
python manage.py migrate --no-input
