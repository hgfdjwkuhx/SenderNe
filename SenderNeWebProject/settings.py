"""
Django settings for SenderNeWebProject project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import posixpath
from os import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '90ea97fa-a856-4b40-bee1-041f1d6ecb1e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = [u'hvsgkd.herokuapp.com']
ALLOWED_HOSTS = ['*']



# Application definition

INSTALLED_APPS = [
    'app',
    'SenderNeClientAPI',



    'forms_builder.forms',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    # therd part
    'crispy_forms',
    'registration',
    #'country_dialcode',

    ######################
    'django_bulk_update',

    ########## rest framework #########
    'rest_framework',
    'rest_framework.authtoken', # new!
    'rest_auth', # new!




    ####### Channels ############
    'debug_toolbar',


    "gunicorn",
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}


'''
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
'''

MIDDLEWARE = [
    ####### Channels ############

    'debug_toolbar.middleware.DebugToolbarMiddleware',

    ####### Base ############

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SenderNeWebProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'SenderNeWebProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Define the database manager to setup the various projects
DATABASE_ROUTERS = [


                    ]

DATABASE_APPS_MAPPING = {



}

MAP_APPS_TO_DB = {


}

#postgres://user:pass@localhost/dbname
#DATABASE_URL: postgres://mkigesztkwaiqa:075d7a98e8c8b4fde6e9d9a5211dc31506c17689060c07ead092c0d3ce3ee251@ec2-50-17-203-51.compute-1.amazonaws.com:5432/d3trujo4q0vl5p
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_heroku_db_name',
        'USER': 'your_heroku_db_user_name',
        'PASSWORD': 'your_heroku_password',
        'HOST': 'ec2-23-21-133-106.compute-1.amazonaws.com', # Or something like this
        'PORT': '5432',
    }
}
'''

#'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd3trujo4q0vl5p',
        'USER': 'mkigesztkwaiqa',
        'PASSWORD': '075d7a98e8c8b4fde6e9d9a5211dc31506c17689060c07ead092c0d3ce3ee251',
        'HOST': 'ec2-50-17-203-51.compute-1.amazonaws.com', # Or something like this
        'PORT': '5432',
    }
}

'''


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


'''

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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))



#CRISPY_TEMPLATE_PACK = 'uni_form'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.

SITE_ID = 1
LOGIN_REDIRECT_URL='/'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format':
                '%(levelname)s %(asctime)s %(module)s'
                ' %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django_private_chat': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'custom_app': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}
#INTERNAL_IPS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ['*']
SESSION_COOKIE_AGE = 12096000
LOGIN_REDIRECT_URL = '/admin/'


