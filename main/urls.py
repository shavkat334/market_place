from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/', views.update_cart_item, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
]