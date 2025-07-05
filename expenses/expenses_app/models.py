from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# Create your models here.

class ExpenseIncome(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    TAX_TYPE_CHOICES = [
        ('flat', 'Flat'),
        ('percentage', 'Percentage'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_type = models.CharField(max_length=10, choices=TAX_TYPE_CHOICES, default='flat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        # Handle None values for both amount and tax
        amount_value = self.amount or 0
        tax_value = self.tax or 0
        
        if self.tax_type == 'flat':
            return amount_value + tax_value
        elif self.tax_type == 'percentage':
            return amount_value + (amount_value * tax_value / 100)
        return amount_value

    def __str__(self):
        return f"{self.title} ({self.transaction_type}) - {self.amount}"