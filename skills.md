# KXAITrader Report Generation Skills

This file defines specific skills, capabilities, and techniques for generating KXAITrader-quality reports. These skills are modular and can be applied across different agents and contexts.

---

## Skill 1: Strategic Title Crafting

**Purpose:** Create insight-driven section titles that communicate findings, not just topics

**Technique:**
Instead of asking "what is this section about?", ask "what does this section prove/reveal/suggest?"

**Formula:**
`[Data observation/pattern] + [Implication] + [Action context]`

**Examples:**

| ❌ Generic | ✅ Strategic |
|-----------|-------------|
| "Market Analysis" | "Technical oversold conditions signal potential inflection point" |
| "Risk Assessment" | "Three risk scenarios define the recovery trajectory" |
| "Competitive Landscape" | "Oracle's cloud positioning lags AWS and Azure in AI workloads" |
| "Investment Thesis" | "42% correction creates asymmetric opportunity for value investors" |
| "Price Action Review" | "Institutional accumulation pattern emerges on elevated volume" |

**Practice drill:**
Take any generic title and apply: "This section proves that..." → use that as your title

**Quality test:**
- Can someone understand the key finding from the title alone?
- Does it create curiosity about the supporting evidence?
- Would KXAITrader use this title?

---

## Skill 2: Technical Translation

**Purpose:** Convert quantitative/technical data into strategic business language

**Translation matrix:**

### Financial Indicators → Business Implications

| Technical | Strategic Translation | Additional Context |
|-----------|----------------------|-------------------|
| RSI > 70 | Momentum reaching overbought extremes | May signal near-term exhaustion or continued strength in strong trends |
| RSI < 30 | Deeply oversold conditions | Suggests panic selling may have run its course |
| RSI 40-60 | Neutral momentum zone | Neither overbought nor oversold, directionally ambiguous |
| MACD crossing above signal | Emerging positive momentum | Early-stage buy signal as rate of change accelerates |
| MACD negative but improving | Decline rate slowing | Momentum still bearish but showing signs of stabilization |
| Upper Bollinger Band test | Approaching volatility extreme | Either strong momentum or near-term pause likely |
| Price below 50-day MA | Short-term downtrend intact | Technical weakness on 2-3 month timeframe |
| Price below 200-day MA | Long-term downtrend confirmed | Major trend remains bearish until reclaimed |
| Volume spike on up day | Institutional accumulation | Sophisticated capital deployment, not retail speculation |
| Volume spike on down day | Distribution or forced selling | Large holders reducing positions or stops triggered |
| ATR expanding | Volatility increasing | Larger daily price swings, adjust position sizing |
| Low ATR | Compressed volatility | Potential breakout/breakdown setup forming |

### Options Terminology → Strategic Language

| Technical | Strategic Translation |
|-----------|----------------------|
| Implied volatility elevated | Market pricing increased uncertainty and risk premium |
| Put/call ratio rising | Hedging demand or bearish sentiment increasing |
| Open interest surge | Significant positioning for directional move |
| Skew to downside | Market pricing tail risk, protection expensive |

### Chart Patterns → Strategic Narratives

| Pattern | Strategic Description |
|---------|---------------------|
| Higher highs, higher lows | Uptrend structure intact with improving momentum |
| Lower highs, lower lows | Downtrend structure reinforcing bearish sentiment |
| Consolidation after rally | Digesting gains before potential continuation |
| Gap up on volume | Immediate repricing as new information integrated |
| Failed breakout | Insufficient buying conviction, trend reversal risk |

**Application rules:**
1. Always provide both the technical data AND the business implication
2. Use analogies from broader business domains when helpful
3. Connect to decision-making: "What does this mean for positioning?"
4. Avoid hedging unless genuinely uncertain ("may", "could", "possibly")

**Example transformation:**

❌ **Before:**
"The RSI is at 53.69, having recovered from oversold levels. The MACD is -3.98, improving from -5.19. Volume was 26.2M vs. average of 16-19M."

✅ **After:**
"Momentum indicators suggest the panic selling has subsided—the stock has recovered from deeply oversold conditions without yet reaching overbought extremes, leaving room for continued upside. More critically, trading activity spiked 38% above normal on the recovery days, indicating institutional accumulation rather than retail speculation."

