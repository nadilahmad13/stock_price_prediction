import pandas as pd
import joblib
from ..repositories.PredictionRepository import StockPredictionRepository
from datetime import datetime
import numpy as np


class PredictionUseCase:
    @staticmethod
    def predict_stock_price(symbol):
        model = joblib.load('./api/model/stock_price_prediction_model.pkl')
        future_dates = np.array(
            [datetime.now().toordinal() + i for i in range(1, 30 + 1)]).reshape(-1, 1)
        future_predictions = model.predict(future_dates)
        predictions = []
        for i, future_date in enumerate(future_dates):
            predictions.append({
                'date': datetime.fromordinal(int(future_date)),
                'predicted_close': future_predictions[i]
            })
        PredictionUseCase.save_stock_prediction(symbol, predictions)
        return predictions

    def save_stock_prediction(symbol, predictions):
        for prediction in predictions:
            StockPredictionRepository.save_stock_prediction(
                symbol, prediction['date'], prediction['predicted_close'])
