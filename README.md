# AI Trading Agents Report Generator

A sophisticated report generation system that transforms financial trading analysis JSON into executive-grade reports. Built in the KXAITrader style, it produces professional Markdown and HTML reports with clean aesthetics suitable for C-suite presentations.

## Features

- **Dual Output Formats**: Generate reports in both Markdown and HTML
- **Professional Styling**: Executive-ready design with carefully chosen color palette
- **Technical Translation**: Converts technical indicators into business-relevant insights
- **Multi-Perspective Analysis**: Covers day trading, swing trading, momentum trading, and long-term investing strategies
- **Automated Pipeline**: Fetches real-time market data from Alpha Vantage
- **Interactive Charts**: Plotly-based visualizations for data-driven insights
- **AI-Powered Synthesis**: Leverages Claude for intelligent report generation

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai_trading_agents_report_gen_test.git
cd ai_trading_agents_report_gen_test

# Install dependencies
pip install -r requirements.txt
```

### Get an API Key

Sign up for a free Alpha Vantage API key at: https://www.alphavantage.co/support/#api-key

### Basic Usage

```bash
# Set your API key as an environment variable
export ALPHA_VANTAGE_API_KEY=YOUR_KEY

# Generate HTML report from JSON analysis
python generate_report.py ORCL --json analysis.json --format html

# Generate markdown report
python generate_report.py AAPL --format markdown

# Custom date range
python generate_report.py GOOGL --start 2024-01-01 --end 2024-06-30

# Without charts
python generate_report.py MSFT --no-charts
```

## Project Structure

```
.
├── generate_report.py           # CLI entry point
├── requirements.txt             # Python dependencies
├── kxaitrader_styles.css       # Complete CSS stylesheet for HTML reports
├── kxaitrader_html_prompt.md   # Prompt template for HTML generation
├── agents.md                    # Five specialized AI agents
├── skills.md                    # Technical translation techniques
├── CLAUDE.md                    # Project instructions for Claude Code
└── output/                      # Generated reports directory
```

## Usage Modes

### 1. Python Script Mode (Automated)

Use `generate_report.py` for fully automated report generation:
- Fetches Alpha Vantage market data
- Calculates technical indicators
- Generates Plotly charts
- Produces HTML/Markdown reports

### 2. Prompt-Based Mode (Manual)

Use the markdown prompt files and agents for manual report generation through Claude conversations:
- `kxaitrader_html_prompt.md` - Report generation template
- `agents.md` - Five specialized agents (Report Writer, Technical Translator, etc.)
- `skills.md` - Detailed techniques for data contextualization

## Report Structure

Every generated report includes:

1. **Executive Summary** (300-400 words) - Strategic overview with key insights
2. **The Situation** (500-800 words) - Market context and critical signals
3. **Core Analysis** (1,000-1,500 words) - Multi-perspective assessment with exhibits
4. **Implications & Risk** (400-600 words) - Scenario planning and risk factors
5. **Recommended Actions** (300-400 words) - Decision framework by investor profile
6. **Methodology & Sources** - Data attribution and metadata

## Design Philosophy

**Lead with insights, not topics**: Section titles communicate findings, not generic labels.

**Specific data**: Exact percentages, dates, and dollar values.

**Business context**: Technical concepts translated into strategic implications.

**Answer "so what?"**: Every section explains significance and actionability.

## Color Palette

The HTML reports use a professional color scheme:

- **Navy** (#003366) - Authority, primary headings
- **Charcoal** (#404040) - Professional body text
- **Teal** (#00A3A1) - Innovation, analytical callouts
- **Gold** (#F2A900) - Caution, financial metrics
- **Coral** (#E06055) - Risk, urgent action items
- **Light Grey** (#F5F5F5) - Background panels

## JSON Input Structure

The system accepts flexible JSON input:

```json
{
  "event_id": "...",
  "report": {
    "summary": {
      "headline": "...",
      "key_findings": [...],
      "analysis": {
        "day_trader": "...",
        "swing_trader": "...",
        "momentum_trader": "...",
        "growth_investor": "...",
        "value_investor": "..."
      }
    }
  }
}
```

The structure adapts gracefully to missing or additional fields.

## Technical Translation Examples

| Technical Indicator | Strategic Translation |
|---------------------|----------------------|
| "RSI at 53.69" | "Momentum indicators suggest selling pressure has subsided without reaching overbought extremes" |
| "Stock testing upper Bollinger Band" | "Price approaching technical resistance zone, signaling potential inflection point" |
| "MACD negative but improving" | "Rate of decline slowing, suggesting momentum shift may be emerging" |
| "High volume on up days" | "Institutional accumulation pattern evident in elevated buying pressure" |

## Contributing

This project is designed to work seamlessly with [Claude Code](https://claude.ai/code). See `CLAUDE.md` for detailed development guidelines.

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please open an issue on the GitHub repository.

---

**Note**: This system is for informational and educational purposes only. Not financial advice. Always consult with qualified financial professionals before making investment decisions.
