from django.urls import path
from .controllers.stock_data import StockDataController
from .controllers.backtesting import BacktestingController
from .controllers.prediction import StockPricePredictionView

urlpatterns = [
    path('stocks/', StockDataController.as_view(), name='stocks'),
    path('backtest/', BacktestingController.as_view(), name='backtest'),
    path('predict/', StockPricePredictionView.as_view(), name='predict')
]
