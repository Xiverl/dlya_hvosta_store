from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from store.models import Product, Order, OrderItem, Location
from store.forms import (
    OrderForm,
    CartAddProductForm,
    InfoUserForm,
    UserRegistrationForm
)
from store.cart import Cart
from store.utils import get_info_order
from feedStore.settings import PAGINATE_STEP


User = get_user_model()


class ProfileLoginView(LoginView):
    def get_success_url(self):
        url = reverse(
            'store:profile',
            args=(self.request.user.get_username(),)
        )
        return url


class CreateUserView(CreateView):
    form_class = UserRegistrationForm

    class Meta:
        model = User
        fields = ('username', 'password')


@login_required
def info_profile(request, name):
    template_name = 'store/profile.html'
    user = get_object_or_404(
        User,
        username=name,
    )
    orders = user.order.all().order_by('-created_at')
    order_items = OrderItem.objects.all()
    context = {
        'orders': orders,
        'order_items': order_items
    }
    return render(request, template_name, context)


@login_required
def info_user_edit(request, name):
    template_name = 'store/info-user.html'
    instance = request.user
    form = InfoUserForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            info = form.save(commit=False)
            info.save()
            return redirect('store:profile', name)
    context = {
        'form': form,
        'info': instance,
    }
    return render(request, template_name, context)


def product_list(request):
    template_name = 'store/store_pages.html'
    products_list = Product.objects.filter(is_published=True)
    paginator = Paginator(products_list, PAGINATE_STEP)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
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
    return redirect('store:product-list')


@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('store:cart_detail')


@login_required(login_url='login')
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})


@login_required(login_url='login')
def order_list(request):
    template_name = 'store/admin_pages.html'
    orders = Order.objects.filter(is_published=True)
    context = {
        'orders': orders
    }
    return render(request, template_name, context)


@login_required(login_url='login')
def order_add(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = OrderForm(request.POST or None)
    if request.user.is_info:
        order = get_info_order(request.user)
        form = OrderForm(request.POST or None, instance=order)
        order.delete()
    if request.method == 'POST':
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.user = request.user
            order.save()
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=product.price
            )
            product.value = product.value - 1
            product.save()
            return redirect('store:profile', request.user.username)
    template_name = 'store/single_order_create.html'
    context = {
        'form': form,
        'product': product
    }
    return render(request, template_name, context)


@login_required(login_url='login')
def order_create(request):
    template_name = 'store/order_create.html'
    cart = Cart(request)
    form = OrderForm(request.POST or None)
    if request.user.is_info:
        order = get_info_order(request.user)
        form = OrderForm(request.POST or None, instance=order)
        order.delete()
    if request.method == 'POST':
        if len(cart) == 0:
            form.add_error(
                error='Добавте товар(ы) в корзину.',
                field='__all__'
            )
            return render(
                request,
                template_name,
                {
                    'cart': cart,
                    'form': form,
                }
            )
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                item['product'].value = item['product'].value - item['quantity']
                item['product'].save()
            cart.clear()
            return redirect('store:profile', request.user.username)
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, template_name, context)


def order_ready(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.status = 'Доставлен'
    order.save()
    return redirect('store:profile', request.user.username)


def order_confirmed(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.status = 'Подтвержден'
    order.save()
    return redirect('store:profile', request.user.username)


def order_cancelled(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.status = 'Отменен'
    order.save()
    return redirect('store:profile', request.user.username)


@login_required(login_url='login')
def delivery_page(request):
    order_items = OrderItem.objects.all()
    template_name = 'store/delivery_page.html'
    if not request.user.is_superuser:
        return render(request, 'error/403.html')
    menu_dict = list()
    for location in Location.objects.all():
        menu_dict.append(
            {
                f'{location.name}': location.order.all()
            }
        )
    context = {
        'menu_dict': menu_dict,
        'order_items': order_items
    }
    return render(request, template_name, context)
