"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# 1. Calculate the absolute path to your 'src' directory
SRC_DIR = Path(__file__).resolve().parent.parent

# 2. FORCE Python to search the 'src' directory FIRST
sys.path.insert(0, str(SRC_DIR))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# 3. Vercel's serverless functions specifically look for a variable named 'app'
app = application