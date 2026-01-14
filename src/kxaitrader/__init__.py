"""
KXAITrader Report Generation Module

Generate comprehensive trading analysis reports with automated chart generation
and market data enrichment.
"""

from .config import Config
from .alphavantage_client import AlphaVantageClient
from .chart_generator import ChartGenerator
from .report_generator import ReportGenerator
from .sample_data import generate_sample_data, get_sample_quote

__all__ = [
    "Config",
    "AlphaVantageClient",
    "ChartGenerator",
    "ReportGenerator",
    "generate_sample_data",
    "get_sample_quote",
]

__version__ = "1.0.0"
