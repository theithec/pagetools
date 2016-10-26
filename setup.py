import os

from setuptools import setup, find_packages

# from distutils.core import setup
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
from version import get_git_version

setup(
    name='django-pagetools',
    version=get_git_version(),
    packages=find_packages(exclude=("demo","demo.*")),
    include_package_data=True,
    license='BSD License',  # example license
    description='A set of Django apps to to provide some cms-like features',
    install_requires = [
        'django>=1.9, <1.10',
        'django-grappelli==2.8.1',
        'django-filebrowser==3.7.2',
        'django-mptt==0.8.6',
        'django-crispy-forms==1.6.0',
        #  'awesome-slugify=',
        'django-model-utils==2.5.2',
        'Pillow==3.3.1',
        'beautifulsoup4==4.5.1',
        'djangoajax==2.3.6',
        'django-sekizai==0.10.0',
        'django-debug-toolbar==1.5'
    ],

    long_description=README,
    author='Tim Heithecker',
    author_email='tim.heithecker@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
