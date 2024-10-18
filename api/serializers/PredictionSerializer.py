from rest_framework import serializers
from ..models import StockPrediction


class StockPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrediction
        fields = ['symbol', 'date', 'prediction_close']
