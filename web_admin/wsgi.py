#coding:utf-8
"""
WSGI config for web_admin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_admin.settings")

#解决布署时找不到应用的问题，路径根据情况填写
sys.path.append('/opt/web_admin')

application = get_wsgi_application()
print sys.path

