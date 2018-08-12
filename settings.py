import os

DEBUG = False
ROOT_URLCONF = 'urls'
APPEND_SLASH = False

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'customexceptions.ExceptionHandler'
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
)

ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    ROOT_PATH + '/templates',
)