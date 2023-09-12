from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from store.models import Product, Order
from store.forms import OrderForm


class ProfileLoginView(LoginView):
    def get_success_url(self):
        url = reverse(
            'store:profile',
            args=(self.request.user.get_username(),)
        )
        return url


def info_profile(request, name):
    templates = 'store/profile.html'
    return render(request, templates)


def product_list(request):
    template_name = 'store/store_pages.html'
    products = Product.objects.filter(is_published=True)
    context = {
        'products': products,
    }
    return render(request, template_name, context)


def product_detail(request, pk):
    template_name = 'store/detail.html'
    form = OrderForm
    product = get_object_or_404(Product, id=pk)
    context = {
        'product': product,
        'form': form
    }
    return render(request, template_name, context)


def order_list(request):
    template_name = 'store/admin_pages.html'
    orders = Order.objects.filter(is_published=True)
    context = {
        'orders': orders
    }
    return render(request, template_name, context)


def order_add(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = OrderForm(request.POST)
    if form.is_valid():
        order = form.save(commit=False)
        order.product = product
        order.save()
    return redirect('pages:index')
