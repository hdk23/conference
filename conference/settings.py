"""
Django settings for conference project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1b$jt1d259j@%l)l!i9t&7%c%m-xxjrip4cs5ec)_uvykbt+n&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
# remove non-UN members from list
to_remove ={
    'AQ',	'NF',	'HM',	'CC',	'CX',	'JE',	'IM',	'GG',	'MO',	'HK',	'GL',	'FO',	'EH',	'TW',	'AX',	'WF',	'PM',	'MF',	'BL',	'RE',	'NC',	'YT',	'MQ',	'GP',	'TF',	'PF',	'GF',	'SX',	'CW',	'BQ',	'AW',	'TK',	'NU',	'CK',	'SJ',	'BV',	'VG',	'TC',	'GS',	'SH',	'PN',	'MS',	'GI',	'FK',	'KY',	'IO',	'BM',	'AI',	'VI',	'UM',	'PR',	'MP',	'GU',	'AS'
}

COUNTRIES_OVERRIDE = {
    'US': {'names': [_('United States'), _('US'), _('USA'), _('United States of America')]},
    'RU': {'names': [_('Russia'), _('Russian Federation')]},
    'GB': {'names': [_('United Kingdom'), _('UK')]},
    'AE': {'names': [_('United Arab Emirates'), _('UAE')]},
    'CD': {'names': [_('DR Congo'), _('Democratic Republic of the Congo')]},
}

for remove in to_remove:
    COUNTRIES_OVERRIDE[remove] = None


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dartmun',
    'accounts',
    'django_countries'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conference.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conference.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '../../dartmun/'
LOGOUT_REDIRECT_URL = '../../dartmun/'