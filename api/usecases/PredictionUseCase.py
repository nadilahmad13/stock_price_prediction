import pandas as pd
import joblib
from ..repositories.StockDataRepository import StockDataRepository
from ..repositories.PredictionRepository import StockPredictionRepository
from datetime import timedelta


class PredictionUseCase:
    @staticmethod
    def predict_stock_price(symbol):
        model = joblib.load('api\model\stock_price_model.pkl')
        stock_data = StockDataRepository.get_stock_data_by_symbol(symbol).values(
            'date', 'close_price', 'open_price', 'high_price', 'low_price', 'volume')
        if not stock_data:
            return None
        df = pd.DataFrame(stock_data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        last_close_price = df['close_price'].iloc[-1]
        prediction_input = [[last_close_price]]
        prediction_input = [[float(i) for i in prediction_input[0]]]

        predictions = []
        date = df.index[0]
        for i in range(30):
            predicted_price = model.predict(prediction_input)[0]
            date += timedelta(days=1)
            predictions.append(
                {"date": date, "predicted_close": predicted_price})

            prediction_input = [[predicted_price]]

        return predictions

    def save_stock_prediction(symbol, predictions):
        for prediction in predictions:
            StockPredictionRepository.save_stock_prediction(
                symbol, prediction['date'], prediction['predicted_close'])
