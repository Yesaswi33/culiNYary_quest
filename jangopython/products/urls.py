# products/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart'),
    path('add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('add-custom/<int:dish_id>/', views.add_custom_dish_to_cart, name='add_custom_dish_to_cart'),
]
