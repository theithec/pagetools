from fabric.api import local
from fabric.api import lcd


def prepare_deployment(branch_name):
    with lcd('~/workspaces/python/django-pagetools/pagetools/demo'):
        local('python manage.py test demo')
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)