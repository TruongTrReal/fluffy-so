"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# myapp/urls.py
from django.urls import path
from myapp.views import StockAPI, add_or_modify_stock, delete_stock, get_all_stocks, get_account_summary_api, add_or_modify_summary_api

urlpatterns = [
    path('stockapi/', StockAPI.as_view(), name='stockAPI'),
    path('stock/', add_or_modify_stock, name='add_or_modify_stock'),
    path('stock/<str:account_number>/<int:account_type>/<str:symbol>/', delete_stock, name='delete_stock'),
    path('stocks/<str:account_number>/<int:account_type>', get_all_stocks, name='get_all_stocks'),
    path('account-summary/<str:account_number>/<int:account_type>/', get_account_summary_api, name='get_account_summary_api'),
    path('add-or-modify-summary/', add_or_modify_summary_api, name='add_or_modify_summary_api'),

]


