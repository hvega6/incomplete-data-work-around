"""Compute daily and cumulative returns with filled missing values."""

import os
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf  # Import yfinance to fetch data

def get_data(symbols, dates):
    """Fetch stock data (adjusted close) for given symbols from Yahoo Finance."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = yf.download(symbol, start=dates[0], end=dates[-1])['Adj Close']
        df_temp = df_temp.rename(symbol)
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns = df.pct_change()  # Calculate percentage change
    daily_returns.iloc[0] = 0  # Set the first value to zero
    return daily_returns  # Return the DataFrame of daily returns

def compute_cumulative_returns(daily_returns):
    """Compute and return cumulative returns."""
    cumulative_returns = (1 + daily_returns).cumprod() - 1  # Cumulative product of daily returns
    return cumulative_returns  # Return the DataFrame of cumulative returns

def fill_missing_values(df):
    """Fill missing values in the DataFrame."""
    df_filled = df.ffill()  # Forward fill
    # Alternatively, you can use:
    # df_filled = df.bfill()  # Backward fill
    # df_filled = df.fillna(0)  # Fill with zero
    # df_filled = df.fillna(df.mean())  # Fill with the mean of the column
    return df_filled

def test_run():
    # Read data
    dates = pd.date_range('2012-07-01', '2012-07-31')  # one month only
    symbols = ['SPY', 'XOM']
    df = get_data(symbols, dates)

    # Fill missing values
    df_filled = fill_missing_values(df)
    plot_data(df_filled, title="Filled Stock Prices")

    # Compute daily returns
    daily_returns = compute_daily_returns(df_filled)
    plot_data(daily_returns, title="Daily Returns", ylabel="Daily Returns")

    # Compute cumulative returns
    cumulative_returns = compute_cumulative_returns(daily_returns)
    plot_data(cumulative_returns, title="Cumulative Returns", ylabel="Cumulative Returns")

if __name__ == "__main__":
    test_run()
