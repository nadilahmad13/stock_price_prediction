from django.urls import path
from .views import update_stock_price, get_stock_price

urlpatterns = [
    path('stocks/update', update_stock_price),
    path('stocks/', get_stock_price),
]
