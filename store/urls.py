from django.urls import path

from store import views


app_name = 'store'

urlpatterns = [
    # url связанные с продукцией
    path('', views.product_list, name='product-list'),
    path('<int:pk>/', views.product_detail, name='product-detail'),

    # url связанные с заказами корзины
    path('order/', views.order_list, name='order-list'),
    path('add_order/', views.order_create, name='order-add'),

    # url связанные с одиночными заказами
    path(
        '<int:pk>/single_add_order/',
        views.order_add,
        name='single-order-create'
    ),

    # url связанные с корзиной
    path('<int:product_id>/cart_add/', views.cart_add, name='cart_add'),
    path(
        '<int:product_id>/cart_revove/',
        views.cart_remove,
        name='cart_remove'
    ),
    path('cart/', views.cart_detail, name='cart_detail'),

    # url связанные с пользователями
    path('profile/<name>/', views.info_profile, name='profile'),
]
