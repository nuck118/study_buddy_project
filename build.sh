#!/usr/bin/env bash
set -o errexit

# Use pip instead of python -m pip to keep it clean
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
