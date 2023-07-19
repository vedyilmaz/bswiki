from django.contrib import admin
from .models import Customer, BankAccount, Contract, ContractSale, ContractSalesInvoice


@admin.register(Customer)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ["company", "address", "web", "email", "responsible", "created_date"]
    list_display_links = ["company", "created_date"]
    search_fields = ["company"]
    list_filter = ["created_date"]
    list_per_page = 25

    class Meta:
        model = Customer


@admin.register(BankAccount)
class BankAccountsAdmin(admin.ModelAdmin):
    list_display = ["bank", "account_alias", "account_type", "account_no", "sort_code", "account_owner",
                    "currency", "note"]

    list_display_links = ["bank", "account_alias"]
    search_fields = ["bank", "account_alias"]
    list_filter = ["bank", "account_type", "currency"]
    list_per_page = 25

    class Meta:
        model = BankAccount


@admin.register(Contract)
class ContractsAdmin(admin.ModelAdmin):
    list_display = ["contract_alias", "customer", "start_date", "end_date", "rate_type",
                    "rate_amount", "currency", "billing_period", "is_active", "description"]
    list_display_links = ["contract_alias", "customer"]
    search_fields = ["contract_alias"]
    list_filter = ["contract_alias"]
    list_editable = ["is_active"]
    list_per_page = 25

    class Meta:
        model = Contract


@admin.register(ContractSale)
class ContractSalesAdmin(admin.ModelAdmin):
    list_display = ["contract", "date", "worked_hours", "total_amount"]
    list_display_links = ["contract", "date", "worked_hours", "total_amount"]
    search_fields = ["contract"]
    list_filter = ["contract"]
    list_per_page = 25

    class Meta:
        model = ContractSale


@admin.register(ContractSalesInvoice)
class ContractSalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ["sales", "invoice_number", "date", "due_date", "is_paid_off", "invoice_file"]
    list_display_links = ["sales", "invoice_number", "date"]
    search_fields = ["invoice_number"]
    list_filter = ["sales"]
    list_per_page = 25

    class Meta:
        model = ContractSalesInvoice