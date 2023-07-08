from django.db import models
from django_cleanup import cleanup
from ckeditor.fields import RichTextField
import django.db.models.options as options


options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)


# Create your models here.

@cleanup.ignore
class Customer(models.Model):
    company = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    web = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    responsible = models.CharField(max_length=150, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    company_logo = models.FileField(blank=True, null=True, verbose_name="Add the company logo")
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
    account_alias = models.CharField(max_length=150)
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
    contract_alias = models.CharField(max_length=150)
    customer_id = models.ForeignKey("accounting.Customer", on_delete=models.SET_DEFAULT, default=None, null=True)
    start_date = models.DateField(help_text='contract start date')
    end_date = models.DateField(help_text='contract end date', blank=True, null=True)
    rate_type = models.CharField(max_length=150)        # hourly, daily, weekly, monthly
    rate_amount = models.FloatField()
    currency = models.CharField(max_length=150)         # USD, GBP, etc
    billing_period = models.CharField(max_length=15)    # weekly, monthly
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description

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
    contract_id = models.ForeignKey("accounting.Contract", on_delete=models.SET_DEFAULT, default=None, null=True)
    date = models.DateField(help_text='date')
    worked_hours = models.FloatField()
    amount = models.FloatField()
    note = models.TextField(blank=True)

    def __str__(self):
        return self.note

    class Meta:
        ordering = ['-date']
        # es_index_name = 'django'
        # es_type_name = 'contract'
        # es_mapping = {
        #     'properties': {
        #         'contract_alias': {'type': 'string', 'index': 'not_analyzed'},
        #         'start_date': {'type': 'date', 'index': 'not_analyzed'},
        #         'due_date': {'type': 'date', 'index': 'not_analyzed'},
        #         'rate_type': {'type': 'string', 'index': 'not_analyzed'},
        #         'rate_amount': {'type': 'float', 'index': 'not_analyzed'},
        #         'currency': {'type': 'string', 'index': 'not_analyzed'},
        #         'billing_period': {'type': 'string', 'index': 'not_analyzed'},
        #         'is_active': {'type': 'boolean', 'index': 'not_analyzed'},
        #         'description': {'type': 'string', 'index': 'not_analyzed'}
        #     }
        # }