from ..models import StockData


class StockDataRepository:
    @staticmethod
    def get_all_stock_data():
        return StockData.objects.all().order_by('-date')

    @staticmethod
    def get_stock_data_by_symbol(stock_symbol):
        return StockData.objects.filter(symbol=stock_symbol).order_by('-date')

    @staticmethod
    def create_stock_data(data):
        StockData.objects.update_or_create(
            symbol=data['symbol'],
            date=data['date'],
            defaults={
                'open_price': data['open_price'],
                'high_price': data['high_price'],
                'low_price': data['low_price'],
                'close_price': data['close_price'],
                'volume': data['volume']
            }
        )