---

## Skill 3: Data Contextualization

**Purpose:** Transform raw numbers into meaningful, contextualized insights

**Contextualization framework:**

Every number should answer at least 2 of these questions:
1. **Compared to what?** (benchmark, historical average, peer group)
2. **How unusual?** (percentile, standard deviations, historical precedent)
3. **What's the rate of change?** (velocity, acceleration)
4. **What's the magnitude?** (absolute dollars, percentage impact, duration)
5. **What are the implications?** (risk/reward, decision threshold, signal)

**Examples:**

| ❌ Uncontextualized | ✅ Contextualized |
|---------------------|-------------------|
| "The stock fell to $185.66" | "The stock fell to $185.66—a 42% decline from the October peak of $321.69, erasing $68 billion in market value over eight weeks" |
| "Volume was high" | "Volume reached 26.2M shares, 38% above the 3-month average of 16-19M, suggesting institutional participation" |
| "RSI is 53.69" | "RSI has recovered to 53.69 from oversold levels below 30, indicating panic selling has subsided without yet reaching overbought extremes above 70" |
| "The stock is volatile" | "Daily volatility (ATR) stands at $7.99, representing 4% of the current price—twice the typical 2% level, demanding more conservative position sizing" |

**Date precision rules:**
- Always include day-of-week for recent events: "January 8th (Wednesday)"
- Include year for events >6 months ago: "October 16, 2024"
- Use relative timeframes when clearer: "in the past four trading sessions"

**Percentage precision:**
- Round to whole numbers for large moves: "42% decline" (not 42.3%)
- Use one decimal for smaller moves: "5.3% gain"
- Always clarify the baseline: "42% below October peak" (not just "down 42%")

**Dollar value precision:**
- Include cents for stock prices: "$185.66"
- Round large values: "$68 billion" (not $68,234,567,890)
- Provide context: "$68 billion (23% of market cap)"

---

## Skill 4: Narrative Flow Construction

**Purpose:** Create logical, compelling progression through complex analysis

**Narrative arc structure:**

```
1. SITUATION (Context)
   ↓
2. COMPLICATION (Problem/Question)
   ↓
3. ANALYSIS (Evidence/Investigation)
   ↓
4. IMPLICATION (What it means)
   ↓
5. RESOLUTION (Recommended action)
```

**Transition techniques:**

**Sequential logic:**
- "This leads to..."
- "Consequently..."
- "As a result..."
- "Building on this foundation..."

**Contrast:**
- "However, this view must be balanced against..."
- "This stands in sharp contrast to..."
- "Conversely..."
- "On the other hand..."

**Deepening:**
- "More fundamentally..."
- "Looking beneath the surface..."
- "The critical question becomes..."
- "To understand this dynamic..."

**Elevation:**
- "Stepping back..."
- "In the broader context..."
- "What does this mean for investors?"
- "The strategic implication is clear..."

**Evidence layering:**
- "First evidence point"
- "Supporting this view..."
- "More critically..."
- "Most tellingly..."

**Paragraph structure template:**

```
[Topic sentence - the claim]
[Evidence point 1 - specific data]
[Evidence point 2 - supporting data]
[Connection/implication - so what?]
[Bridge to next paragraph]
```

**Example:**

"The near-term technical setup favors aggressive traders willing to accept elevated volatility. The stock has completed a textbook capitulation pattern: sharp decline on rising volume, followed by reversal on elevated buying pressure. Volume patterns are particularly instructive—the January 9th and 12th sessions both showed 26.2M and 25.3M shares respectively, well above the typical 16-19M range. This suggests institutional accumulation rather than retail speculation. However, this optimism must be tempered by the stock's position below both major moving averages, which indicates the broader downtrend remains intact."

---

## Skill 5: Synthesis Across Perspectives

**Purpose:** Integrate multiple viewpoints into coherent strategic frameworks

**Synthesis techniques:**

### Technique 1: Comparative Matrix
Create 2x2 or 2x3 frameworks comparing perspectives:

