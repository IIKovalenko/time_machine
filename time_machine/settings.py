import os
from configurations import Configuration


class BaseSettings(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    SECRET_KEY = 'rh+v5cy7i3id%_kn6ljpzp0t&pu4#*f9fp=yr7wtlx-opia^ma'

    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'south',
        'rest_framework',

        'layout',
        'times',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'time_machine.urls'

    WSGI_APPLICATION = 'time_machine.wsgi.application'

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'

    TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

    LOGIN_URL = '/'
    LOGIN_REDIRECT_URL = '/profile/'

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        )
    }


class Dev(BaseSettings):
    DEBUG = True
    DATABASES = {
        'default': {
            'NAME': 'time_machine',
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'OPTIONS': {'init_command': 'SET storage_engine=INNODB'}
        }
    }


class Test(BaseSettings):
    DATABASES = {
        'default': {
            'NAME': ':memory:',
            'ENGINE': 'django.db.backends.sqlite3',
            'USER': '',
            'PASSWORD': '',
        }
    }
