from rest_framework import serializers
from accounting.models import ContractSale, Contract


# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = 'auth.User'
#         fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'


class ContractSaleSerializer(serializers.ModelSerializer):
    contract = ContractSerializer()
    # user = UserSerializer()

    class Meta:
        model = ContractSale
        fields = ('id', 'contract', 'date', 'sales_data', 'total_amount', 'is_invoiced', 'note')
