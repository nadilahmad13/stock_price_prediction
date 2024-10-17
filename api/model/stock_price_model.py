# stock_price_model.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_csv('historical_data.csv')

df['previous_close'] = df['close_price'].shift(1)
df.dropna(inplace=True)

X = df[['previous_close']]
y = df['close_price']

split = int(len(df) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

model = LinearRegression()
model.fit(X_train, y_train)

# test to predict the price of the first row in the test data
predicted_price = model.predict(X_test.iloc[[0]])[0]

print("Predicted price:", predicted_price)

# # Save the trained model to a file (e.g., stock_price_model.pkl)
# joblib.dump(model, 'stock_price_model.pkl')

# print("Model trained and saved successfully.")
