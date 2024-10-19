import pandas as pd
from ..repositories.StockDataRepository import StockDataRepository
import matplotlib.pyplot as plt
from fpdf import FPDF


class BackTestingUseCase:
    @staticmethod
    def run_backtest(symbol, initial_investment, short_ma_days, long_ma_days):
        stock_data = StockDataRepository.get_stock_data_by_symbol(symbol).values(
            'date', 'close_price', 'open_price', 'high_price', 'low_price', 'volume')
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
        actions = []

        for index, row in df.iterrows():
            # Skip rows where moving averages are not available
            if pd.isna(row['short_ma']) or pd.isna(row['long_ma']):
                continue

            # Buy signal
            if row['close_price'] < row['short_ma'] and cash > 0:
                shares = cash / row['close_price']
                cash = 0
                trades += 1
                actions.append({"date": index, "action": "buy",
                               "price": row['close_price']})
            # Sell signal
            elif row['close_price'] > row['long_ma'] and shares > 0:
                cash = shares * row['close_price']
                shares = 0
                trades += 1
                actions.append({"date": index, "action": "sell",
                               "price": row['close_price']})

            # Update peak value and max drawdown
            portfolio_value = cash + shares * row['close_price']
            peak_value = max(peak_value, portfolio_value)
            drawdown = (peak_value - portfolio_value) / peak_value
            max_drawdown = max(max_drawdown, drawdown)

        final_portfolio_value = cash + shares * df.iloc[-1]['close_price']
        total_return = final_portfolio_value - initial_investment

        return {
            "total_return": total_return,
            "max_drawdown": max_drawdown,
            "number_of_trades": trades,
            "final_value": final_portfolio_value,
            "actions": actions
        }

    @staticmethod
    def generate_backtest_report(params, backtest_results):
        stock_data = StockDataRepository.get_stock_data_by_symbol(
            params['symbol']).values()
        if not stock_data:
            return {"error": "No stock data found for the given symbol."}

        stock_df = pd.DataFrame(stock_data)
        stock_df['date'] = pd.to_datetime(stock_df['date'])
        stock_df.set_index('date', inplace=True)

        plt.figure(figsize=(14, 8))
        plt.plot(stock_df.index, stock_df['close_price'],
                 label='Stock Price', color='blue')

        buy_signals = [(action['date'], action['price'])
                       for action in backtest_results['actions'] if action['action'] == 'buy']
        sell_signals = [(action['date'], action['price'])
                        for action in backtest_results['actions'] if action['action'] == 'sell']

        if buy_signals:
            buy_dates, buy_prices = zip(*buy_signals)
            plt.scatter(buy_dates, buy_prices,
                        color='green', label='Buy Signal')

        if sell_signals:
            sell_dates, sell_prices = zip(*sell_signals)
            plt.scatter(sell_dates, sell_prices,
                        color='red', label='Sell Signal')

        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.title('Stock Price & Buy/Sell Signals')
        plt.legend()

        plt.savefig('./result/plot.png')

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(
            0, 10, txt=f"Backtest Report - {stock_df['symbol'][0]}", ln=True, align='C')

        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(0, 10, txt="Results", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.set_xy(10, 30)
        pdf.cell(0, 10, txt=f"Total Return: {backtest_results['total_return']:.4f}", ln=True)
        pdf.set_xy(10, 40)
        pdf.cell(0, 10, txt=f"Max Drawdown: {backtest_results['max_drawdown']:.4f}", ln=True)
        pdf.set_xy(10, 50)
        pdf.cell(0, 10, txt=f"Number of Trades: {backtest_results['number_of_trades']}", ln=True)
        pdf.set_xy(10, 60)
        pdf.cell(0, 10, txt=f"Final Portfolio Value: {backtest_results['final_value']:.4f}", ln=True)

        pdf.set_font("Arial", 'B', size=12)
        pdf.set_xy(150, 20)
        pdf.cell(0, 10, txt="Parameters", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.set_xy(150, 30)
        pdf.cell(0, 10, txt=f"Initial Investment: {params['initial_investment']}", ln=True)
        pdf.set_xy(150, 40)
        pdf.cell(0, 10, txt=f"Short MA Days: {params['short_ma_days']}", ln=True)
        pdf.set_xy(150, 50)
        pdf.cell(0, 10, txt=f"Long MA Days: {params['long_ma_days']}", ln=True)

        pdf.image('./result/plot.png', x=10, y=60, w=270)

        pdf.output('./result/report.pdf', 'F')

        return open('./result/report.pdf', 'rb')
