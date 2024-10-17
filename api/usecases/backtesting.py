import pandas as pd
from ..repositories.stock_data import StockDataRepository


class BacktestingUseCase:
    @staticmethod
    def run_backtest(symbol, initial_investment, short_ma_days, long_ma_days):
        stock_data = StockDataRepository.get_stock_data_by_symbol(symbol)
        if not stock_data:
            return None

        df = pd.DataFrame(stock_data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Calculate moving averages
        df['short_ma'] = df['close_price'].rolling(window=short_ma_days).mean()
        df['long_ma'] = df['close_price'].rolling(window=long_ma_days).mean()

        # Backtesting logic
        cash = initial_investment
        shares = 0
        trades = 0
        max_drawdown = 0
        peak_value = initial_investment

        for _, row in df.iterrows():
            # Buy condition
            if row['close_price'] < row['short_ma'] and cash > 0:
                shares = cash / row['close_price']
                cash = 0
                trades += 1

            # Sell condition
            elif row['close_price'] > row['long_ma'] and shares > 0:
                cash = shares * row['close_price']
                shares = 0
                trades += 1

            # Portfolio value and drawdown calculation
            portfolio_value = cash + shares * row['close_price']
            peak_value = max(peak_value, portfolio_value)
            drawdown = (peak_value - portfolio_value) / peak_value
            max_drawdown = max(max_drawdown, drawdown)

        # Total return
        total_return = (
            cash + shares * df.iloc[-1]['close_price']) - initial_investment

        return {
            "total_return": total_return,
            "max_drawdown": max_drawdown,
            "number_of_trades": trades,
            "final_value": cash + shares * df.iloc[-1]['close_price']
        }
