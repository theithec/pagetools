import os

from setuptools import setup, find_packages


#from distutils.core import setup
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
from version import get_git_version
#find_packages(),
setup(
    name='django-pagetools',
    version=get_git_version(),
    #packages_dir={'':'pagetools'},
    #packages = [''],
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A set of Django apps to to provide some cms-like features',
    long_description=README,
    #url='http://www.example.com/',
    author='Tim Heithecker',
    author_email='tim.heithecker@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)