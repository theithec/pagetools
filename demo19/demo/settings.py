"""
Django settings for demo project.

Generated by 'django-admin startproject' using Django 1.9.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#c##*+s7^=1m^p-=m&fvs8v(8p&#esxlqbq_3i+v(5)4z3ud)@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'grappelli.dashboard',  # optional (pagetools provides two dashboard modules),
                            # needs further configuration
    'grappelli',            # required
    'filebrowser',          # required
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # required for search
    'crispy_forms',      # required for pages
    'sekizai',           # required for sections. Needs further configuration
    'polls',
    'main.apps.MainConfig',
    'pagetools.core',    # needed for all pagetools modules
    'pagetools.widgets', # Widgets (e.g. for sidebars)
    'pagetools.pages',   # Simple Pages
    'pagetools.menus',   #
    'pagetools.sections',# Nested Content (e.g. for a singlepage site)
    'pagetools.sections.tests',
    'pagetools.search',  # Simple Search on database fields
    'pagetools.subscriptions',  # Subscriptions to whatever
    'behave_django',
    #'debug_toolbar',
]

SITE_ID = 1  # required by contrib.sites


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'pagetools.widgets.context_processors.pagetype_from_view',
            ],
        },
    },
]

WSGI_APPLICATION = 'demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/debug.log',
        },
    },
    'loggers': {
        'pagetools': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'



PT_TEMPLATETAG_WIDGETS = {
    'subscribe':
        'pagetools.subscriptions.templatetags.subscriptions_tags.NewsSubscribtionNode',
    'latest_question': 'main.templatetags.LatestQuestionNode',
}
PT_MENU_TEMPLATE = 'foundation6_nav_menu.html'
