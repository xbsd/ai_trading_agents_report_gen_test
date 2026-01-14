# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KXAITrader-style report generation system that transforms financial trading analysis JSON into executive-grade reports. Outputs both Markdown and HTML with professional aesthetics suitable for C-suite presentations.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Generate HTML report from JSON analysis
python generate_report.py ORCL --api-key YOUR_KEY --json analysis.json --format html

# Generate markdown report without charts
python generate_report.py AAPL --api-key YOUR_KEY --format markdown --no-charts

# Custom date range
python generate_report.py GOOGL --api-key YOUR_KEY --start 2024-01-01 --end 2024-06-30

# Using environment variable for API key
export ALPHA_VANTAGE_API_KEY=YOUR_KEY
python generate_report.py ORCL --json analysis.json
```

Get a free API key at: https://www.alphavantage.co/support/#api-key

## Architecture

### Two Usage Modes

1. **Python Script Mode** (`generate_report.py`): Automated pipeline using `src/kxaitrader/` modules to fetch Alpha Vantage market data, calculate technical indicators, generate Plotly charts, and produce HTML/Markdown reports.

2. **Prompt-Based Mode**: Use the prompts and agents defined in markdown files to manually generate reports from JSON data through Claude conversations.

### Key Files

| File | Purpose |
|------|---------|
| `generate_report.py` | CLI entry point for automated report generation |
| `kxaitrader_styles.css` | Complete CSS stylesheet for HTML reports |
| `kxaitrader_html_prompt.md` | Prompt template for generating HTML reports |
| `agents.md` | Five specialized agents (Report Writer, Technical Translator, Executive Synthesizer, Exhibit Designer, Quality Reviewer) |
| `skills.md` | Detailed techniques for technical translation and data contextualization |

### JSON Input Structure

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

Structure is flexible—adapt gracefully to missing or additional fields.

## Report Generation Guidelines

### Content Philosophy

**Always:**
- Lead with insights, not topics (section titles communicate findings)
- Use specific data: exact percentages, dates, dollar values
- Translate technical concepts into business implications
- Answer "so what?" in every major section

**Never:**
- Use generic section titles ("Introduction", "Conclusion", "Analysis")
- Include bullet points in body paragraphs (reserve for exec summary)
- Present raw data without strategic context
- Use hedging language ("maybe", "possibly", "might")

### Technical Translation

| Technical | Strategic Translation |
|-----------|----------------------|
| "RSI at 53.69" | "Momentum indicators suggest selling pressure has subsided without reaching overbought extremes" |
| "Stock testing upper Bollinger Band" | "Price approaching technical resistance zone, signaling potential inflection point" |
| "MACD negative but improving" | "Rate of decline slowing, suggesting momentum shift may be emerging" |
| "High volume on up days" | "Institutional accumulation pattern evident in elevated buying pressure" |

### Trader Types → Strategic Frameworks

| JSON Key | Report Framework |
|----------|------------------|
| `day_trader` | Short-Term Tactical Opportunity |
| `swing_trader` | Medium-Term Position Trade |
| `momentum_trader` | Trend-Following Strategy |
| `growth_investor` | Long-Term Growth Thesis |
| `value_investor` | Intrinsic Value Assessment |

### Color Palette (HTML)

```css
--navy: #003366        /* Authority, primary headings */
--charcoal: #404040    /* Professional body text */
--teal: #00A3A1        /* Innovation, analytical callouts */
--gold: #F2A900        /* Caution, financial metrics */
--coral: #E06055       /* Risk, urgent action items */
--light-grey: #F5F5F5  /* Background panels */
```

## Report Structure

1. **Executive Summary** (300-400 words): Strategic title, 3-5 key insights, at-a-glance metrics
2. **The Situation** (500-800 words): Market context, key events, critical inflection signals
3. **Core Analysis** (1,000-1,500 words): Multi-perspective assessment, comparative frameworks, 2-3 exhibits
4. **Implications & Risk** (400-600 words): Scenario planning (bull/base/bear), risk factors
5. **Recommended Actions** (300-400 words): Decision-tree by investor profile, timeframes, invalidation levels
6. **Methodology & Sources**: Data attribution, report metadata

## Quality Checklist

- [ ] Executive summary stands alone as complete brief
- [ ] All section titles are insight-driven (not generic)
- [ ] All numbers precise and contextualized
- [ ] Technical concepts translated for business audience
- [ ] 3-5 exhibits described with clear purpose
- [ ] Recommendations actionable and time-bound
- [ ] Sources properly cited

## Agent Selection

| Task | Agent |
|------|-------|
| New report from JSON | KXAITrader Report Writer |
| Heavy technical data | Technical Translator |
| Quick executive briefing | Executive Synthesizer |
| Adding visualizations | Exhibit Designer |
| Final polish | Quality Reviewer |

See `agents.md` for detailed definitions and `skills.md` for specific techniques.
