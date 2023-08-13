# myapp/permissions.py

from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

class IsAdminOrReadOnly:
    def __init__(self, view_func):
        self.view_func = view_func

    def __call__(self, request, *args, **kwargs):
        if request.method == 'GET' or request.user.is_staff:
            return self.view_func(request, *args, **kwargs)
        if request.user.is_authenticated == False:
            return login_required(self.view_func, login_url='login')(request, *args, **kwargs) 
        elif request.method == 'POST':
            if request.user.is_authenticated and request.user.is_staff:
                return self.view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to perform this action.")


def is_admin(user):
    return user.is_authenticated and user.is_staff
