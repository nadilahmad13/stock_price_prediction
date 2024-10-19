from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from ..repositories.StockDataRepository import StockDataRepository
from ..usecases.BackTestingUseCase import BackTestingUseCase


class BackTestingReportView(APIView):
    def get(self, request):
        params = {
            'symbol': request.data.get('symbol', 'NVDA'),
            'initial_investment': request.data.get('initial_investment', 10000),
            'short_ma_days': request.data.get('short_ma_days', 50),
            'long_ma_days': request.data.get('long_ma_days', 200)
        }

        backtest_results = BackTestingUseCase.run_backtest(
            params['symbol'], initial_investment=params['initial_investment'], short_ma_days=params['short_ma_days'], long_ma_days=params['long_ma_days'])

        report_pdf = BackTestingUseCase.generate_backtest_report(
            params, backtest_results)

        return FileResponse(report_pdf, as_attachment=True, filename=f"backtest_report_{params['symbol']}_{datetime.now().strftime('%Y-%m-%d')}.pdf")
