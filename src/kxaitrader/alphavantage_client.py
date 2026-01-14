"""
Alpha Vantage API client for fetching market data.
"""

import time
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import requests

from .config import Config


class AlphaVantageClient:
    """Client for fetching data from Alpha Vantage API."""

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, config: Config):
        """Initialize the client with configuration."""
        self.config = config
        self.api_key = config.alpha_vantage_api_key
        self._last_request_time = 0
        self._min_request_interval = 12  # Alpha Vantage free tier: 5 requests/minute

    def _rate_limit(self):
        """Implement rate limiting for API calls."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_request_interval:
            time.sleep(self._min_request_interval - elapsed)
        self._last_request_time = time.time()

    def _make_request(self, params: dict) -> dict:
        """Make a rate-limited request to the API."""
        self._rate_limit()
        params["apikey"] = self.api_key
        response = requests.get(self.BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            raise ValueError(f"API Error: {data['Error Message']}")
        if "Note" in data:
            raise ConnectionError(f"API Rate Limit: {data['Note']}")

        return data

    def get_daily_data(
        self,
        symbol: str,
        outputsize: str = "compact",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Fetch daily time series data for a symbol.

        Args:
            symbol: Stock ticker symbol
            outputsize: 'compact' (100 days) or 'full' (20+ years)
            start_date: Optional start date filter (YYYY-MM-DD)
            end_date: Optional end date filter (YYYY-MM-DD)

        Returns:
            DataFrame with columns: open, high, low, close, volume
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,
        }

        data = self._make_request(params)
        time_series = data.get("Time Series (Daily)", {})

        if not time_series:
            raise ValueError(f"No daily data found for {symbol}")

        # Convert to DataFrame
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df.index = pd.to_datetime(df.index)
        df.columns = ["open", "high", "low", "close", "volume"]
        df = df.astype({
            "open": float,
            "high": float,
            "low": float,
            "close": float,
            "volume": int,
        })
        df = df.sort_index()

        # Apply date filters
        if start_date:
            df = df[df.index >= start_date]
        if end_date:
            df = df[df.index <= end_date]

        return df

    def get_intraday_data(
        self,
        symbol: str,
        interval: str = "5min",
        outputsize: str = "compact",
    ) -> pd.DataFrame:
        """
        Fetch intraday time series data for a symbol.

        Args:
            symbol: Stock ticker symbol
            interval: Time interval (1min, 5min, 15min, 30min, 60min)
            outputsize: 'compact' or 'full'

        Returns:
            DataFrame with columns: open, high, low, close, volume
        """
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
        }

        data = self._make_request(params)
        time_series_key = f"Time Series ({interval})"
        time_series = data.get(time_series_key, {})

        if not time_series:
            raise ValueError(f"No intraday data found for {symbol}")

        # Convert to DataFrame
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df.index = pd.to_datetime(df.index)
        df.columns = ["open", "high", "low", "close", "volume"]
        df = df.astype({
            "open": float,
            "high": float,
            "low": float,
            "close": float,
            "volume": int,
        })
        df = df.sort_index()

        return df

    def get_quote(self, symbol: str) -> dict:
        """
        Get the latest quote for a symbol.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary with quote data
        """
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
        }

        data = self._make_request(params)
        quote = data.get("Global Quote", {})

        if not quote:
            raise ValueError(f"No quote data found for {symbol}")

        return {
            "symbol": quote.get("01. symbol"),
            "open": float(quote.get("02. open", 0)),
            "high": float(quote.get("03. high", 0)),
            "low": float(quote.get("04. low", 0)),
            "price": float(quote.get("05. price", 0)),
            "volume": int(quote.get("06. volume", 0)),
            "latest_trading_day": quote.get("07. latest trading day"),
            "previous_close": float(quote.get("08. previous close", 0)),
            "change": float(quote.get("09. change", 0)),
            "change_percent": quote.get("10. change percent", "0%").replace("%", ""),
        }

    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators from price data.

        Args:
            df: DataFrame with OHLCV data

        Returns:
            DataFrame with additional technical indicator columns
        """
        df = df.copy()

        # Simple Moving Averages
        df["sma_20"] = df["close"].rolling(window=20).mean()
        df["sma_50"] = df["close"].rolling(window=50).mean()
        df["sma_200"] = df["close"].rolling(window=200).mean()

        # Bollinger Bands (20-period, 2 std dev)
        df["boll_mid"] = df["sma_20"]
        df["boll_std"] = df["close"].rolling(window=20).std()
        df["boll_upper"] = df["boll_mid"] + (2 * df["boll_std"])
        df["boll_lower"] = df["boll_mid"] - (2 * df["boll_std"])

        # RSI (14-period)
        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))

        # MACD (12-26-9)
        ema_12 = df["close"].ewm(span=12, adjust=False).mean()
        ema_26 = df["close"].ewm(span=26, adjust=False).mean()
        df["macd"] = ema_12 - ema_26
        df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
        df["macd_hist"] = df["macd"] - df["macd_signal"]

        # ATR (14-period)
        high_low = df["high"] - df["low"]
        high_close = (df["high"] - df["close"].shift()).abs()
        low_close = (df["low"] - df["close"].shift()).abs()
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df["atr"] = true_range.rolling(window=14).mean()

        # Volume Moving Average
        df["volume_sma"] = df["volume"].rolling(window=20).mean()

        return df
