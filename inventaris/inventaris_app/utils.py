# utils.py

from .models import Item, Transaction, models
from django.db.models import Sum
from datetime import datetime, timedelta

def get_inventory_summary():
    # Current Stock Levels
    items = Item.objects.all()

    # Low Stock Items
    low_stock_threshold = 10  # Define your threshold
    low_stock_items = items.filter(stock__lt=low_stock_threshold)

    # Stock Trends
    transactions = Transaction.objects.all()
    stock_trends = (
        transactions
        .values('item__name')
        .annotate(total_added=Sum('quantity', filter=models.Q(transaction_type='ADD')),
                  total_removed=Sum('quantity', filter=models.Q(transaction_type='REMOVE')))
    )

    # Get the most recent transaction date
    if transactions.exists():
        most_recent_transaction = transactions.latest('date')
        most_recent_transaction_date = most_recent_transaction.date.isoformat()
    else:
        most_recent_transaction_date = None

    # Predict Future Stock Needs using a simple moving average for the last 30 days
    prediction_days = 30  # Predicting needs for the next 30 days
    today = datetime.now().date()
    predicted_needs = {}

    for item in items:
        past_transactions = transactions.filter(item=item, date__gte=today - timedelta(days=30))
        total_removed = past_transactions.filter(transaction_type='REMOVE').aggregate(total=Sum('quantity'))['total'] or 0
        average_daily_usage = total_removed / 30 if total_removed > 0 else 0
        predicted_need = average_daily_usage * prediction_days
        predicted_needs[item.name] = predicted_need

    return {
        'date': most_recent_transaction_date,
        'current_stock': {item.name: item.stock for item in items},
        'low_stock_items': {item.name: item.stock for item in low_stock_items},
        'stock_trends': [
            {
                'item': trend['item__name'],
                'total_added': trend['total_added'] or 0,
                'total_removed': trend['total_removed'] or 0,
                'net_stock': (trend['total_added'] or 0) - (trend['total_removed'] or 0),
            }
            for trend in stock_trends
        ],
        'predicted_needs': predicted_needs,
    }
