#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python loan_project/manage.py migrate
python loan_project/manage.py collectstatic --noinput
