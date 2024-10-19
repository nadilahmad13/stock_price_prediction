from django.urls import path
from .controllers.StockDataController import StockDataController
from .controllers.BackTestingController import BackTestingController
from .controllers.PredictionController import StockPricePredictionView
from .controllers.BackTestingReportController import BackTestingReportView

urlpatterns = [
    path('stocks/', StockDataController.as_view(), name='stocks'),
    path('backtest/', BackTestingController.as_view(), name='backtest'),
    path('predict/', StockPricePredictionView.as_view(), name='predict'),
    path('report/backtest/', BackTestingReportView.as_view(), name='backtest-report')
]
