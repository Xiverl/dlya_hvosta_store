from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.views import LoginView


class ProfileLoginView(LoginView):
    def get_success_url(self):
        url = reverse(
            'users:profile',
            args=(self.request.user.get_username(),)
        )
        return url


def info_profile(request, name):
    templates = 'users/profile.html'
    return render(request, templates)
