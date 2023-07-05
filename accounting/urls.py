from django.contrib import admin
from django.urls import path
from . import views

app_name = "accounting"

urlpatterns = [
    path('customers', views.customers, name='customers'),
    path('addcustomer', views.add_customer, name='addcustomer'),
    path('customer/<int:id>', views.customer_detail, name='customer_detail'),
    path('update_customer/<int:id>', views.update_customer, name='update_customer'),
    path('delete_customer/<int:id>', views.delete_customer, name='delete_customer')
]
