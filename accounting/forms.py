from django.forms import ModelForm, SelectDateWidget
from .models import Customer, BankAccount, Contract, ContractSale
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
        # start_field = forms.DateField(widget=DatePickerInput)
        # end_field = forms.DateField(widget=DatePickerInput)
        # is_active = forms.BooleanField(widget=forms.CheckboxInput)

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
    rate_amount = forms.DecimalField(disabled=True, required=False)

    class Meta:
        model = ContractSale

        # contract = models.ForeignKey("accounting.Contract", on_delete=models.SET_DEFAULT, default=None, null=True)
        # date = models.DateField(help_text='date')
        # worked_hours = models.FloatField()
        # amount = models.FloatField()
        # note = models.TextField(blank=True)

        fields = ['contract', 'date', 'worked_hours', 'rate_amount', 'total_amount', 'note']

        widgets = {
            'date': DatePickerInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # print(self.instance)
    #     if self.instance.contract:
    #         self.fields['total_amount'].initial = self.instance.contract.rate_amount

