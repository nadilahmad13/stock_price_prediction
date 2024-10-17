from django.urls import path
from .controllers.stock_data import StockDataController
from .controllers.backtesting import BacktestingController

urlpatterns = [
    path('stocks/', StockDataController.as_view(), name='stocks'),
    path('backtest/', BacktestingController.as_view(), name='backtest')
]
