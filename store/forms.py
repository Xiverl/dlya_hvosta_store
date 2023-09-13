from django import forms
from django.contrib.auth import get_user_model

from store.models import Order


User = get_user_model()


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ('is_published', 'product', )
        # fields = '__all__'


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
