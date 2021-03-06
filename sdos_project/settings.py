import os
import dj_database_url
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.contrib.messages import constants

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SDOS_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (int(os.environ.get('SDOS_PRODUCTION_SERVER')) == 0)

ALLOWED_HOSTS = [
	'researchmentoringplatform.herokuapp.com',
	'127.0.0.1',
	'localhost',
]


# Application definition

INSTALLED_APPS = [
	# API
	'api',

	# Custom apps
	'users',
	'home',
	'mentor_mentee',

	# Crispy Forms
	'crispy_forms',

	# Confirmation Mail
	# 'simple_email_confirmation',

	# Django default apps
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

# Email confirmation
# EMAIL_CONFIRMATION_PERIOD_DAYS = 7
# SIMPLE_EMAIL_CONFIRMATION_PERIOD = timedelta(days=EMAIL_CONFIRMATION_PERIOD_DAYS)

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'sdos_project.urls'

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

WSGI_APPLICATION = 'sdos_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
# 	'default': {
# 		'ENGINE': 'django.db.backends.sqlite3',
# 		'NAME': BASE_DIR / 'db.sqlite3',
# 	}
# }

DATABASES = {
	'default': dj_database_url.parse(os.environ.get('SDOS_DB'), conn_max_age=600)
}


AUTH_USER_MODEL = 'users.User'


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# Was set to False from True on Nov 20, 2020 at 2 AM, and set back to True minutes after


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Created 'static' folder at the level of all the apps to get this to work
# This global variable may not be needed
STATICFILES_DIRS = (BASE_DIR / 'static', )


LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'homepage'


# EMail Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_USERNAME', None)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', None)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'SDOS Team'


LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'simple': {
			'format': '[{asctime}] {levelname} module:[{module}] {message}',
			'style': '{',
			'datefmt': '%d/%b/%Y %H:%M:%S'
		},
		'verbose': {
			'format': '{asctime} {levelname} location:[{pathname}:{lineno}] thread:[{threadName}] {message}',
			'style': '{',
			'datefmt': '%d/%b/%Y %H:%M:%S'
		}
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
		'file': {
			'level': 'WARNING',
			'class': 'logging.FileHandler',
			'filename': 'warning.log',
			'formatter': 'verbose'
		}
	},
	'loggers': {
		'app': {
			'handlers': ['console', 'file'],
			'level': 'DEBUG',
		},
		'django': {
			'handlers': ['console', 'file'],
			'level': 'INFO'
		}
	},
}

# Messages Framework
MESSAGE_TAGS = {
	constants.DEBUG: 'alert-info',
	constants.INFO: 'alert-info',
	constants.SUCCESS: 'alert-success',
	constants.WARNING: 'alert-warning',
	constants.ERROR: 'alert-danger',
}

if int(os.environ.get('SDOS_PRODUCTION_SERVER')) == 1:
	SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
	SECURE_SSL_REDIRECT = True
