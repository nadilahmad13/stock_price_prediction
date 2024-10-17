from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.stock_data import StockDataSerializer
from ..usecases.stock_data import StockDataUseCase


class StockDataController(APIView):
    def get(self, request):
        stock_symbol = request.query_params.get('symbol')
        count = request.query_params.get('count')

        result = StockDataUseCase.get_stock_data(stock_symbol, count)

        serializer = StockDataSerializer(result, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        params = {
            'symbol': request.data.get('symbol'),
            'outputsize': request.data.get('outputsize', 'compact')
        }

        result = StockDataUseCase.create_stock_data(params)

        return Response(result, status=status.HTTP_200_OK)
