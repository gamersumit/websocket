"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import *
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Combine the HTTP and WebSocket applications
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        chat.routing.websocket_urlpatterns,
    ),
})



