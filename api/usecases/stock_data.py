import requests
from ..repositories.stock_data import StockDataRepository
from dotenv import load_dotenv
import os

load_dotenv()
ALPHA_VINTAGE_API_KEY = os.environ.get('ALPHA_VINTAGE_API_KEY')
API_URL = os.environ.get('API_URL')


class StockDataUseCase:
    @staticmethod
    def get_stock_data(symbol=None):
        if symbol:
            stock_data = StockDataRepository.get_stock_data_by_symbol(
                symbol)
        else:
            stock_data = StockDataRepository.get_all_stock_data()

        return stock_data

    @staticmethod
    def create_stock_data(stock_symbol):
        if not stock_symbol:
            return {"error": "Stock symbol is required"}

        response = requests.get(
            f"{API_URL}?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={ALPHA_VINTAGE_API_KEY}")

        if response.status_code != 200:
            return {"error": "Failed to fetch data from Alpha Vantage"}

        data = response.json()

        if "Time Series (Daily)" not in data:
            return {"error": "Invalid data format from Alpha Vantage"}

        time_series = data["Time Series (Daily)"]

        for date, values in time_series.items():
            StockDataRepository.create_stock_data({
                'symbol': stock_symbol,
                'date': date,
                'open_price': values['1. open'],
                'high_price': values['2. high'],
                'low_price': values['3. low'],
                'close_price': values['4. close'],
                'volume': values['5. volume']
            })

        return {"message": "Stock data updated successfully"}
