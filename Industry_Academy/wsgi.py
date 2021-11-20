"""
WSGI config for Industry_Academy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Industry_Academy.settings')

import sys
from os.path import join, dirname, abspath
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

from Industry_Academy.local_settings import virtualenv_path
sys.path.append(virtualenv_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()