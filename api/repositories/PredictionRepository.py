from ..models import StockPrediction


class StockPredictionRepository:
    @staticmethod
    def save_stock_prediction(symbol, date, predicted_close):
        StockPrediction.objects.update_or_create(
            symbol=symbol, date=date, defaults={'predicted_close': predicted_close})
