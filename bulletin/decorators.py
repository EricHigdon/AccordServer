import logging
import base64
from functools import wraps
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden

def http_basic_auth(func):
    """
    Use as a decorator for views that need to perform HTTP basic
    authorization.
    """
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            try:
                authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
                if authmeth.lower() == 'basic':
                    auth = str(base64.b64decode(auth.strip()))
                    username, password = auth.split(':', 1)
                    user = authenticate(username=username, password=password)
                    if user:
                        login(request, user)
            except ValueError:
                # Bad HTTP_AUTHORIZATION header
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return _decorator