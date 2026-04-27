from django.shortcuts import redirect
from django.urls import reverse

class PasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        allowed_urls = [
            reverse('users:password_change'),
            reverse('users:logout'),
        ]

        if getattr(request.user, 'needs_password_change', False):
            if request.path not in allowed_urls and not request.path.startswith('/static/'):
                return redirect('users:password_change')

        return self.get_response(request)