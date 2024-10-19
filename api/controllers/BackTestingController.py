from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..usecases.BackTestingUseCase import BacktestingUseCase


class BacktestingController(APIView):
    def get(self, request):
        data = request.data
        result = BacktestingUseCase.run_backtest(
            symbol=data.get('symbol','NVDA'),
            initial_investment=data.get('initial_investment', 10000),
            short_ma_days=data.get('short_ma_days', 50),
            long_ma_days=data.get('long_ma_days', 200)
        )

        if not result:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)