**Example: Time Horizon × Risk Tolerance**
```
           Short-term (1-2 weeks)    Long-term (6-12 months)
High Risk  Swing trade: High         Growth investor: Medium
           reward, tight stops        reward, requires research

Low Risk   Day trade: Medium         Value investor: Uncertain
           reward, intraday only      reward, fundamentals unclear
```

### Technique 2: Consensus vs. Divergence
Identify where all perspectives agree vs. where they differ:

**Consensus points:**
- All strategies acknowledge 42% decline creates opportunity
- All note elevated volume on recovery days
- All recognize $210-$215 resistance zone as critical

**Divergence points:**
- Time horizon: Days vs. weeks vs. years
- Entry trigger: Immediate vs. confirmation required
- Risk tolerance: Tight stops vs. buy-and-hold

### Technique 3: Scenario Building
Transform individual perspectives into unified scenarios:

**Bull scenario:** All conditions met
- Breaks above $215 with volume
- Fundamental catalyst clarifies positive outlook
- Momentum traders enter → virtuous cycle
- Timeline: 2-4 weeks

**Base scenario:** Mixed conditions
- Consolidates $200-$215 for several weeks
- No clear fundamental driver emerges
- Selective short-term trades viable
- Timeline: 4-8 weeks

**Bear scenario:** Adverse conditions
- Breaks below $195, retest of $185 lows
- Fundamental news confirms deterioration
- All strategies invalidated
- Timeline: 1-2 weeks

**Example synthesis paragraph:**

"The Oracle opportunity presents distinct value propositions across different investment horizons. Short-term traders see a compelling mean-reversion setup with clear entry/exit levels, while long-term investors face decision-forcing uncertainty until fundamental drivers clarify. What unites all perspectives is recognition that the $210-$215 zone represents a critical decision threshold—successful reclamation would signal trend reversal, while rejection would confirm continued weakness. This creates a natural decision tree: tactical positioning ahead of the test, with scaling plans based on the outcome."

---

## Skill 6: Exhibit Description Writing

**Purpose:** Specify data visualizations that advance arguments and insights

**Exhibit description template:**

```markdown
**Exhibit [N]: [Insight-driven title]**

*Chart type:* [Line, bar, waterfall, heat map, etc.]
*Dimensions:* [Width × Height in pixels or print dimensions]

*Data series:*
- Series 1: [Description, color: #HEX, line weight]
- Series 2: [Description, color: #HEX, line weight]

*Axis specifications:*
- X-axis: [Label, range, tick intervals]
- Y-axis: [Label, range, tick intervals, format]

*Key annotations:*
- Point 1: [Date/Value, callout text]
- Point 2: [Date/Value, callout text]
- Shaded region: [Range, meaning, color]

*Design notes:*
- Remove gridlines, use subtle axis rules only
- Direct label data series (no legend unless >3 series)
- Font: [Sans-serif for labels, size specifications]

*Color usage:*
- [Specific colors from KXAITrader palette with purpose]

*Insight:* [1-2 sentences explaining what the exhibit proves]

*Source:* [Data attribution]
```

**Exhibit title formulas:**

**Pattern 1: Observation + Implication**
- "Stock declined 42% from October peak, creating potential value entry point"

**Pattern 2: Comparison + Conclusion**
- "Volume surge on recovery days exceeds distribution phase, signaling accumulation"

**Pattern 3: Trend + Consequence**
- "Momentum indicators improving from oversold extremes, leaving room for continuation"

**Pattern 4: Question + Answer**
- "Is this a bear market bounce or genuine reversal? Technical signals point to the latter"

**Chart type selection guide:**

| Data/Message Type | Recommended Chart | KXAITrader Example |
|-------------------|-------------------|------------------|
| Time series trend | Line chart | Price over time, single line |
| Multiple trends comparison | Multi-line chart | Price vs. moving averages |
| Change attribution | Waterfall chart | P&L breakdown, price change factors |
| Part-to-whole | Stacked bar, tree map | Portfolio allocation |
| Correlation | Scatter plot | Risk vs. return |
| Distribution | Histogram, box plot | Return distribution |
| Ranking | Horizontal bar | Top 10 holdings |
| Matrix comparison | Heat map | Risk/return across strategies |
| Small multiples | Grid of mini-charts | Performance across timeframes |
| Single metric spotlight | Bullet chart | Target vs. actual |

