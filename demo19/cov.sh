#! /bin/bash
rm -rf .coverage htmlcov
coverage  run --source pagetools ./manage.py test pagetools
coverage html
chromium-browser htmlcov/index.html

