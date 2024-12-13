"""
WSGI config for store project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import threading
import run_tasks

from django.core.wsgi import get_wsgi_application

def start_scheduler():
    run_tasks.run_scheduler()
    
threading.Thread(target=start_scheduler).start()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

application = get_wsgi_application()
