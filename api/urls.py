from django.urls import path
from .controllers.StockDataController import StockDataController
from .controllers.BackTestingController import BacktestingController
from .controllers.PredictionController import StockPricePredictionView

urlpatterns = [
    path('stocks/', StockDataController.as_view(), name='stocks'),
    path('backtest/', BacktestingController.as_view(), name='backtest'),
    path('predict/', StockPricePredictionView.as_view(), name='predict')
]
