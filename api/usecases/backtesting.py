import pandas as pd
from ..repositories.stock_data import StockDataRepository


class BacktestingUseCase:
    @staticmethod
    def run_backtest(symbol, initial_investment, short_ma_days, long_ma_days):
        stock_data = StockDataRepository.get_stock_data_by_symbol(symbol).values('date', 'close_price', 'open_price', 'high_price', 'low_price', 'volume')
        if not stock_data:
            return {"error": "Stock data not found"}

        df = pd.DataFrame(stock_data)

        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Calculate moving averages
        df['short_ma'] = df['close_price'].rolling(
            window=short_ma_days, min_periods=1).mean()
        df['long_ma'] = df['close_price'].rolling(
            window=long_ma_days, min_periods=1).mean()

        cash = initial_investment
        shares = 0
        trades = 0
        max_drawdown = 0
        peak_value = initial_investment

        # Iterate over the stock data and apply buy/sell rules
        for index, row in df.iterrows():
            # Skip if either moving average is NaN (which will happen for the first few rows)
            if pd.isna(row['short_ma']) or pd.isna(row['long_ma']):
                continue

            # Buy condition (price below short moving average and we have cash)
            if row['close_price'] < row['short_ma'] and cash > 0:
                # Buy shares with all available cash
                shares = cash / row['close_price']
                cash = 0  # No more cash after buying
                trades += 1

            # Sell condition (price above long moving average and we hold shares)
            elif row['close_price'] > row['long_ma'] and shares > 0:
                cash = shares * row['close_price']  # Sell all shares
                shares = 0  # No more shares after selling
                trades += 1

            # Calculate the current portfolio value
            portfolio_value = cash + shares * row['close_price']

            # Update peak value and drawdown
            peak_value = max(peak_value, portfolio_value)
            drawdown = (peak_value - portfolio_value) / peak_value
            max_drawdown = max(max_drawdown, drawdown)

        # Calculate total return
        final_portfolio_value = cash + shares * df.iloc[-1]['close_price']
        total_return = final_portfolio_value - initial_investment

        return {
            "total_return": total_return,
            "max_drawdown": max_drawdown,
            "number_of_trades": trades,
            "final_value": final_portfolio_value
        }
