from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from ..usecases.PredictionUseCase import PredictionUseCase
from django.http import FileResponse


class PredictionReportView(APIView):
    def get(self, request):
        symbol = request.data.get('symbol', 'NVDA')

        report_pdf = PredictionUseCase.generate_prediction_report(symbol)

        return FileResponse(report_pdf, as_attachment=True, filename=f"backtest_report_{symbol}_{datetime.now().strftime('%Y-%m-%d')}.pdf")