---

## Skill 7: Risk Articulation

**Purpose:** Present risks in structured, decision-relevant format

**Risk framework:**

Every risk should include:
1. **Description:** What could go wrong?
2. **Probability:** How likely? (High/Medium/Low or %)
3. **Impact:** How severe? (Quantified if possible)
4. **Leading indicators:** How would we know it's happening?
5. **Mitigation:** What can be done? (if applicable)

**Risk categories for financial reports:**

**Market structure risks:**
- Liquidity drying up
- False breakout/breakdown
- Volatility expansion beyond assumptions

**Fundamental risks:**
- Earnings disappointment
- Business model disruption
- Management changes

**Macro risks:**
- Economic slowdown
- Interest rate changes
- Geopolitical events

**Execution risks:**
- Position sizing errors
- Stop-loss discipline failure
- Opportunity cost

**Technical risks:**
- Trend confirmation failure
- Support/resistance violation
- Pattern invalidation

**Example risk section:**

"Three categories of risk warrant consideration. **Market structure risks** center on the sustainability of the current bounce—specifically, whether institutional buyers will continue to support prices above $200. Leading indicators include volume patterns and bid-ask spread behavior. **Fundamental risks** remain opaque given limited disclosure around the earnings miss catalyst; any additional negative news would likely trigger retests of the $185 low. **Execution risks** for traders include the elevated volatility environment (ATR $7.99, or 4% of price) which demands position sizing discipline—using half normal size provides equivalent dollar risk while accommodating wider stops."

---

## Skill 8: Action Item Specification

**Purpose:** Create clear, actionable recommendations with decision trees

**Action specification template:**

```markdown
**For [Investor Type] ([Timeframe]):**

*Entry strategy:*
- Trigger: [Specific condition]
- Price: [Exact level or range]
- Size: [% of normal position]

*Exit strategy:*
- Target 1: [Price, % gain, condition]
- Target 2: [Price, % gain, condition]
- Stop: [Price, % loss, invalidation condition]

*Risk/Reward:* [Ratio, e.g., 1:3]

*Position management:*
- [Scaling plan if applicable]
- [Adjustment rules based on behavior]

*Timeframe:* [Expected holding period]

*Invalidation:* [Condition that breaks thesis]

*Success metrics:* [How to measure if working]
```

**Decision tree format:**

```
IF [condition A]:
  → Action 1 [specific steps]
  → Monitor [specific metrics]
  
  IF [sub-condition]:
    → Adjust to Action 2
  ELSE:
    → Continue with Action 1

ELSE IF [condition B]:
  → Action 3 [specific steps]
  → Different monitoring approach

ELSE:
  → Wait for clarity
  → Revisit in [timeframe]
```

**Example action item section:**

"The optimal strategy depends critically on investor timeframe and fundamental conviction:

**For tactical traders (1-2 week horizon):**
- **Entry:** 50% position at $200-$202 on any pullback, or current levels if risk tolerance permits
- **Add:** 25% on break above $206.60 (recent high)
- **Target 1:** $210.43 (50-day MA) for +5-6%
- **Target 2:** $215.78 (200-day MA) for +8-10%
- **Stop:** Below $194 (invalidates bounce thesis)
- **Risk/Reward:** 1:3
- **Invalidation:** Close below $195 signals failed reversal
- **Timeframe:** 5-10 trading days

**For long-term investors:**
First, research the fundamental cause of the 42% decline through earnings reports and analyst commentary. **IF fundamental thesis remains intact:**
- Build position in tranches: 25% now, 25% at $190-$195 if pullback, 25% on break above $215, final 25% at $230
- Target: $300-$350 over 12-24 months
- Monitor: Quarterly earnings, cloud growth metrics, competitive positioning
- **IF fundamental thesis impaired:** Avoid until growth trajectory stabilizes, deploy capital elsewhere"

---

## Skill 9: Source Attribution

**Purpose:** Provide clean, professional citation of data sources

**Attribution principles:**
- Cite at the point of claim, not in giant bibliography
- Use inline citations for specific facts
- Use footer for general data sources
- Distinguish between primary and secondary sources
- Note data limitations when relevant

**Inline citation formats:**

