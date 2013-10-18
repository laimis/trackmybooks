import os
import sys
import cgi

from google.appengine.ext.webapp import util

# Must set this env var before importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# from google.appengine.dist import use_library
# use_library('django', '1.1')

# Force Django to reload its settings.
from django.conf import settings
settings._target = None


import logging
import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch.dispatcher
import django.http

from google.appengine.api import mail

def log_exception(*args, **kwds):
  logging.exception('Exception in request:')

# Log errors.
#django.dispatch.dispatcher.connect(log_exception, django.core.signals.got_request_exception)

# Unregister the rollback event handler.
#django.dispatch.dispatcher.disconnect(
#    django.db._rollback_on_exception,
#    django.core.signals.got_request_exception
#)

from django.http import HttpResponse

import django.core.handlers.wsgi
app = django.core.handlers.wsgi.WSGIHandler()
