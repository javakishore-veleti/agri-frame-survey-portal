# apps/django-identity-access/entitlements/middleware.py

from .models_base import set_current_user


class CurrentUserMiddleware:
    """
    Stores request.user in thread-local storage for audited models to consume.
    Add AFTER AuthenticationMiddleware in settings.MIDDLEWARE.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_user(getattr(request, "user", None))
        try:
            return self.get_response(request)
        finally:
            set_current_user(None)
