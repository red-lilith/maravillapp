from functools import wraps

from django.conf import settings
from django.contrib import messages

import requests


def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            request.recaptcha_is_valid = True
        return view_func(request, *args, **kwargs)
    return _wrapped_view
