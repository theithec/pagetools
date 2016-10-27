#! /bin/bash
rm -rf .coverage htmlcov
coverage  run --source pagetools ./manage.py test pagetools main -v3
coverage html
chromium-browser htmlcov/index.html

