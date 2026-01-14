"""
Sample market data for testing and demonstration purposes.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_sample_data(symbol: str, days: int = 365) -> pd.DataFrame:
    """
    Generate realistic sample market data for testing.

    Args:
        symbol: Stock ticker symbol
        days: Number of days of data to generate

    Returns:
        DataFrame with OHLCV data
    """
    np.random.seed(42)  # For reproducibility

    # Base prices for different symbols
    base_prices = {
        "ORCL": 200.0,
        "AAPL": 180.0,
        "MSFT": 400.0,
        "GOOGL": 140.0,
        "AMZN": 180.0,
        "TSLA": 250.0,
        "NVDA": 500.0,
    }

    base_price = base_prices.get(symbol.upper(), 100.0)

    # Generate dates (excluding weekends)
    end_date = datetime.now()
    dates = []
    current_date = end_date - timedelta(days=int(days * 1.5))

    while len(dates) < days:
        if current_date.weekday() < 5:  # Monday = 0, Friday = 4
            dates.append(current_date)
        current_date += timedelta(days=1)

    dates = dates[:days]

    # Generate price movements with realistic volatility
    returns = np.random.normal(0.0005, 0.02, days)  # Mean daily return ~0.05%, volatility ~2%

    # Add some trend and mean reversion
    trend = np.linspace(-0.1, 0.1, days)  # Slight upward trend
    mean_reversion = np.zeros(days)

    prices = [base_price]
    for i in range(1, days):
        # Add trend component
        ret = returns[i] + trend[i] * 0.01

        # Mean reversion when price moves too far
        if prices[-1] > base_price * 1.3:
            ret -= 0.005
        elif prices[-1] < base_price * 0.7:
            ret += 0.005

        new_price = prices[-1] * (1 + ret)
        prices.append(max(new_price, base_price * 0.5))  # Floor at 50% of base

    # Create OHLCV data
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        # Generate OHLC from close price
        daily_volatility = abs(np.random.normal(0, 0.015))

        high = close * (1 + daily_volatility * np.random.uniform(0.3, 1.0))
        low = close * (1 - daily_volatility * np.random.uniform(0.3, 1.0))

        # Open based on previous close with gap
        if i > 0:
            gap = np.random.normal(0, 0.005)
            open_price = prices[i - 1] * (1 + gap)
        else:
            open_price = close * (1 + np.random.uniform(-0.01, 0.01))

        # Ensure high >= max(open, close) and low <= min(open, close)
        high = max(high, open_price, close) * (1 + np.random.uniform(0, 0.005))
        low = min(low, open_price, close) * (1 - np.random.uniform(0, 0.005))

        # Generate volume (higher on big move days)
        base_volume = 15_000_000
        move_size = abs(close - open_price) / open_price
        volume = int(base_volume * (1 + move_size * 10) * np.random.uniform(0.7, 1.3))

        data.append({
            "open": round(open_price, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "close": round(close, 2),
            "volume": volume,
        })

    df = pd.DataFrame(data, index=pd.DatetimeIndex(dates))
    df.index.name = "date"

    return df


def get_sample_quote(symbol: str, df: pd.DataFrame = None) -> dict:
    """
    Generate a sample quote based on the latest data.

    Args:
        symbol: Stock ticker symbol
        df: Optional DataFrame with price data

    Returns:
        Dictionary with quote data
    """
    if df is None:
        df = generate_sample_data(symbol, days=100)

    latest = df.iloc[-1]
    prev_close = df.iloc[-2]["close"] if len(df) > 1 else latest["close"]

    change = latest["close"] - prev_close
    change_pct = (change / prev_close) * 100

    return {
        "symbol": symbol,
        "open": latest["open"],
        "high": latest["high"],
        "low": latest["low"],
        "price": latest["close"],
        "volume": latest["volume"],
        "latest_trading_day": df.index[-1].strftime("%Y-%m-%d"),
        "previous_close": prev_close,
        "change": change,
        "change_percent": f"{change_pct:.2f}",
    }
