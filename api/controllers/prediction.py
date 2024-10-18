from rest_framework.response import Response
from rest_framework.views import APIView
from ..usecases.prediction import PredictionUseCase


class StockPricePredictionView(APIView):
    def get(self, request):
        symbol = request.data.get('symbol')

        predictions = PredictionUseCase.predict_stock_price(symbol)

        PredictionUseCase.save_stock_prediction(symbol, predictions)

        return Response({"symbol": symbol, "predictions": predictions})
