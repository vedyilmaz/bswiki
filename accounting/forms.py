from django.forms import ModelForm
from .models import Customers

# Create the form class.


class CustomerForm(ModelForm):
    class Meta:
        model = Customers
        fields = ['company', 'address', 'web', 'email', 'responsible', 'company_logo', 'note']
