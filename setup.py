import os
from setuptools import setup, find_packages

# from distutils.core import setup
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
from version import get_git_version

setup(
    name='django-pagetools',
    version=get_git_version(),
    packages=find_packages(exclude=("demo", "demo.*")),
    include_package_data=True,
    license='BSD License',  # example license
    description='A set of Django apps to to provide some cms-like features',
    install_requires=[
        'Django==1.11.2',
        'beautifulsoup4==4.6.0',
        'django-crispy-forms==1.7.0',
        'django-debug-toolbar==1.8',
        'django-filebrowser==4.1-dev',
        'django-grappelli==2.10.1',
        'django-model-utils==3.1.1',
        'django-mptt==0.9.0',
        'django-sekizai==0.10.0',
        'django-simple-captcha==0.5.6',
        'djangoajax==2.4.5',
        'Pillow==4.1.1',
    ],

    dependency_links=[
        'http://github.com/theithec/django-filebrowser/tarball/master#egg=django-filebrowser-4.1-dev',
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    test_suite="runtests.runtests",
)
