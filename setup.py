import os
from setuptools import setup, find_packages

from version import get_git_version

# from distutils.core import setup
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-pagetools',
    version=get_git_version(),
    packages=find_packages(exclude=("demo", "demo.*")),
    include_package_data=True,
    license='BSD License',  # example license
    description='A set of Django apps to to provide some cms-like features',
    install_requires=[
        'Django<=2.0',
        'beautifulsoup4>=4.7.1',
        'django-crispy-forms>=1.7.2',
        'django-debug-toolbar<=2.0',
        'django-filebrowser<=3.12',
        'django-grappelli<=2.13',
        'django-model-utils<4.0',
        'django-mptt>=0.10.0',
        'django-sekizai>=1.0.0',
        'django-simple-captcha>=0.5.12',
        'djangoajax<=3.0',
        'Pillow==6.0',
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
