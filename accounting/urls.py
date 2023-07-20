from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('set_sales_data', views.set_sales_data, name='ajax_set_sales_data'),
    path('update_contract/<int:id>', views.update_contract, name='update_contract'),
    path('delete_contract/<int:contract_id>', views.delete_contract, name='delete_contract'),

    # contract sales
    path('contract_sales', views.contract_sales, name='contract_sales'),
    path('add_contract_sale', views.add_contract_sale, name='add_contract_sale'),
    path('contract_sale_detail/<int:id>', views.contract_sale_detail, name='contract_sale_detail'),
    path('load_contract', views.load_contract, name='ajax_load_contract'),
    path('update_contract_sale/<int:id>', views.update_contract_sale, name='update_contract_sale'),
    path('delete_contract_sale/<int:id>', views.delete_contract_sale, name='delete_contract_sale'),

    # contract sales invoice
    path('cont_sale_invoices', views.contract_sale_invoices, name='cont_sale_invoices'),
    path('add_cont_sale_invoice', views.add_contract_sale_invoice, name='add_cont_sale_invoice'),
    path('set_invoice_data', views.set_invoice_data, name='ajax_set_invoice_data'),
    path('cont_sale_invoice_detail/<int:id>', views.cont_sale_invoice_detail, name='cont_sale_invoice_detail'),
    path('update_cont_sale_invoice/<int:id>', views.update_cont_sale_invoice, name='update_cont_sale_invoice'),
    path('delete_cont_sale_invoice/<int:id>', views.delete_cont_sale_invoice, name='delete_cont_sale_invoice'),

    # contract sales transactions
    path('cont_sales_transactions', views.contract_sales_transactions, name='cont_sales_transactions'),
    path('add_cont_sales_transaction', views.add_contract_sales_transaction, name='add_cont_sales_transaction'),
    path('set_transaction_data', views.set_transaction_data, name='ajax_set_transaction_data'),
    path('cont_sales_transaction_detail/<int:id>', views.cont_sales_transaction_detail, name='cont_sales_transaction_detail'),
    path('update_cont_sales_transaction/<int:id>', views.update_cont_sales_transaction, name='update_cont_sales_transaction'),
    path('delete_cont_sales_transaction/<int:id>', views.delete_cont_sales_transaction, name='delete_cont_sales_transaction'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
