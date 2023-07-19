from django.forms import ModelForm, SelectDateWidget, ClearableFileInput
from .models import Customer, BankAccount, Contract, ContractSale, ContractSalesInvoice, ContractSalesTransaction
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django import forms
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, CheckBoxInput, RadioSelectInput

# Create the form class.


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['company', 'address', 'web', 'email', 'responsible', 'company_logo', 'note']


class BankAccountForm(ModelForm):

    class Meta:

        ACCOUNT_TYPES = [('business', 'Business'), ('personal', 'Personal')]
        model = BankAccount
        fields = ['bank', 'account_alias', 'account_type', 'account_no', 'sort_code', 'account_owner', 'currency',
                  'note']

        widgets = {
            "account_type": RadioSelectInput(choices=ACCOUNT_TYPES)
        }


class ContractForm(ModelForm):

    class Meta:
        model = Contract
        RATE_TYPES = [("hourly", "Hourly"), ("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly"),
                      ("project_based", "Project Based")]

        BILLING_PERIODS = [("weekly", "Weekly"), ("monthly", "Monthly"), ("milestone", "Milestone")]

        fields = ['customer', 'contract_alias', 'start_date', 'end_date', 'rate_type', 'rate_amount', 'currency',
                  'billing_period', 'is_active', 'description']

        widgets = {
            'start_date': DatePickerInput(),
            'end_date': DatePickerInput(),
            'is_active': CheckBoxInput(),
            'rate_type': RadioSelectInput(choices=RATE_TYPES),
            'billing_period': RadioSelectInput(choices=BILLING_PERIODS)
        }


class ContractSaleForm(ModelForm):
    rate_amount = forms.DecimalField(disabled=False, required=False)

    class Meta:
        model = ContractSale

        fields = ['contract', 'date', 'worked_hours', 'rate_amount', 'total_amount', 'is_invoiced', 'note']

        widgets = {
            'date': DatePickerInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # print(self.instance)
    #     if self.instance.contract:
    #         self.fields['total_amount'].initial = self.instance.contract.rate_amount

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['rate_amount'].queryset = Contract.objects.none()
    #
    #     if 'contract' in self.data:
    #         try:
    #             contract_id = int(self.data.get('contract__id'))
    #             self.fields['rate_amount'].queryset = Contract.objects.filter(id=contract_id)
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #
    #     elif self.instance.pk:
    #         self.fields['rate_amount'].queryset = self.instance.contract.contract_set
    #
    #     else:
    #         print("empty data!")


class ContractSaleInvoiceForm(ModelForm):

    class Meta:
        model = ContractSalesInvoice

        fields = ['sales', 'invoice_number', 'date', 'due_date', 'is_paid_off', 'invoice_file', 'note']

        widgets = {
            'date': DatePickerInput(),
            'due_date': DatePickerInput(),
            'is_paid_off': CheckBoxInput(),
        }


class ContractSaleTransactForm(ModelForm):

    class Meta:
        model = ContractSalesTransaction

        fields = ['invoice', 'date', 'amount', 'bank_account', 'note']

        widgets = {
            'date': DatePickerInput(),
        }
