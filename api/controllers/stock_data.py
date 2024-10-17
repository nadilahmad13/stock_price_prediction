from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.stock_data import StockDataSerializer
from ..usecases.stock_data import StockDataUseCase


class StockDataController(APIView):
    def get(self, request):
        stock_symbol = request.query_params.get('symbol')

        result = StockDataUseCase.get_stock_data(stock_symbol)

        serializer = StockDataSerializer(result, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        stock_symbol = request.data.get('symbol')

        result = StockDataUseCase.create_stock_data(stock_symbol)

        return Response(result, status=status.HTTP_200_OK)
