import datetime

import django
from django.db import models
from django.db.models import Q
from django_cleanup import cleanup
from ckeditor.fields import RichTextField
import django.db.models.options as options
from datetime import date
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)

fs_invoice = FileSystemStorage(location="/invoices")

# Create your models here.


@cleanup.ignore
class Customer(models.Model):
    company = models.CharField(max_length=150, unique=True)
    address = models.CharField(max_length=150)
    web = models.URLField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    responsible = models.CharField(max_length=150, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    company_logo = models.FileField(upload_to='logos/', blank=True, null=True, verbose_name="Add the company logo")
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company

    class Meta:
        ordering = ['-created_date']
        es_index_name = 'django'
        es_type_name = 'customer'
        es_mapping = {
            'properties': {
                'company': {'type': 'string', 'index': 'not_analyzed'},
                'address': {'type': 'string', 'index': 'not_analyzed'},
                'web': {'type': 'string', 'index': 'not_analyzed'},
                'responsible': {'type': 'string', 'index': 'not_analyzed'},
                'note': {'type': 'string', 'index': 'not_analyzed'}
            }
        }


@cleanup.ignore
class BankAccount(models.Model):
    bank = models.CharField(max_length=150)
    account_alias = models.CharField(max_length=150, unique=True)
    account_type = models.CharField(max_length=50)  # 1: business, 2: personal
    account_no = models.CharField(max_length=150)
    sort_code = models.CharField(max_length=150)
    account_owner = models.CharField(max_length=150)
    currency = models.CharField(verbose_name="currency",  max_length=15)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.account_alias

    class Meta:
        ordering = ['-bank']
        es_index_name = 'django'
        es_type_name = 'bank_account'
        es_mapping = {
            'properties': {
                'bank': {'type': 'string', 'index': 'not_analyzed'},
                'account_alias': {'type': 'string', 'index': 'not_analyzed'},
                'account_type': {'type': 'string', 'index': 'not_analyzed'},
                'account_no': {'type': 'string', 'index': 'not_analyzed'},
                'sort_code': {'type': 'string', 'index': 'not_analyzed'},
                'account_owner': {'type': 'string', 'index': 'not_analyzed'},
                'currency': {'type': 'string', 'index': 'not_analyzed'},
                'note': {'type': 'string', 'index': 'not_analyzed'}
            }
        }


@cleanup.ignore
class Contract(models.Model):
    contract_alias = models.CharField(max_length=150, unique=True)
    customer = models.ForeignKey("accounting.Customer", on_delete=models.CASCADE)
    start_date = models.DateField(help_text='contract start date')
    end_date = models.DateField(help_text='contract end date', blank=True, null=True)
    rate_type = models.CharField(max_length=150)        # hourly, daily, weekly, monthly
    rate_amount = models.FloatField()
    currency = models.CharField(max_length=150)         # USD, GBP, etc
    billing_period = models.CharField(max_length=15)    # weekly, monthly
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.contract_alias

    class Meta:
        ordering = ['-start_date']
        es_index_name = 'django'
        es_type_name = 'contract'
        es_mapping = {
            'properties': {
                'contract_alias': {'type': 'string', 'index': 'not_analyzed'},
                'start_date': {'type': 'date', 'index': 'not_analyzed'},
                'due_date': {'type': 'date', 'index': 'not_analyzed'},
                'rate_type': {'type': 'string', 'index': 'not_analyzed'},
                'rate_amount': {'type': 'float', 'index': 'not_analyzed'},
                'currency': {'type': 'string', 'index': 'not_analyzed'},
                'billing_period': {'type': 'string', 'index': 'not_analyzed'},
                'is_active': {'type': 'boolean', 'index': 'not_analyzed'},
                'description': {'type': 'string', 'index': 'not_analyzed'}
            }
        }


@cleanup.ignore
class ContractSale(models.Model):
    contract = models.ForeignKey("accounting.Contract", on_delete=models.CASCADE)
    date = models.DateField(help_text='date', default=django.utils.timezone.now)
    worked_hours = models.FloatField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    is_invoiced = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    # implement calculated field
    # https://stackoverflow.com/questions/44805303/django-model-method-or-calculation-as-field-in-database

    # def total_amount(self):
    #     #  need to dynamically fetched the rate amount on selection change
    #     # in the template form
    #     return self.contract.rate_amount * self.worked_hours
    #
    # def save(self, *args, **kwargs):
    #     self.amount = self.calculate_amount
    #     # self.age = self.get_age
    #     super(ContractSale, self).save(*args, **kwargs)

    def __str__(self):
        return self.contract.contract_alias



    class Meta:
        ordering = ['-date']
        # es_index_name = 'django'
        # es_type_name = 'contract'
        # es_mapping = {
        #     'properties': {
        #         'date': {'type': 'date', 'index': 'not_analyzed'},
        #         'worked_hours': {'type': 'float', 'index': 'not_analyzed'},
        #         'amount': {'type': 'float', 'index': 'not_analyzed'},
        #         'note': {'type': 'string', 'index': 'not_analyzed'}
        #     }
        # }


@cleanup.ignore
class MileStone(models.Model):
    contract = models.ForeignKey("accounting.Contract", on_delete=models.SET_DEFAULT, default=None)
    due_date = models.DateField(help_text='milestone due date')
    delivery_date = models.DateField(help_text='date of delivery')
    milestone_number = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    milestone_amount = models.DecimalField(decimal_places=2, max_digits=6)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.contract.contract_alias

    class Meta:
        ordering = ['-due_date']
        # es_index_name = 'django'
        # es_type_name = 'contract'
        # es_mapping = {
        #     'properties': {
        #         'contract_alias': {'type': 'string', 'index': 'not_analyzed'},
        #         'start_date': {'type': 'date', 'index': 'not_analyzed'},
        #         'total_amount': {'type': 'float', 'index': 'not_analyzed'},
        #         'milestone_count': {'type': 'integer', 'index': 'not_analyzed'},
        #         'currency': {'type': 'string', 'index': 'not_analyzed'},
        #         'is_active': {'type': 'boolean', 'index': 'not_analyzed'},
        #         'description': {'type': 'string', 'index': 'not_analyzed'}
        #     }
        # }


@cleanup.ignore
class ContractSalesInvoice(models.Model):
    # sales = models.ForeignKey("accounting.ContractSale", on_delete=models.CASCADE, unique=True)
    contract = models.ForeignKey("Contract", on_delete=models.CASCADE, default=1)
    sales_ids = models.CharField(max_length=100, verbose_name="sales_ids")
    invoice_number = models.CharField(max_length=100)
    date = models.DateField(help_text='invoice date', default= django.utils.timezone.now)
    due_date = models.DateField(help_text='invoice due date', default=now() + datetime.timedelta(days=7))
    total_amount = models.DecimalField(verbose_name="total_amount", decimal_places=2, max_digits=12, default=0)
    is_paid_off = models.BooleanField(default=False)
    invoice_file = models.FileField(upload_to='invoices/%Y-%b', blank=True, null=True, verbose_name="Add an invoice file")
    note = models.TextField(blank=True)

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = ['-due_date']


@cleanup.ignore
class ContractSalesTransaction(models.Model):
    invoice = models.ForeignKey("accounting.ContractSalesInvoice", on_delete=models.CASCADE, unique=True)
    date = models.DateField(help_text='invoice date', default=django.utils.timezone.now)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    bank_account = models.ForeignKey("accounting.BankAccount", on_delete=models.CASCADE)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.invoice.invoice_number

    class Meta:
        ordering = ['-date']
