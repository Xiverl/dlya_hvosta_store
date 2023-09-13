from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from store.models import Product, Order
from store.forms import OrderForm, CartAddProductForm
from store.cart import Cart


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
    form = CartAddProductForm
    context = {
        'products': products,
        'form': form,
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


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=1,
                 update_quantity=cd['update'])
    return redirect('store:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('store:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})


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
    return redirect('pages:about')
