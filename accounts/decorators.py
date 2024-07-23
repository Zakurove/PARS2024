from functools import wraps
from django.http import HttpResponseRedirect

def user_has_role(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or (not request.user.is_staff and not request.user.is_admin and not request.user.is_superuser):
            return HttpResponseRedirect('/login/')  # Redirect to login if user is not authenticated or does not have the required roles
        return view_func(request, *args, **kwargs)
    return _wrapped_view