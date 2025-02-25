#!/usr/bin/env python
"""
Back-Testing Suite for Trading Strategies

This script implements a comprehensive back-testing framework for evaluating trading strategies.
It uses VectorBT for efficient vectorized backtesting, yfinance for data acquisition,
and QuantStats for performance analysis and visualization.

The sample strategy implemented is a Moving Average Crossover:
- Buy signal: When fast MA crosses above slow MA
- Sell signal: When fast MA crosses below slow MA

Dependencies:
- yfinance: For downloading historical market data
- vectorbt: For vectorized backtesting
- quantstats: For performance metrics and visualizations
- pandas: For data manipulation
- matplotlib: For plotting

Install dependencies with:
pip install yfinance vectorbt quantstats pandas matplotlib
"""

# Set matplotlib to use a non-interactive backend to avoid Tkinter errors
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import yfinance as yf
import vectorbt as vbt
import quantstats as qs
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

# Configure VectorBT settings - fixed for compatibility with current version
vbt.settings.array_wrapper['freq'] = '1d'

def load_data(symbol, start_date, end_date):
    """
    Load historical price data for the specified symbol and date range.
    
    Parameters:
    -----------
    symbol : str
        The ticker symbol to download data for
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing the historical OHLCV data
    """
    print(f"Loading data for {symbol} from {start_date} to {end_date}...")
    data = yf.download(symbol, start=start_date, end=end_date)
    
    # Check if data was successfully downloaded
    if data.empty:
        raise ValueError(f"No data found for {symbol} in the specified date range")
        
    print(f"Successfully loaded {len(data)} data points")
    return data

def moving_average_crossover(close_prices, fast_window, slow_window):
    """
    Generate entry and exit signals based on moving average crossover strategy.
    
    Parameters:
    -----------
    close_prices : pd.Series
        Series of closing prices
    fast_window : int
        Window size for the fast moving average
    slow_window : int
        Window size for the slow moving average
        
    Returns:
    --------
    tuple
        (entries, exits) - Boolean Series indicating buy and sell signals
    """
    # Calculate moving averages
    fast_ma = close_prices.rolling(window=fast_window).mean()
    slow_ma = close_prices.rolling(window=slow_window).mean()
    
    # Generate signals based on crossovers
    # Buy when fast MA crosses above slow MA
    entries = (fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))
    
    # Sell when fast MA crosses below slow MA
    exits = (fast_ma < slow_ma) & (fast_ma.shift(1) >= slow_ma.shift(1))
    
    return entries, exits, fast_ma, slow_ma

def run_backtest(close_prices, entries, exits, initial_cash=10000):
    """
    Run backtest using the provided signals.
    
    Parameters:
    -----------
    close_prices : pd.Series
        Series of closing prices
    entries : pd.Series
        Boolean Series indicating buy signals
    exits : pd.Series
        Boolean Series indicating sell signals
    initial_cash : float
        Initial capital for the backtest
        
    Returns:
    --------
    vbt.Portfolio
        Portfolio object containing backtest results
    """
    print("Running backtest...")
    
    # Create portfolio object with the generated signals
    portfolio = vbt.Portfolio.from_signals(
        close_prices,
        entries,
        exits,
        init_cash=initial_cash,
        fees=0.001,  # 0.1% trading fee
        freq='1D'
    )
    
    return portfolio

