from django.contrib import admin
from .models import Customers
# Register your models here.

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ["company", "address", "web", "email", "responsible", "created_date"]
    list_display_links = ["company", "created_date"]
    search_fields = ["company"]
    list_filter = ["created_date"]

    class Meta():
        model = Customers