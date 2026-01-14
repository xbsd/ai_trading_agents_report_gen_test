#!/usr/bin/env python3
"""
Test script for the KXAITrader report generation system.
"""

import json
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kxaitrader import ReportGenerator, Config


def main():
    # Get API key from environment (check multiple common names)
    # Note: Not strictly required when using sample data
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") or os.getenv("ALPHAVANTAGE_KEY") or os.getenv("ALPHAVANTAGE_API_KEY") or "SAMPLE_MODE"

    if api_key == "SAMPLE_MODE":
        print("No API key found - running with sample data only")
    else:
        print(f"API Key found: {api_key[:8]}...")

    # Load the JSON analysis file
    json_path = Path(__file__).parent / "final-report-ai_trading_agents.json.txt"
    if json_path.exists():
        print(f"Loading agent analysis from: {json_path}")
        with open(json_path, "r", encoding="utf-8") as f:
            json_analysis = json.load(f)
    else:
        print("No JSON analysis file found, proceeding without agent data")
        json_analysis = None

    # Create config
    config = Config(
        alpha_vantage_api_key=api_key,
        output_dir=Path("./output"),
        chart_format="png",
    )

    # Generate report
    generator = ReportGenerator(config=config)

    print("\nGenerating report for ORCL...")
    print("=" * 60)

    try:
        result = generator.generate_report(
            symbol="ORCL",
            json_analysis=json_analysis,
            include_charts=True,
            include_news=False,
            include_intraday=False,
            output_format="html",
            use_sample_data=True,  # Use sample data for demonstration
        )

        print("\n" + "=" * 60)
        print("REPORT GENERATION COMPLETE")
        print("=" * 60)
        print(f"\nOutput: {result['output_path']}")
        print(f"Data points: {result['data_points']}")
        print(f"Charts generated: {len(result.get('charts', {}))}")

        for chart_name in result.get("charts", {}).keys():
            print(f"  - {chart_name}")

    except Exception as e:
        print(f"\nError generating report: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
