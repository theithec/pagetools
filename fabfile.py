from fabric.api import local, env
from fabric.api import lcd
from fabric.contrib import django




django.settings_module('project.settings')


def test():
    with lcd('demo'):
        local('python manage.py test main pagetools')

def push(skiptest=False):
    if not skiptest:
        test()
    local('git push origin -- master ')
    
def deploy(branch_name):
    test()
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)
    push()
    
    
def build():
    local('python setup.py sdist')

'''
from fabric.main import main

if __name__ == '__main__':
    import sys
    sys.argv = ['fab', '-f', __file__, 'update_server']
    main()
'''