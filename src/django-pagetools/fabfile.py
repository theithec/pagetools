from fabric.api import local
from fabric.api import lcd


def prepare_deployment(branch_name):
    with lcd('~/workspaces/python/django-pagetools/src/django-pagetools/pagetools/demo'):
        local('python manage.py test main pagetools')
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)