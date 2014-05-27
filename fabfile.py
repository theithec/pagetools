from fabric.api import local, env
from fabric.api import lcd

env.passwords={'github.com': 'ku8cheunu_iY'}
env.hosts = ['github.com']

def test():
    with lcd('demo'):
        local('python manage.py test main pagetools')


def deploy(branch_name):
    test()
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)
    local('git push orgin -- master ')
    
    
def build():
    local('python setup.py sdist')

'''
from fabric.main import main

if __name__ == '__main__':
    import sys
    sys.argv = ['fab', '-f', __file__, 'update_server']
    main()
'''