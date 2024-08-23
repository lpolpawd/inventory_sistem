from django.db import models
import json
from datetime import datetime

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('ADD', 'Add'),
        ('REMOVE', 'Remove'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.transaction_type} - {self.quantity}"
    
class Report(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()  # Store the report as text or JSON

    def __str__(self):
        return f"Report generated on {self.created_at}"
    
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)