from rest_framework.response import Response
from rest_framework.views import APIView
from ..usecases.PredictionUseCase import PredictionUseCase


class StockPricePredictionView(APIView):
    def get(self, request):
        symbol = request.data.get('symbol', 'NVDA')

        predictions = PredictionUseCase.predict_stock_price(symbol)

        if not predictions:
            return Response({"error": "Stock data not found"})

        PredictionUseCase.save_stock_prediction(symbol, predictions)

        return Response({"symbol": symbol, "predictions": predictions})
