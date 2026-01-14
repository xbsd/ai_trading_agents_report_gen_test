"""
Report generator for creating professional trading analysis reports.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from .alphavantage_client import AlphaVantageClient
from .chart_generator import ChartGenerator
from .config import Config
from .sample_data import generate_sample_data, get_sample_quote


class ReportGenerator:
    """Generate comprehensive trading analysis reports."""

    def __init__(self, config: Config):
        """Initialize the report generator with configuration."""
        self.config = config
        self.api_client = AlphaVantageClient(config)
        self.chart_generator = ChartGenerator(config)

    def _extract_agent_findings(self, json_analysis: dict) -> dict:
        """
        Extract key findings from agent analysis JSON.

        Args:
            json_analysis: Raw JSON analysis from trading agents

        Returns:
            Dictionary with structured findings
        """
        report = json_analysis.get("report", {})
        summary = report.get("summary", {})
        headlines = report.get("report_headlines", {})
        trader_insights = headlines.get("trader_insights", {})
        findings = report.get("findings", {})
        fundamentals = findings.get("fundamentals", {}).get("summaries", {})

        return {
            "headline": summary.get("headline", ""),
            "key_findings": summary.get("key_findings", []),
            "risk_assessment": summary.get("risk_assessment", "moderate"),
            "confidence_score": summary.get("confidence_score", 0.8),
            "executive_summary": headlines.get("executive_summary", ""),
            "research_findings": headlines.get("research_findings", ""),
            "trader_insights": {
                "info": trader_insights.get("info", ""),
                "day_trader": trader_insights.get("day_trader", ""),
                "swing_trader": trader_insights.get("swing_trader", ""),
                "momentum_trader": trader_insights.get("momentum_trader", ""),
                "growth_investor": trader_insights.get("growth_investor", ""),
                "value_investor": trader_insights.get("value_investor", ""),
            },
            "fundamentals": fundamentals,
            "sources": headlines.get("sources", ""),
            "recommendations": report.get("recommendations", {}),
        }

    def _parse_trader_insight(self, insight_text: str) -> dict:
        """Parse a trader insight text block into structured data."""
        result = {
            "relevance": "Medium",
            "confidence": "MODERATE",
            "analysis": "",
            "action": "",
            "risks": [],
        }

        if not insight_text:
            return result

        # Extract relevance
        relevance_match = re.search(r"\*\*Relevance\*\*:\s*(\w+)", insight_text)
        if relevance_match:
            result["relevance"] = relevance_match.group(1)

        # Extract confidence
        confidence_match = re.search(r"\*\*Confidence\*\*:\s*(\w+)", insight_text)
        if confidence_match:
            result["confidence"] = confidence_match.group(1)

        # Extract main analysis (text before **Action**)
        action_idx = insight_text.find("**Action**")
        if action_idx > 0:
            analysis_text = insight_text[:action_idx]
            # Clean up markdown
            analysis_text = re.sub(r"\*\*Relevance\*\*:.*?\n", "", analysis_text)
            analysis_text = re.sub(r"\*\*Confidence\*\*:.*?\n", "", analysis_text)
            result["analysis"] = analysis_text.strip()

        # Extract action section
        risk_idx = insight_text.find("**Risks**")
        if action_idx >= 0 and risk_idx > action_idx:
            action_text = insight_text[action_idx:risk_idx]
            action_text = action_text.replace("**Action**:", "").strip()
            result["action"] = action_text

        # Extract risks
        if risk_idx >= 0:
            risks_text = insight_text[risk_idx:]
            risks_text = risks_text.replace("**Risks**:", "").strip()
            # Parse bullet points
            risks = re.findall(r"[-•]\s*(.+?)(?=\n[-•]|\n\n|\*\*|$)", risks_text, re.DOTALL)
            result["risks"] = [r.strip() for r in risks if r.strip()]

        return result

    def _generate_html_report(
        self,
        symbol: str,
        df: pd.DataFrame,
        charts: dict,
        agent_findings: dict,
        quote: dict,
    ) -> str:
        """
        Generate the complete HTML report.

        Args:
            symbol: Stock ticker symbol
            df: DataFrame with price data and indicators
            charts: Dictionary of chart images (base64 encoded)
            agent_findings: Extracted agent findings
            quote: Current quote data

        Returns:
            Complete HTML document as string
        """
        current_date = datetime.now().strftime("%B %d, %Y")
        current_price = df["close"].iloc[-1]
        prev_price = df["close"].iloc[-2] if len(df) > 1 else current_price
        price_change = ((current_price - prev_price) / prev_price) * 100

        # Calculate key metrics
        high_52w = df["high"].max() if len(df) >= 252 else df["high"].max()
        low_52w = df["low"].min() if len(df) >= 252 else df["low"].min()
        from_high = ((current_price - high_52w) / high_52w) * 100
        from_low = ((current_price - low_52w) / low_52w) * 100

        # Get technical indicators from latest row
        latest = df.iloc[-1]
        sma_50 = latest.get("sma_50", 0)
        sma_200 = latest.get("sma_200", 0)
        rsi = latest.get("rsi", 50)
        macd = latest.get("macd", 0)

        # Parse trader insights for structured display
        trader_data = {}
        for trader_type in ["day_trader", "swing_trader", "momentum_trader", "growth_investor", "value_investor"]:
            trader_data[trader_type] = self._parse_trader_insight(
                agent_findings["trader_insights"].get(trader_type, "")
            )

        # Build the HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{symbol} Strategic Analysis | KXAITrader Report</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        :root {{
            --navy: #003366;
            --charcoal: #404040;
            --teal: #00A3A1;
            --gold: #F2A900;
            --coral: #E06055;
            --light-grey: #F5F5F5;
            --medium-grey: #CCCCCC;
            --white: #FFFFFF;
            --green: #2ECC71;
            --font-heading: 'Helvetica Neue', 'Arial', sans-serif;
            --font-body: 'Georgia', 'Times New Roman', serif;
            --spacing-xs: 0.5rem;
            --spacing-sm: 1rem;
            --spacing-md: 1.5rem;
            --spacing-lg: 2rem;
            --spacing-xl: 3rem;
            --max-width: 950px;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ font-size: 16px; line-height: 1.6; }}
        body {{
            font-family: var(--font-body);
            color: var(--charcoal);
            background-color: var(--white);
            max-width: var(--max-width);
            margin: 0 auto;
            padding: var(--spacing-xl) var(--spacing-lg);
        }}

        h1 {{
            font-family: var(--font-heading);
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--navy);
            line-height: 1.2;
            margin-bottom: var(--spacing-sm);
        }}

        .subtitle {{
            font-family: var(--font-heading);
            font-size: 1.15rem;
            font-weight: 400;
            color: var(--teal);
            line-height: 1.4;
            margin-bottom: var(--spacing-lg);
        }}

        h2 {{
            font-family: var(--font-heading);
            font-size: 1.6rem;
            font-weight: 600;
            color: var(--navy);
            margin-top: var(--spacing-xl);
            margin-bottom: var(--spacing-md);
            padding-top: var(--spacing-md);
            border-top: 3px solid var(--navy);
        }}

        h3 {{
            font-family: var(--font-heading);
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--charcoal);
            margin-top: var(--spacing-lg);
            margin-bottom: var(--spacing-sm);
        }}

        p {{
            margin-bottom: var(--spacing-md);
            text-align: justify;
        }}

        .report-header {{
            margin-bottom: var(--spacing-xl);
            padding-bottom: var(--spacing-lg);
            border-bottom: 1px solid var(--medium-grey);
        }}

        .metadata {{
            font-family: var(--font-heading);
            font-size: 0.875rem;
            display: flex;
            gap: var(--spacing-md);
            flex-wrap: wrap;
            margin-top: var(--spacing-md);
        }}

        .metadata span {{
            padding: 0.25rem 0.75rem;
            background-color: var(--light-grey);
            border-radius: 4px;
        }}

        /* Agent Findings Highlights Section */
        .agent-highlights {{
            background: linear-gradient(135deg, var(--navy) 0%, #004d99 100%);
            color: var(--white);
            padding: var(--spacing-xl);
            margin: var(--spacing-lg) 0;
            border-radius: 8px;
        }}

        .agent-highlights h2 {{
            color: var(--white);
            border-top: none;
            margin-top: 0;
            padding-top: 0;
            font-size: 1.5rem;
        }}

        .agent-highlights .subtitle {{
            color: rgba(255, 255, 255, 0.9);
            font-size: 1rem;
        }}

        .findings-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: var(--spacing-md);
            margin-top: var(--spacing-lg);
        }}

        .finding-card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: var(--spacing-md);
            border-radius: 6px;
            border-left: 4px solid var(--teal);
        }}

        .finding-card h4 {{
            font-family: var(--font-heading);
            font-size: 0.9rem;
            color: var(--teal);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: var(--spacing-xs);
        }}

        .finding-card p {{
            color: var(--white);
            font-size: 0.95rem;
            margin-bottom: 0;
            text-align: left;
        }}

        /* Trader Insights Summary */
        .trader-summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: var(--spacing-sm);
            margin-top: var(--spacing-md);
        }}

        .trader-badge {{
            background: rgba(255, 255, 255, 0.15);
            padding: var(--spacing-sm);
            border-radius: 6px;
            text-align: center;
        }}

        .trader-badge .type {{
            font-family: var(--font-heading);
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.7);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .trader-badge .relevance {{
            font-family: var(--font-heading);
            font-size: 1rem;
            font-weight: 600;
            color: var(--white);
            margin-top: 4px;
        }}

        .trader-badge .confidence {{
            font-size: 0.75rem;
            color: var(--teal);
            margin-top: 2px;
        }}

        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: var(--spacing-sm);
            margin: var(--spacing-md) 0;
        }}

        .metric-box {{
            background: var(--light-grey);
            border: 1px solid var(--medium-grey);
            padding: var(--spacing-sm);
            text-align: center;
            border-radius: 4px;
        }}

        .metric-value {{
            font-family: var(--font-heading);
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--navy);
        }}

        .metric-value.positive {{ color: var(--green); }}
        .metric-value.negative {{ color: var(--coral); }}

        .metric-label {{
            font-family: var(--font-heading);
            font-size: 0.7rem;
            color: var(--charcoal);
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}

        /* Chart Container */
        .chart-container {{
            margin: var(--spacing-lg) 0;
            padding: var(--spacing-md);
            background: var(--light-grey);
            border-radius: 8px;
        }}

        .chart-container h3 {{
            color: var(--navy);
            margin-top: 0;
            margin-bottom: var(--spacing-md);
            font-size: 1.1rem;
        }}

        .chart-container img {{
            width: 100%;
            height: auto;
            display: block;
            border-radius: 4px;
        }}

        .chart-wrapper {{
            width: 100%;
            min-height: 400px;
            background: var(--white);
            border-radius: 4px;
        }}

        .chart-wrapper .plotly-graph-div {{
            width: 100% !important;
        }}

        .chart-caption {{
            font-family: var(--font-heading);
            font-size: 0.8rem;
            color: var(--charcoal);
            margin-top: var(--spacing-sm);
            font-style: italic;
        }}

        /* Trader Insight Cards */
        .insight-card {{
            background: var(--white);
            border: 1px solid var(--medium-grey);
            border-radius: 8px;
            margin: var(--spacing-lg) 0;
            overflow: hidden;
        }}

        .insight-header {{
            background: var(--light-grey);
            padding: var(--spacing-md);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--medium-grey);
        }}

        .insight-header h3 {{
            margin: 0;
            color: var(--navy);
            font-size: 1.15rem;
        }}

        .insight-badges {{
            display: flex;
            gap: var(--spacing-xs);
        }}

        .badge {{
            font-family: var(--font-heading);
            font-size: 0.7rem;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .badge-high {{ background: var(--green); color: var(--white); }}
        .badge-medium {{ background: var(--gold); color: var(--charcoal); }}
        .badge-low {{ background: var(--medium-grey); color: var(--charcoal); }}
        .badge-confidence {{ background: var(--teal); color: var(--white); }}

        .insight-body {{
            padding: var(--spacing-md);
        }}

        .insight-section {{
            margin-bottom: var(--spacing-md);
        }}

        .insight-section h4 {{
            font-family: var(--font-heading);
            font-size: 0.9rem;
            color: var(--teal);
            text-transform: uppercase;
            letter-spacing: 0.03em;
            margin-bottom: var(--spacing-xs);
        }}

        .action-box {{
            background: var(--light-grey);
            border-left: 4px solid var(--gold);
            padding: var(--spacing-md);
            margin: var(--spacing-sm) 0;
            font-family: var(--font-heading);
            font-size: 0.9rem;
        }}

        .risk-list {{
            list-style: none;
            padding: 0;
        }}

        .risk-list li {{
            padding: var(--spacing-xs) 0;
            padding-left: var(--spacing-md);
            position: relative;
            font-size: 0.9rem;
        }}

        .risk-list li::before {{
            content: "!";
            position: absolute;
            left: 0;
            color: var(--coral);
            font-weight: bold;
        }}

        /* Technical Indicators Table */
        .tech-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: var(--font-heading);
            font-size: 0.9rem;
            margin: var(--spacing-md) 0;
        }}

        .tech-table th, .tech-table td {{
            padding: var(--spacing-sm);
            text-align: left;
            border-bottom: 1px solid var(--medium-grey);
        }}

        .tech-table th {{
            background: var(--navy);
            color: var(--white);
            font-weight: 600;
        }}

        .tech-table tr:nth-child(even) {{
            background: var(--light-grey);
        }}

        /* Footer */
        .report-footer {{
            margin-top: var(--spacing-xl);
            padding-top: var(--spacing-lg);
            border-top: 2px solid var(--navy);
            font-family: var(--font-heading);
            font-size: 0.85rem;
        }}

        .sources h4 {{
            color: var(--navy);
            margin-bottom: var(--spacing-sm);
        }}

        .sources ul {{
            list-style: none;
            padding: 0;
        }}

        .sources li {{
            padding-left: var(--spacing-md);
            position: relative;
            margin-bottom: 0.25rem;
        }}

        .sources li::before {{
            content: "\\2192";
            position: absolute;
            left: 0;
            color: var(--teal);
        }}

        .disclaimer {{
            font-size: 0.8rem;
            color: var(--charcoal);
            font-style: italic;
            margin-top: var(--spacing-md);
            padding: var(--spacing-md);
            background: var(--light-grey);
            border-radius: 4px;
        }}

        @media screen and (max-width: 768px) {{
            html {{ font-size: 14px; }}
            .metrics-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .findings-grid {{ grid-template-columns: 1fr; }}
            .trader-summary {{ grid-template-columns: repeat(2, 1fr); }}
        }}

        @media print {{
            body {{ max-width: 100%; padding: 1in; }}
            .agent-highlights {{ background: var(--navy); -webkit-print-color-adjust: exact; }}
            .chart-container {{ page-break-inside: avoid; }}
            .insight-card {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <header class="report-header">
        <h1>{agent_findings.get('headline', f'{symbol} Strategic Analysis')}</h1>
        <p class="subtitle">{agent_findings.get('executive_summary', '')[:200]}...</p>
        <div class="metadata">
            <span>Report Date: {current_date}</span>
            <span>Asset: {symbol}</span>
            <span>Risk Assessment: {agent_findings.get('risk_assessment', 'Moderate').title()}</span>
            <span>Confidence: {agent_findings.get('confidence_score', 0.8) * 100:.0f}%</span>
        </div>
    </header>

    <!-- Agent Findings Highlights -->
    <section class="agent-highlights">
        <h2>AI Agent Key Findings</h2>
        <p class="subtitle">Critical insights extracted from multi-agent analysis</p>

        <div class="findings-grid">
            <div class="finding-card">
                <h4>Current Price</h4>
                <p><strong>${current_price:.2f}</strong> ({price_change:+.2f}% from previous close)</p>
            </div>
            <div class="finding-card">
                <h4>From Period High</h4>
                <p><strong>{from_high:+.1f}%</strong> from ${high_52w:.2f}</p>
            </div>
            <div class="finding-card">
                <h4>From Period Low</h4>
                <p><strong>{from_low:+.1f}%</strong> from ${low_52w:.2f}</p>
            </div>
            <div class="finding-card">
                <h4>Technical Posture</h4>
                <p><strong>{'Bullish' if current_price > sma_50 and current_price > sma_200 else 'Bearish' if current_price < sma_50 and current_price < sma_200 else 'Mixed'}</strong> - {'Above' if current_price > sma_50 else 'Below'} 50 & {'Above' if current_price > sma_200 else 'Below'} 200 SMA</p>
            </div>
            <div class="finding-card">
                <h4>RSI Reading</h4>
                <p><strong>{rsi:.1f}</strong> - {'Overbought' if rsi > 70 else 'Oversold' if rsi < 30 else 'Neutral'}</p>
            </div>
            <div class="finding-card">
                <h4>MACD Signal</h4>
                <p><strong>{macd:.2f}</strong> - {'Bullish' if macd > 0 else 'Bearish'} momentum</p>
            </div>
        </div>

        <h3 style="color: white; margin-top: 2rem; margin-bottom: 1rem;">Trader Relevance Summary</h3>
        <div class="trader-summary">
            <div class="trader-badge">
                <div class="type">Day Trader</div>
                <div class="relevance">{trader_data['day_trader']['relevance']}</div>
                <div class="confidence">{trader_data['day_trader']['confidence']}</div>
            </div>
            <div class="trader-badge">
                <div class="type">Swing Trader</div>
                <div class="relevance">{trader_data['swing_trader']['relevance']}</div>
                <div class="confidence">{trader_data['swing_trader']['confidence']}</div>
            </div>
            <div class="trader-badge">
                <div class="type">Momentum</div>
                <div class="relevance">{trader_data['momentum_trader']['relevance']}</div>
                <div class="confidence">{trader_data['momentum_trader']['confidence']}</div>
            </div>
            <div class="trader-badge">
                <div class="type">Growth</div>
                <div class="relevance">{trader_data['growth_investor']['relevance']}</div>
                <div class="confidence">{trader_data['growth_investor']['confidence']}</div>
            </div>
            <div class="trader-badge">
                <div class="type">Value</div>
                <div class="relevance">{trader_data['value_investor']['relevance']}</div>
                <div class="confidence">{trader_data['value_investor']['confidence']}</div>
            </div>
        </div>
    </section>

    <!-- Key Metrics -->
    <section>
        <h2>Market Snapshot</h2>
        <div class="metrics-grid">
            <div class="metric-box">
                <div class="metric-value">${current_price:.2f}</div>
                <div class="metric-label">Current Price</div>
            </div>
            <div class="metric-box">
                <div class="metric-value {'positive' if price_change >= 0 else 'negative'}">{price_change:+.2f}%</div>
                <div class="metric-label">Daily Change</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">${sma_50:.2f}</div>
                <div class="metric-label">50-Day SMA</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">${sma_200:.2f}</div>
                <div class="metric-label">200-Day SMA</div>
            </div>
        </div>

        <table class="tech-table">
            <thead>
                <tr>
                    <th>Indicator</th>
                    <th>Value</th>
                    <th>Signal</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>RSI (14)</td>
                    <td>{rsi:.2f}</td>
                    <td>{'Overbought - Consider selling' if rsi > 70 else 'Oversold - Consider buying' if rsi < 30 else 'Neutral'}</td>
                </tr>
                <tr>
                    <td>MACD</td>
                    <td>{macd:.4f}</td>
                    <td>{'Bullish momentum' if macd > 0 else 'Bearish momentum'}</td>
                </tr>
                <tr>
                    <td>Price vs 50 SMA</td>
                    <td>{((current_price - sma_50) / sma_50 * 100):+.2f}%</td>
                    <td>{'Above - Bullish' if current_price > sma_50 else 'Below - Bearish'}</td>
                </tr>
                <tr>
                    <td>Price vs 200 SMA</td>
                    <td>{((current_price - sma_200) / sma_200 * 100):+.2f}%</td>
                    <td>{'Above - Long-term bullish' if current_price > sma_200 else 'Below - Long-term bearish'}</td>
                </tr>
                <tr>
                    <td>ATR (14)</td>
                    <td>${latest.get('atr', 0):.2f}</td>
                    <td>Daily volatility range</td>
                </tr>
            </tbody>
        </table>
    </section>

    <!-- Charts Section -->
    <section>
        <h2>Technical Analysis Charts</h2>
        <p style="font-size: 0.9rem; color: var(--charcoal); margin-bottom: 1rem;"><em>Interactive charts - hover over data points for details, use toolbar to zoom and pan</em></p>
"""

        # Add charts - handle both interactive HTML and static images
        def embed_chart(chart_content: str, is_interactive: bool = True) -> str:
            """Helper to embed chart content properly."""
            if is_interactive and chart_content.startswith("<div"):
                # Interactive Plotly chart - embed directly
                return chart_content
            elif chart_content.startswith("data:image"):
                # Static base64 image
                return f'<img src="{chart_content}" alt="Chart" style="width:100%; height:auto;">'
            else:
                # Assume it's interactive HTML
                return chart_content

        # Check if charts are interactive (contain div tags)
        charts_are_interactive = any(
            c.startswith("<div") for c in charts.values() if isinstance(c, str)
        ) if charts else False

        if "price_volume" in charts:
            html += f"""
        <div class="chart-container">
            <h3>Price & Volume Analysis</h3>
            <div class="chart-wrapper">{embed_chart(charts['price_volume'])}</div>
            <p class="chart-caption">Daily closing price with 50-day and 200-day moving averages. Volume bars show buying (green) vs selling (red) pressure.</p>
        </div>
"""

        if "candlestick" in charts:
            html += f"""
        <div class="chart-container">
            <h3>Candlestick with Bollinger Bands</h3>
            <div class="chart-wrapper">{embed_chart(charts['candlestick'])}</div>
            <p class="chart-caption">OHLC candlestick pattern with Bollinger Bands (20-period, 2 std dev). Price near upper band suggests overbought, near lower suggests oversold.</p>
        </div>
"""

        if "technical" in charts:
            html += f"""
        <div class="chart-container">
            <h3>Technical Indicators Dashboard</h3>
            <div class="chart-wrapper">{embed_chart(charts['technical'])}</div>
            <p class="chart-caption">Multi-panel view: Price trend, RSI (14) with overbought/oversold zones, and MACD histogram for momentum analysis.</p>
        </div>
"""

        if "performance" in charts:
            html += f"""
        <div class="chart-container">
            <h3>Period Performance</h3>
            <div class="chart-wrapper">{embed_chart(charts['performance'])}</div>
            <p class="chart-caption">Returns over different holding periods. Green indicates positive returns, red indicates losses.</p>
        </div>
"""

        html += """
    </section>

    <!-- Detailed Trader Insights -->
    <section>
        <h2>Detailed Trader Analysis</h2>
"""

        # Add trader insight cards
        trader_names = {
            "day_trader": "Day Trader",
            "swing_trader": "Swing Trader",
            "momentum_trader": "Momentum Trader",
            "growth_investor": "Growth Investor",
            "value_investor": "Value Investor",
        }

        for trader_key, trader_name in trader_names.items():
            data = trader_data[trader_key]
            relevance_class = "high" if data["relevance"].lower() == "high" else "medium" if data["relevance"].lower() == "medium" else "low"

            html += f"""
        <div class="insight-card">
            <div class="insight-header">
                <h3>{trader_name}</h3>
                <div class="insight-badges">
                    <span class="badge badge-{relevance_class}">Relevance: {data['relevance']}</span>
                    <span class="badge badge-confidence">{data['confidence']}</span>
                </div>
            </div>
            <div class="insight-body">
                <div class="insight-section">
                    <h4>Analysis</h4>
                    <p>{data['analysis'][:500]}{'...' if len(data['analysis']) > 500 else ''}</p>
                </div>
"""
            if data["action"]:
                html += f"""
                <div class="insight-section">
                    <h4>Recommended Action</h4>
                    <div class="action-box">{data['action'][:400]}{'...' if len(data['action']) > 400 else ''}</div>
                </div>
"""
            if data["risks"]:
                html += """
                <div class="insight-section">
                    <h4>Key Risks</h4>
                    <ul class="risk-list">
"""
                for risk in data["risks"][:5]:
                    html += f"                        <li>{risk}</li>\n"
                html += """                    </ul>
                </div>
"""
            html += """            </div>
        </div>
"""

        # Footer
        html += f"""
    </section>

    <footer class="report-footer">
        <div class="sources">
            <h4>Data Sources</h4>
            <ul>
                <li>Daily price and volume data via Alpha Vantage API</li>
                <li>Technical indicators calculated from OHLCV data (50/200-day SMA, RSI-14, MACD 12-26-9, Bollinger Bands 20-2, ATR-14)</li>
                <li>AI Agent analysis for trader-specific insights</li>
            </ul>
        </div>

        <div class="disclaimer">
            <strong>Disclaimer:</strong> This analysis is for informational purposes only and does not constitute investment advice.
            Past performance does not guarantee future results. The views expressed represent analysis as of the report date
            and are subject to change. Investors should conduct their own due diligence and consult with qualified financial
            advisors before making investment decisions.
        </div>

        <div style="display: flex; justify-content: space-between; margin-top: 1rem; font-size: 0.75rem; color: var(--charcoal);">
            <span>Generated: {current_date}</span>
            <span>Symbol: {symbol}</span>
            <span>KXAITrader Report v1.0</span>
        </div>
    </footer>
</body>
</html>
"""

        return html

    def generate_report(
        self,
        symbol: str,
        json_analysis: Optional[dict] = None,
        include_charts: bool = True,
        include_news: bool = True,
        include_intraday: bool = False,
        output_format: str = "html",
        date_range: Optional[tuple] = None,
        use_sample_data: bool = False,
    ) -> dict:
        """
        Generate a comprehensive trading analysis report.

        Args:
            symbol: Stock ticker symbol
            json_analysis: Optional JSON analysis from trading agents
            include_charts: Whether to generate charts
            include_news: Whether to include news data
            include_intraday: Whether to include intraday data
            output_format: Output format ('html' or 'markdown')
            date_range: Optional (start_date, end_date) tuple
            use_sample_data: Use sample data instead of API (for testing)

        Returns:
            Dictionary with output path and generated charts
        """
        print(f"Fetching market data for {symbol}...")

        # Fetch daily data
        start_date = date_range[0] if date_range else None
        end_date = date_range[1] if date_range else None

        if use_sample_data:
            print("Using sample data for demonstration...")
            df = generate_sample_data(symbol, days=365)
        else:
            try:
                df = self.api_client.get_daily_data(
                    symbol,
                    outputsize="full",
                    start_date=start_date,
                    end_date=end_date,
                )
            except Exception as e:
                print(f"API call failed: {e}")
                print("Falling back to sample data...")
                df = generate_sample_data(symbol, days=365)

        print(f"Retrieved {len(df)} days of price data")

        # Calculate technical indicators
        df = self.api_client.calculate_technical_indicators(df)

        # Get current quote
        if use_sample_data:
            quote = get_sample_quote(symbol, df)
        else:
            try:
                quote = self.api_client.get_quote(symbol)
            except Exception:
                quote = get_sample_quote(symbol, df)

        # Extract agent findings if provided
        if json_analysis:
            agent_findings = self._extract_agent_findings(json_analysis)
        else:
            agent_findings = {
                "headline": f"{symbol} Technical Analysis Report",
                "key_findings": [],
                "risk_assessment": "moderate",
                "confidence_score": 0.8,
                "executive_summary": f"Comprehensive technical analysis for {symbol}",
                "trader_insights": {},
            }

        # Generate charts
        charts = {}
        if include_charts:
            print("Generating charts...")

            try:
                charts["price_volume"] = self.chart_generator.generate_price_chart(
                    df.tail(90), symbol
                )
                print("  - Price & Volume chart generated")
            except Exception as e:
                print(f"  - Warning: Could not generate price chart: {e}")

            try:
                charts["candlestick"] = self.chart_generator.generate_candlestick_chart(
                    df.tail(60), symbol
                )
                print("  - Candlestick chart generated")
            except Exception as e:
                print(f"  - Warning: Could not generate candlestick chart: {e}")

            try:
                charts["technical"] = self.chart_generator.generate_technical_indicators_chart(
                    df.tail(90), symbol
                )
                print("  - Technical indicators chart generated")
            except Exception as e:
                print(f"  - Warning: Could not generate technical chart: {e}")

            try:
                charts["performance"] = self.chart_generator.generate_performance_summary_chart(
                    df, symbol
                )
                print("  - Performance chart generated")
            except Exception as e:
                print(f"  - Warning: Could not generate performance chart: {e}")

        # Generate HTML report
        print("Generating HTML report...")
        html_content = self._generate_html_report(
            symbol, df, charts, agent_findings, quote
        )

        # Save report
        output_filename = f"{symbol.lower()}_report.html"
        output_path = self.config.output_dir / output_filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"Report saved to: {output_path}")

        return {
            "output_path": str(output_path),
            "charts": {k: f"{k}_chart.png" for k in charts.keys()},
            "data_points": len(df),
            "symbol": symbol,
        }
