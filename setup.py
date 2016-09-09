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
        'django>=1.8',
        'django-grappelli>=2.7.3',
        'django-filebrowser>=3.6.4',
        #'django-mptt==0.8.6',
        'django-mptt',
        'django-crispy-forms',
        'django-model-utils',
        'Pillow',
        'beautifulsoup4',
        'djangoajax',
        'django-sekizai',
        'django-simple-captcha',
        'django-debug-toolbar'
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
    test_suite="runtests.runtests",
)
