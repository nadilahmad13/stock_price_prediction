from django.urls import path
from .controllers.StockDataController import StockDataController
from .controllers.BackTestingController import BacktestingController
from .controllers.PredictionController import StockPricePredictionView
from .controllers.ReportController import BacktestReportView

urlpatterns = [
    path('stocks/', StockDataController.as_view(), name='stocks'),
    path('backtest/', BacktestingController.as_view(), name='backtest'),
    path('predict/', StockPricePredictionView.as_view(), name='predict'),
    path('report/backtest/', BacktestReportView.as_view(), name='backtest-report')
]