**For specific facts:**
"According to Oracle's Q2 FY2026 earnings report, cloud revenue grew 24% year-over-year..."

**For market data:**
"As of January 12th close (source: daily price data via Alpha Vantage)..."

**For analysis:**
"Seeking Alpha analysts note that the post-earnings selloff appears disconnected from actual results..."

**Footer format:**

```markdown
---

**Data Sources:**
- Daily price data: Alpha Vantage, 3-month history through January 12, 2026
- Technical indicators: Calculated from daily OHLCV data
- Earnings information: Oracle Corporation investor relations, Q2 FY2026 report
- Analyst commentary: Seeking Alpha, CNBC, Yahoo Finance
- Volume analysis: NYSE daily trading data

**Methodology:**
- Moving averages: Simple moving average (SMA) calculations
- RSI: 14-period relative strength index
- Bollinger Bands: 20-period, 2 standard deviations
- MACD: 12-26-9 standard parameters

**Disclaimer:**
This analysis is for informational purposes only and does not constitute investment advice. Past performance does not guarantee future results.

---

**Report ID:** [from JSON if available]
**Generated:** January 13, 2026, 2:28 PM UTC
**Confidentiality:** Internal Use
```

---

## Skill 10: HTML Generation with KXAITrader Aesthetics

**Purpose:** Create production-ready HTML reports with proper styling

**HTML structure template:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Report Title]</title>
    <style>
        /* KXAITrader aesthetic CSS */
        /* See kxaitrader_styles.css for complete stylesheet */
    </style>
</head>
<body>
    <header class="report-header">
        <h1 class="main-title">[Strategic Title]</h1>
        <p class="subtitle">[Context-setting subtitle]</p>
        <div class="metadata">
            <span>Report Date: [Date]</span>
            <span>Asset: [Ticker]</span>
        </div>
    </header>

    <section class="executive-summary">
        <h2>Executive Summary</h2>
        [Content]
    </section>

    <section class="main-content">
        <h2 class="section-heading">[Section 1 Title]</h2>
        [Content]
        
        <div class="exhibit">
            <h3 class="exhibit-title">Exhibit 1: [Title]</h3>
            [Chart/description]
        </div>
    </section>

    [Additional sections...]

    <footer class="report-footer">
        <div class="sources">
            <h4>Data Sources</h4>
            [Sources list]
        </div>
        <div class="metadata">
            Report ID: [ID] | Generated: [Timestamp]
        </div>
    </footer>
</body>
</html>
```

**CSS color variables (KXAITrader palette):**
```css
:root {
    --kxaitrader-navy: #003366;
    --kxaitrader-charcoal: #404040;
    --kxaitrader-teal: #00A3A1;
    --kxaitrader-gold: #F2A900;
    --kxaitrader-coral: #E06055;
    --kxaitrader-light-grey: #F5F5F5;
    --kxaitrader-white: #FFFFFF;
}
```

---

## Skill Application Checklist

When generating a report, ensure these skills are applied:

- [ ] **Strategic Titles:** All section headings insight-driven
- [ ] **Technical Translation:** No unexplained jargon
- [ ] **Data Contextualization:** All numbers have comparisons/context
- [ ] **Narrative Flow:** Logical progression with smooth transitions
- [ ] **Synthesis:** Multiple perspectives integrated into frameworks
- [ ] **Exhibit Descriptions:** 3-5 visualizations specified with insight-driven titles
- [ ] **Risk Articulation:** Structured with probability, impact, mitigation
- [ ] **Action Items:** Specific, measurable, time-bound recommendations
- [ ] **Source Attribution:** Clean citations and data source footer
- [ ] **HTML Aesthetics:** Proper KXAITrader styling if HTML output

---

## Continuous Improvement

**Skill refinement process:**
1. Generate report using skills
2. Review against examples
3. Identify weak areas
4. Practice specific skill in isolation
5. Integrate improved skill into next report
6. Build personal library of successful patterns

**Success metrics:**
- Can executive understand report without questions?
- Would report pass for KXAITrader engagement deliverable?
- Are all technical concepts accessible to non-specialists?
- Do exhibits advance arguments vs. just displaying data?
- Are recommendations actionable without additional clarification?
