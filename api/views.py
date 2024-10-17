from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import StockPrice
from .serializer import StockDataSerializer
import requests

ALPHA_VANTAGE_API_KEY = 'D1U1GP6B39O48KSG'
API_URL = 'https://www.alphavantage.co/query'


@api_view(['GET'])
def get_stock_price(request):
    # Get the stock symbol from the query parameters (if provided)
    stock_symbol = request.query_params.get('symbol', None)

    # If a stock symbol is provided, filter data for that stock
    if stock_symbol:
        stock_data = StockPrice.objects.filter(
            symbol=stock_symbol).order_by('-date')
    else:
        # Otherwise, return all stock data
        stock_data = StockPrice.objects.all().order_by('-date')

    # Serialize the data
    serializer = StockDataSerializer(stock_data, many=True)

    # Return the serialized data
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_stock_price(request):
    # Get the stock symbol from the request body
    stock_symbol = request.data.get('symbol')

    if not stock_symbol:
        return Response({"error": "Stock symbol is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Alpha Vantage API Key (put your key in settings or .env)
    api_key = ALPHA_VANTAGE_API_KEY
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={
        stock_symbol}&apikey={api_key}"

    # Fetch data from the API
    response = requests.get(url)

    if response.status_code != 200:
        return Response({"error": "Failed to fetch data from Alpha Vantage"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    data = response.json()

    # Check if "Time Series (Daily)" exists in the response
    if "Time Series (Daily)" not in data:
        return Response({"error": "Invalid data format from Alpha Vantage"}, status=status.HTTP_400_BAD_REQUEST)

    # Extract the daily data
    time_series = data["Time Series (Daily)"]

    # Iterate through each date in the daily data and save it to the database
    for date, daily_data in time_series.items():
        stock_data = {
            'symbol': stock_symbol,
            'date': date,
            'open_price': daily_data["1. open"],
            'high_price': daily_data["2. high"],
            'low_price': daily_data["3. low"],
            'close_price': daily_data["4. close"],
            'volume': daily_data["5. volume"]
        }

        # Serialize and save each record to the database
        serializer = StockDataSerializer(data=stock_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Stock data fetched and saved successfully"}, status=status.HTTP_201_CREATED)
