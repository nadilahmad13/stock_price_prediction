from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.StockDataSerializer import StockDataSerializer
from ..usecases.StockDataUseCase import StockDataUseCase


class StockDataController(APIView):
    def get(self, request):
        params = {
            'symbol': request.data.get('symbol'),
            'count': request.data.get('count')
        }
        result = StockDataUseCase.get_stock_data(
            params['symbol'], params['count'])

        if not result:
            return Response({"error": "Data not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StockDataSerializer(result, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        params = {
            'symbol': request.data.get('symbol'),
            'outputsize': request.data.get('outputsize', 'full')
        }

        result = StockDataUseCase.create_stock_data(params)

        if 'error' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)
