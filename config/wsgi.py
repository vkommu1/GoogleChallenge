"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('GOOGLE_API_KEY', 'AIzaSyBGRo3GCYTXxBRpxoZJU-yDl3477gBMW6g')
os.environ.setdefault('GPT_API_KEY', 'sk-proj-26rSfXU7VkhZZVqtBZkAT3BlbkFJ8ie501PN6kZj4y4mLbWq')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIzaSyBGRo3GCYTXxBRpxoZJU-yDl3477gBMW6g')

application = get_wsgi_application()
