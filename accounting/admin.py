from django.contrib import admin
from .models import Customer, BankAccount, Contract, ContractSale, ContractSalesInvoice, RateType, BillingPeriod, \
    ContractType


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
    list_display = ["contract_alias", "customer", "contract_type", "start_date", "end_date",
                    "rate_amount", "currency", "is_active", "note"]
    list_display_links = ["contract_alias", "customer"]
    search_fields = ["contract_alias"]
    list_filter = ["contract_alias"]
    list_editable = ["is_active"]
    list_per_page = 25

    class Meta:
        model = Contract


@admin.register(ContractSale)
class ContractSalesAdmin(admin.ModelAdmin):
    list_display = ["contract", "date", "sales_data", "total_amount"]
    list_display_links = ["contract", "date", "sales_data", "total_amount"]
    search_fields = ["contract"]
    list_filter = ["contract"]
    list_per_page = 25

    class Meta:
        model = ContractSale


@admin.register(ContractSalesInvoice)
class ContractSalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ["sales_ids", "invoice_number", "date", "due_date", "is_paid_off", "invoice_file"]
    list_display_links = ["sales_ids", "invoice_number", "date"]
    search_fields = ["invoice_number"]
    list_filter = ["sales_ids"]
    list_per_page = 25

    class Meta:
        model = ContractSalesInvoice


@admin.register(RateType)
class RateTypeAdmin(admin.ModelAdmin):
    list_display = ["rate_type", "billing_period"]
    list_display_links = ["rate_type", "billing_period"]
    search_fields = ["rate_type"]
    list_filter = ["rate_type"]
    list_per_page = 25

    class Meta:
        model = RateType


@admin.register(BillingPeriod)
class BillingPeriodAdmin(admin.ModelAdmin):
    list_display = ["billing_period"]
    list_display_links = ["billing_period"]
    search_fields = ["billing_period"]
    list_filter = ["billing_period"]
    list_per_page = 25

    class Meta:
        model = BillingPeriod


@admin.register(ContractType)
class ContractTypeAdmin(admin.ModelAdmin):
    list_display = ["contract_type", "rate_type"]
    list_display_links = ["contract_type"]
    search_fields = ["contract_type"]
    list_filter = ["contract_type"]
    list_per_page = 25

    class Meta:
        model = BillingPeriod