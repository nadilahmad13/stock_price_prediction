import pandas as pd
import joblib
from ..repositories.PredictionRepository import StockPredictionRepository
from ..repositories.StockDataRepository import StockDataRepository
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF


class PredictionUseCase:
    @staticmethod
    def predict_stock_price(symbol, initial_date=None, end_date=None):
        model = joblib.load('./api/model/stock_price_prediction_model.pkl')

        if initial_date and end_date:
            if isinstance(initial_date, str):
                initial_date = datetime.strptime(initial_date, '%Y-%m-%d')
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d')

            date_range = (end_date - initial_date).days + 1
            future_dates = np.array(
                [initial_date.toordinal() + i for i in range(date_range)]).reshape(-1, 1)
        else:
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

    def generate_prediction_report(symbol):
        history = StockDataRepository.get_stock_data_by_symbol(symbol).values()

        if not history:
            return {"error": "Stock data not found"}

        history_df = pd.DataFrame(history)
        history_df['date'] = pd.to_datetime(history_df['date'])
        history_df.set_index('date', inplace=True)

        initial_date = datetime.strptime(
            str(history_df.index[0]), '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(
            str(history_df.index[-1]), '%Y-%m-%d %H:%M:%S')
        count = initial_date - end_date

        prediction = PredictionUseCase.predict_stock_price(
            symbol, initial_date=datetime.now()-timedelta(days=count.days), end_date=datetime.now())
        prediction_df = pd.DataFrame(prediction)
        prediction_df['date'] = pd.to_datetime(prediction_df['date'])
        prediction_df.set_index('date', inplace=True)

        plt.figure(figsize=(12, 6))
        plt.scatter(
            history_df.index, history_df['close_price'], label='Historical Price', color='blue')
        plt.plot(prediction_df.index,
                 prediction_df['predicted_close'], label='Predicted Price', color='red')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'{symbol} Stock Price Actual vs Prediction')
        plt.legend()
        plt.savefig('./result/prediction_plot.png')

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        image_path = './result/prediction_plot.png'
        image_width = 270
        pdf.image(image_path, x=(pdf.w - image_width) / 2, w=image_width)

        pdf.output('./result/prediction_report.pdf')

        return open('./result/prediction_report.pdf', 'rb')
