from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..usecases.BackTestingUseCase import BackTestingUseCase


class BackTestingController(APIView):
    def get(self, request):
        result = BackTestingUseCase.run_backtest(
            symbol=request.data.get('symbol','NVDA'),
            initial_investment=request.data.get('initial_investment', 10000),
            short_ma_days=request.data.get('short_ma_days', 50),
            long_ma_days=request.data.get('long_ma_days', 200)
        )

        if not result:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)
