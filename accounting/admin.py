from django.contrib import admin
from .models import Customer, BankAccount, Contract, ContractSale


@admin.register(Customer)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ["company", "address", "web", "email", "responsible", "created_date"]
    list_display_links = ["company", "created_date"]
    search_fields = ["company"]
    list_filter = ["created_date"]

    class Meta:
        model = Customer


@admin.register(BankAccount)
class BankAccountsAdmin(admin.ModelAdmin):
    list_display = ["bank", "account_alias", "account_type", "account_no", "sort_code", "account_owner",
                    "currency", "note"]

    list_display_links = ["bank", "account_alias"]
    search_fields = ["bank"]
    list_filter = ["bank"]

    class Meta:
        model = BankAccount


@admin.register(Contract)
class ContractsAdmin(admin.ModelAdmin):
    list_display = ["contract_alias", "customer_id", "start_date", "end_date", "rate_type",
                    "rate_amount", "currency", "billing_period", "is_active", "description"]
    list_display_links = ["contract_alias", "customer_id"]
    search_fields = ["contract_alias"]
    list_filter = ["contract_alias"]

    class Meta:
        model = Contract
