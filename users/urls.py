from django.urls import path, include, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from users import views


app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', views.ProfileLoginView.as_view(), name='login'),
    path(
        'registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('users:login'),
        ),
        name='registration',
    ),
    path('profile/<name>/', views.info_profile, name='profile'),
]
