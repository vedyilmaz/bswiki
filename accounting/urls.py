from django.contrib import admin
from django.urls import path
from . import views

app_name = "accounting"

urlpatterns = [
    # customers
    path('customers', views.customers, name='customers'),
    path('addcustomer', views.add_customer, name='addcustomer'),
    path('customer/<int:id>', views.customer_detail, name='customer_detail'),
    path('update_customer/<int:id>', views.update_customer, name='update_customer'),
    path('delete_customer/<int:id>', views.delete_customer, name='delete_customer'),

    # bank accounts
    path('bank_accounts', views.bank_accounts, name='bank_accounts'),
    path('bank_account/<int:id>', views.bank_account_detail, name='bank_account_detail'),
    path('add_bank_account', views.add_bank_account, name='add_bank_account'),
    path('update_bank_account/<int:id>', views.update_bank_account, name='update_bank_account'),
    path('delete_bank_account/<int:id>', views.delete_bank_account, name='delete_bank_account'),

    # contracts
    path('contracts', views.contracts, name='contracts'),
    path('contract/<int:id>', views.contract_detail, name='contract_detail'),
    path('add_contract', views.add_contract, name='add_contract'),
    path('update_contract/<int:id>', views.update_contract, name='update_contract'),
    path('delete_contract/<int:contract_id>', views.delete_contract, name='delete_contract'),

    # contract sales
    path('contract_sales', views.contract_sales, name='contract_sales'),
    path('add_contract_sale', views.add_contract_sale, name='add_contract_sale'),
    path('contract_sale_detail/<int:id>', views.contract_sale_detail, name='contract_sale_detail'),
    path('update_contract_sale/<int:id>', views.update_contract_sale, name='update_contract_sale'),
    path('delete_contract_sale/<int:id>', views.delete_contract_sale, name='delete_contract_sale'),
    path('selected_contract_id/', views.selected_contract_id, name='selected_contract_id')
]
