from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from ..repositories.StockDataRepository import StockDataRepository
from ..usecases.BackTestingUseCase import BacktestingUseCase


class BacktestReportView(APIView):
    def get(self, request):
        params = {
            'symbol': request.data.get('symbol', 'NVDA'),
            'initial_investment': request.data.get('initial_investment', 10000),
            'short_ma_days': request.data.get('short_ma_days', 50),
            'long_ma_days': request.data.get('long_ma_days', 200)
        }
        # Get the stock data from the database
        stock_data = StockDataRepository.get_stock_data_by_symbol(
            params['symbol']).values()
        if not stock_data:
            return Response({"error": "No stock data found for the given symbol."}, status=404)

        # Run the backtest (parameters can be customized as needed)
        backtest_results = BacktestingUseCase.run_backtest(
            params['symbol'], initial_investment=params['initial_investment'], short_ma_days=params['short_ma_days'], long_ma_days=params['long_ma_days'])

        # Generate the report
        report_pdf = BacktestingUseCase.generate_backtest_report(params,
                                                                 backtest_results, stock_data)

        # Return the PDF file as a response
        return FileResponse(report_pdf, as_attachment=True, filename=f"backtest_report_{params['symbol']}_{datetime.now().strftime('%Y-%m-%d')}.pdf")
