from django.urls import path

from store import views


app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('<int:pk>/', views.product_detail, name='product-detail'),
    path('order/', views.order_list, name='order-list'),
    path('<int:pk>/add_order/', views.order_add, name='order-add'),
    path('profile/<name>/', views.info_profile, name='profile'),
    path('<int:product_id>/cart_add/', views.cart_add, name='cart_add'),
    path(
        '<int:product_id>/cart_revove/',
        views.cart_remove,
        name='cart_remove'
    ),
    path('cart/', views.cart_detail, name='cart_detail')
]
