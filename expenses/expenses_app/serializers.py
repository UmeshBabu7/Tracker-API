from rest_framework import serializers
from .models import ExpenseIncome


class ExpenseIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseIncome
        fields = [
            'id', 'title', 'description', 'amount', 'transaction_type', 'tax', 'tax_type',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

   