def calculate_metrics(portfolio, symbol):
    """
    Calculate and display key performance metrics.
    
    Parameters:
    -----------
    portfolio : vbt.Portfolio
        Portfolio object from backtest
    symbol : str
        The ticker symbol
        
    Returns:
    --------
    pd.Series
        Returns series for further analysis
    """
    # Extract portfolio returns
    returns = portfolio.returns()
    
    # For a single symbol, extract the series
    if isinstance(returns, pd.DataFrame) and symbol in returns.columns:
        returns = returns[symbol]
    
    # Prepare returns for QuantStats (ensure it's a Series with proper index)
    # Make sure we have a flattened 1D array for the values
    flat_values = returns.values.flatten() if hasattr(returns.values, 'flatten') else returns.values
    returns = pd.Series(flat_values, index=pd.to_datetime(returns.index), name='Strategy')
    
    # Calculate key metrics
    total_return = portfolio.total_return()
    sharpe_ratio = portfolio.sharpe_ratio()
    max_drawdown = portfolio.max_drawdown()
    win_rate = portfolio.trades.win_rate()
    
    # Handle Series objects by converting to scalar values if needed
    if isinstance(total_return, pd.Series):
        total_return = total_return.iloc[0] if len(total_return) > 0 else 0
    if isinstance(sharpe_ratio, pd.Series):
        sharpe_ratio = sharpe_ratio.iloc[0] if len(sharpe_ratio) > 0 else 0
    if isinstance(max_drawdown, pd.Series):
        max_drawdown = max_drawdown.iloc[0] if len(max_drawdown) > 0 else 0
    if isinstance(win_rate, pd.Series):
        win_rate = win_rate.iloc[0] if len(win_rate) > 0 else 0
    
    # Print performance metrics
    print("\n==== Performance Metrics ====")
    print(f"Total Return: {total_return:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
    print(f"Maximum Drawdown: {max_drawdown:.2%}")
    print(f"Win Rate: {win_rate:.2%}")
    
    # Handle trade count and duration as Series if needed
    trade_count = portfolio.trades.count()
    if isinstance(trade_count, pd.Series):
        trade_count = trade_count.iloc[0] if len(trade_count) > 0 else 0
    
    avg_duration = portfolio.trades.duration.mean()
    if isinstance(avg_duration, pd.Series):
        avg_duration = avg_duration.iloc[0] if len(avg_duration) > 0 else 0
    
    print(f"Number of Trades: {trade_count}")
    print(f"Average Trade Duration: {avg_duration:.2f} days")
    
    return returns

def visualize_results(portfolio, close_prices, fast_ma, slow_ma, symbol):
    """
    Create visualizations of the backtest results and save them to files.
    
    Parameters:
    -----------
    portfolio : vbt.Portfolio
        Portfolio object from backtest
    close_prices : pd.Series
        Series of closing prices
    fast_ma : pd.Series
        Fast moving average values
    slow_ma : pd.Series
        Slow moving average values
    symbol : str
        The ticker symbol
    """
    print("Generating visualizations...")
    
    # Create a figure for price and MA
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(close_prices.index, close_prices.values, label=f'{symbol} Price')
    plt.plot(fast_ma.index, fast_ma.values, label='Fast MA', alpha=0.7)
    plt.plot(slow_ma.index, slow_ma.values, label='Slow MA', alpha=0.7)
    
    # Plot entry and exit points
    try:
        entries = portfolio.trades.records['entry_idx']
        exits = portfolio.trades.records['exit_idx']
        entry_prices = portfolio.trades.records['entry_price']
        exit_prices = portfolio.trades.records['exit_price']
        
        entry_dates = [close_prices.index[i] for i in entries]
        exit_dates = [close_prices.index[i] if i < len(close_prices.index) else close_prices.index[-1] for i in exits]
        
        plt.scatter(entry_dates, entry_prices, color='green', marker='^', s=100, label='Buy Signal')
        plt.scatter(exit_dates, exit_prices, color='red', marker='v', s=100, label='Sell Signal')
    except Exception as e:
        print(f"Warning: Could not plot trade markers: {str(e)}")
    
    plt.title(f'{symbol} Price with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    
    # Plot portfolio value - direct matplotlib plotting instead of VectorBT
    plt.subplot(2, 1, 2)
    portfolio_value = portfolio.value()
    
    # Check if it's a Series or DataFrame and handle accordingly
    if isinstance(portfolio_value, pd.DataFrame):
        if symbol in portfolio_value.columns:
            plt.plot(portfolio_value.index, portfolio_value[symbol].values, label='Portfolio Value', color='blue')
        else:
            for col in portfolio_value.columns:
                plt.plot(portfolio_value.index, portfolio_value[col].values, label=f'Portfolio Value ({col})')
    else:
        plt.plot(portfolio_value.index, portfolio_value.values, label='Portfolio Value', color='blue')
    
    plt.title("Portfolio Value Over Time")
    plt.xlabel('Date')
    plt.ylabel('Value ($)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Save figure to file
    price_ma_file = f"{symbol}_price_ma_portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(price_ma_file)
    plt.close()
    print(f"Price and MA chart saved to: {price_ma_file}")
    
    # Plot drawdowns - direct matplotlib plotting instead of VectorBT
    plt.figure(figsize=(12, 6))
    drawdown_series = portfolio.drawdown()
    
    # Check if it's a Series or DataFrame and handle accordingly
    if isinstance(drawdown_series, pd.DataFrame):
        if symbol in drawdown_series.columns:
            plt.plot(drawdown_series.index, drawdown_series[symbol].values, label='Drawdown', color='red')
        else:
            for col in drawdown_series.columns:
                plt.plot(drawdown_series.index, drawdown_series[col].values, label=f'Drawdown ({col})')
    else:
        plt.plot(drawdown_series.index, drawdown_series.values, label='Drawdown', color='red')
    
    plt.title("Portfolio Drawdowns")
    plt.xlabel('Date')
    plt.ylabel('Drawdown (%)')
    plt.legend()
    plt.grid(True)
    
    # Fill between with appropriate data based on type
    if isinstance(drawdown_series, pd.DataFrame):
        if symbol in drawdown_series.columns:
            plt.fill_between(drawdown_series.index, 0, drawdown_series[symbol].values, color='red', alpha=0.3)
        else:
            for i, col in enumerate(drawdown_series.columns):
                plt.fill_between(drawdown_series.index, 0, drawdown_series[col].values, alpha=0.3)
    else:
        fill_values = drawdown_series.values
        if hasattr(fill_values, 'flatten'):
            fill_values = fill_values.flatten()
        plt.fill_between(drawdown_series.index, 0, fill_values, color='red', alpha=0.3)
    
    plt.tight_layout()
    
    # Save drawdowns to file
    drawdowns_file = f"{symbol}_drawdowns_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(drawdowns_file)
    plt.close()
    print(f"Drawdowns chart saved to: {drawdowns_file}")

def generate_quantstats_report(returns, benchmark_symbol='SPY', start_date=None, end_date=None):
    """
    Generate a QuantStats performance report.
    
    Parameters:
    -----------
    returns : pd.Series
        Strategy returns series
    benchmark_symbol : str
        Symbol to use as benchmark (default: SPY)
    start_date : str
        Start date for benchmark data
    end_date : str
        End date for benchmark data
    """
    try:
        print(f"Generating QuantStats report with {benchmark_symbol} as benchmark...")
        
        # Ensure returns is a proper pandas Series of percent changes
        if not isinstance(returns, pd.Series):
            raise ValueError("Returns must be a pandas Series")
            
        # Download benchmark data
        benchmark_data = yf.download(
            benchmark_symbol, 
            start=start_date,
            end=end_date
        )
        
        # Calculate benchmark returns
        benchmark_returns = benchmark_data['Close'].pct_change().dropna()
        
        # Prepare the benchmark returns as a Series
        benchmark_returns = pd.Series(
            benchmark_returns.values,
            index=benchmark_returns.index,
            name=benchmark_symbol
        )
        
        # Print key comparative metrics even if the HTML report fails
        print("\n=== Strategy vs Benchmark ===")
        strategy_cagr = qs.stats.cagr(returns)
        benchmark_cagr = qs.stats.cagr(benchmark_returns)
        print(f"CAGR: Strategy: {strategy_cagr:.2%}, Benchmark: {benchmark_cagr:.2%}")
        
        strategy_sharpe = qs.stats.sharpe(returns)
        benchmark_sharpe = qs.stats.sharpe(benchmark_returns)
        print(f"Sharpe Ratio: Strategy: {strategy_sharpe:.2f}, Benchmark: {benchmark_sharpe:.2f}")
        
        strategy_maxdd = qs.stats.max_drawdown(returns)
        benchmark_maxdd = qs.stats.max_drawdown(benchmark_returns)
        print(f"Max Drawdown: Strategy: {strategy_maxdd:.2%}, Benchmark: {benchmark_maxdd:.2%}")
        
        # Basic tearsheet
        print("\nDetailed metrics for strategy:")
        qs.reports.metrics(returns, mode='basic')
        
        # Generate HTML report
        try:
            report_filename = f"quantstats_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            qs.reports.html(
                returns, 
                benchmark_returns,
                output=report_filename,
                title=f'Trading Strategy Performance Report'
            )
            print(f"Report successfully generated: {report_filename}")
        except Exception as e:
            print(f"HTML report generation failed: {str(e)}")
        
        # Create monthly returns heatmap
        plt.figure(figsize=(12, 8))
        qs.plots.monthly_heatmap(returns)
        plt.title('Monthly Returns')
        plt.tight_layout()
        
        # Save heatmap to file
        heatmap_file = f"monthly_returns_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(heatmap_file)
        plt.close()
        print(f"Monthly returns heatmap saved to: {heatmap_file}")
        
        # Create drawdowns plot
        plt.figure(figsize=(12, 8))
        qs.plots.drawdown(returns)
        plt.title('Drawdowns')
        plt.tight_layout()
        
        # Save drawdowns to file
        drawdowns_file = f"strategy_drawdowns_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(drawdowns_file)
        plt.close()
        print(f"Strategy drawdowns chart saved to: {drawdowns_file}")
        
    except Exception as e:
        print(f"Error generating QuantStats report: {str(e)}")
        print("Displaying basic metrics without benchmark comparison:")
        qs.reports.metrics(returns, mode='basic')


def main():
    """
    Main function to run the backtesting framework.
    """
    # Define trading parameters
    symbol = 'AAPL'
    start_date = '2019-01-01'
    end_date = '2022-01-01'
    initial_cash = 10000
    fast_window = 20
    slow_window = 50
    
    try:
        # Step 1: Load data
        data = load_data(symbol, start_date, end_date)
        close_prices = data['Close']
        
        # Step 2: Generate trading signals
        entries, exits, fast_ma, slow_ma = moving_average_crossover(close_prices, fast_window, slow_window)
        
        # Step 3: Run backtest
        portfolio = run_backtest(close_prices, entries, exits, initial_cash)
        
        # Step 4: Calculate performance metrics
        returns = calculate_metrics(portfolio, symbol)
        
        # Step 5: Visualize results
        visualize_results(portfolio, close_prices, fast_ma, slow_ma, symbol)
        
        # Step 6: Try to generate QuantStats report (but continue if it fails)
        try:
            generate_quantstats_report(returns, 'SPY', start_date, end_date)
        except Exception as e:
            print(f"QuantStats report generation failed: {str(e)}")
            print("Continuing with basic metrics display...")
            # Display basic metrics without comparison
            qs.reports.metrics(returns, mode='basic')
        
        print("\nBacktesting completed successfully!")
        
    except Exception as e:
        print(f"Error running backtest: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error running backtest: {str(e)}")