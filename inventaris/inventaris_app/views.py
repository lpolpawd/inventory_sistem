from django.shortcuts import render, redirect
from .models import Item, Transaction, Report, models
from .forms import ItemForm, TransactionForm
from django.db.models import Sum
import json
from datetime import datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from .utils import get_inventory_summary

#start of inventaris logic
@permission_required('inventaris_app.add_item', raise_exception=True)
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_inventory')
    else:
        form = ItemForm()
    return render(request, 'inventaris_app/add_item.html', {'form': form})

def update_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('view_inventory')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventaris_app/update_item.html', {'form': form})

@permission_required('inventaris_app.delete_item', raise_exception=True)
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('view_inventory')
    return render(request, 'inventaris_app/delete_item.html', {'item': item})

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            item = transaction.item
            if transaction.transaction_type == 'ADD':
                item.stock += transaction.quantity
            else:
                item.stock -= transaction.quantity
            item.save()
            return redirect('view_inventory')
    else:
        form = TransactionForm()
    return render(request, 'inventaris_app/add_transaction.html', {'form': form})

@login_required
def view_inventory(request):
    items = Item.objects.all()
    return render(request, 'inventaris_app/view_inventory.html', {'items': items})

class DateTimeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def generate_report(request):
    # Get the inventory summary using the helper function
    report_content = get_inventory_summary()

    # Store the report (if needed)
    report = Report.objects.create(content=json.dumps(report_content, cls=DjangoJSONEncoder))

    return render(request, 'inventaris_app/report.html', {'report': report_content})
#End of inventaris logic

#start of user autentikasi
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'inventaris_app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('view_inventory')  # Redirect to a protected view after login
    else:
        form = AuthenticationForm()
    return render(request, 'inventaris_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def assign_user_to_group(user_id, group_name):
    user = User.objects.get(id=user_id)
    group = Group.objects.get(name=group_name)
    user.groups.add(group)

def base(request):
    return render(request, 'inventaris_app/base.html')

def dashboard(request):
    # Get the inventory summary using the helper function
    summary_data = get_inventory_summary()

    return render(request, 'inventaris_app/dashboard.html', summary_data)
