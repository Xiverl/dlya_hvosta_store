from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from store import views


app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('<int:pk>/', views.product_detail, name='product-detail'),
    path('order/', views.order_list, name='order-list'),
    path('<int:pk>/add_order/', views.order_add, name='order-add'),
    path('profile/<name>/', views.info_profile, name='profile'),
]
