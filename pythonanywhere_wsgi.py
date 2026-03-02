# ============================================================
# PythonAnywhere WSGI Configuration File
# ============================================================
#
# Instructions:
# 1. Go to PythonAnywhere Web tab
# 2. Click on WSGI configuration file link
# 3. DELETE ALL existing content
# 4. COPY this entire file content and paste there
# 5. REPLACE 'yourusername' with your actual PythonAnywhere username
# 6. Save the file
#
# ============================================================

import os
import sys

# ============================================================
# IMPORTANT: Replace 'yourusername' with your actual username
# ============================================================
path = '/home/yourusername/notes-sharing-platform'
if path not in sys.path:
    sys.path.insert(0, path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'digital_notes.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
