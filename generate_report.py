#!/usr/bin/env python3
"""
KXAITrader Report Generation Script

Generate comprehensive trading analysis reports with automated chart generation
and market data enrichment.

Usage:
    python generate_report.py ORCL --api-key YOUR_API_KEY
    python generate_report.py AAPL --json analysis.json --format html
    python generate_report.py TSLA --no-charts --format markdown

Requirements:
    pip install -r requirements.txt
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kxaitrader import ReportGenerator, Config, AlphaVantageClient, ChartGenerator


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate KXAITrader trading analysis reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic report generation
  python generate_report.py ORCL --api-key YOUR_KEY

  # With JSON analysis from trading agents
  python generate_report.py AAPL --api-key YOUR_KEY --json agent_analysis.json

  # Markdown output without charts
  python generate_report.py MSFT --api-key YOUR_KEY --format markdown --no-charts

  # Custom date range
  python generate_report.py GOOGL --api-key YOUR_KEY --start 2024-01-01 --end 2024-06-30

Environment Variables:
  ALPHA_VANTAGE_API_KEY - API key (alternative to --api-key flag)
  OUTPUT_DIR - Output directory (default: ./output)
        """
    )

    parser.add_argument(
        "symbol",
        help="Stock ticker symbol (e.g., ORCL, AAPL, TSLA)"
    )

    parser.add_argument(
        "--api-key", "-k",
        help="Alpha Vantage API key (or set ALPHA_VANTAGE_API_KEY env var)"
    )

    parser.add_argument(
        "--json", "-j",
        type=Path,
        help="Path to JSON file with trading agent analysis"
    )

    parser.add_argument(
        "--format", "-f",
        choices=["html", "markdown"],
        default="html",
        help="Output format (default: html)"
    )

    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=Path("./output"),
        help="Output directory (default: ./output)"
    )

    parser.add_argument(
        "--no-charts",
        action="store_true",
        help="Skip chart generation"
    )

    parser.add_argument(
        "--no-news",
        action="store_true",
        help="Skip news fetching"
    )

    parser.add_argument(
        "--intraday",
        action="store_true",
        help="Include intraday data analysis"
    )

    parser.add_argument(
        "--start",
        help="Start date for analysis (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--end",
        help="End date for analysis (YYYY-MM-DD)"
    )

    parser.add_argument(
        "--chart-format",
        choices=["png", "svg", "html"],
        default="png",
        help="Chart image format (default: png)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    return parser.parse_args()


def load_json_analysis(json_path: Path) -> dict:
    """Load JSON analysis file."""
    if not json_path.exists():
        print(f"Error: JSON file not found: {json_path}")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    """Main entry point."""
    args = parse_args()

    # Get API key (check multiple common names)
    api_key = args.api_key or os.getenv("ALPHA_VANTAGE_API_KEY") or os.getenv("ALPHAVANTAGE_KEY") or os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        print("Error: Alpha Vantage API key required.")
        print("Set ALPHA_VANTAGE_API_KEY environment variable or use --api-key flag")
        print("\nGet your free API key at: https://www.alphavantage.co/support/#api-key")
        sys.exit(1)

    # Create config
    config = Config(
        alpha_vantage_api_key=api_key,
        output_dir=args.output_dir,
        chart_format=args.chart_format
    )

    # Load JSON analysis if provided
    json_analysis = None
    if args.json:
        print(f"Loading agent analysis from: {args.json}")
        json_analysis = load_json_analysis(args.json)

    # Parse date range
    date_range = None
    if args.start or args.end:
        start = args.start or (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        end = args.end or datetime.now().strftime("%Y-%m-%d")
        date_range = (start, end)

    try:
        # Generate report
        generator = ReportGenerator(config=config)

        result = generator.generate_report(
            symbol=args.symbol.upper(),
            json_analysis=json_analysis,
            include_charts=not args.no_charts,
            include_news=not args.no_news,
            include_intraday=args.intraday,
            output_format=args.format,
            date_range=date_range
        )

        # Print summary
        print("\n" + "=" * 60)
        print("REPORT GENERATION COMPLETE")
        print("=" * 60)
        print(f"\nSymbol: {args.symbol.upper()}")
        print(f"Format: {args.format.upper()}")
        print(f"Output: {result['output_path']}")

        if result.get("charts"):
            print(f"\nCharts generated ({len(result['charts'])}):")
            for chart_type, path in result["charts"].items():
                print(f"  - {chart_type}: {path}")

        print("\n" + "=" * 60)

    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except ConnectionError as e:
        print(f"\nConnection Error: {e}")
        print("Check your internet connection and API key.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
