from django.urls import path
from .views import product, main, orders, categories, contact, order_lookup

app_name = 'frontend'

urlpatterns = [
    path('', main.index, name='index'),
    path('products/', product.product_list, name='product_list'),
    path('products/<int:product_pk>/', product.product_detail, name='product_detail'),
    path('get-communes/<str:wilaya_code>/', product.get_coummunes, name='get_communes'),
    path('product/<int:product_pk>/order/', orders.create_order, name='create_order'),
    path('categories/', categories.category_list, name='category_list'),
    path('categories/<slug:category_slug>/', categories.category_details, name='category_details'),
    path('contact/', contact.contact_view, name='contact'),

    path('order/<str:ref_code>/confirmation/', order_lookup.order_confirmation, name='order_confirmation'),
    path('order/lookup/', order_lookup.order_lookup, name='order_lookup'),

]
