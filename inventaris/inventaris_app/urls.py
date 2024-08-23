from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('add_item/', views.add_item, name='add_item'),
    path('update_item/<int:item_id>/', views.update_item, name='update_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('view_inventory/', views.view_inventory, name='view_inventory'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('base/', views.base, name='base'),
    path('dashboard/', views.dashboard, name='dashboard')
]