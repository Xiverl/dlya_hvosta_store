from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from store.models import Order


User = get_user_model()


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class InfoUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'number_phone',
            'city',
            'street',
            'building',
            'entrance',
            'location',
        )


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ('user', 'status', 'is_published')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )


class CartAddProductForm(forms.Form):
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
