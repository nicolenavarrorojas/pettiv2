from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse

def check_administrator(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_administrator:
            return HttpResponseRedirect(reverse('index'))
        return view_func(request, *args, **kwargs)
    return wrapper
