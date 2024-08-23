from django import forms
from .models import Item, Transaction

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'stock']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['item', 'quantity', 'transaction_type']
