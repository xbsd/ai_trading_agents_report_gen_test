# KXAITrader HTML Report Generation Prompt

Generate a complete, standalone HTML report with KXAITrader & Company's signature aesthetic and editorial standards. The output should be a single HTML file with embedded CSS that can be opened directly in a browser or converted to PDF.

## JSON Input Data
```
[PASTE YOUR JSON DATA HERE]
```

## Output Requirements

### Technical Specifications
- **Format**: Single standalone HTML5 file
- **CSS**: Embedded inline (between `<style>` tags) using kxaitrader_styles.css
- **Encoding**: UTF-8
- **Responsiveness**: Desktop-optimized, mobile-friendly, print-ready
- **Browser compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)

### KXAITrader Aesthetic Standards

**Color Palette** (use CSS variables):
```css
--navy: #003366        /* Authority, primary headings */
--charcoal: #404040    /* Professional body text */
--teal: #00A3A1       /* Innovation, analytical callouts */
--gold: #F2A900       /* Caution, financial metrics */
--coral: #E06055      /* Risk, urgent action items */
--light-grey: #F5F5F5 /* Background panels */
```

**Typography**:
- Headings: Sans-serif (Helvetica Neue, Arial fallback)
- Body: Serif (Georgia, Times New Roman fallback)
- Line height: 1.6 for body, 1.2-1.3 for headings
- Font sizes: H1 (2.5rem), H2 (1.75rem), H3 (1.35rem), Body (1rem)

**Layout**:
- Max width: 900px, centered
- Margins: 1.5-2rem padding
- White space: Generous (1.5-3rem between sections)
- Print margins: 1.25 inches equivalent

### HTML Structure

**Required sections** (in order):
1. **Header** (`<header class="report-header">`)
   - Main title (H1, insight-driven, outcome-focused)
   - Subtitle (context-setting tagline)
   - Metadata bar (date, asset, event)

2. **Executive Summary** (`<section class="executive-summary">`)
   - 300-400 word strategic overview
   - Key Insights box with 3-5 bullets
   - Must stand alone as complete brief

3. **The Situation** (`<section class="main-content">`)
   - Market context and timeline
   - Key developments
   - Use H2 for section heading, H3 for subsections

4. **Core Analysis** (`<section class="main-content">`)
   - Strategic frameworks
   - Minimum 2 exhibits with descriptions
   - Tables for comparative data
   - Callout boxes for key insights

5. **Implications & Risk** (`<section class="main-content">`)
   - Strategic considerations
   - Risk callout box (use `callout-risk` class)
   - Scenario analysis

6. **Recommended Actions** (`<section class="main-content">`)
   - Decision-tree format
   - Action callout boxes (use `callout-action` class)
   - Specific, time-bound recommendations

7. **Footer** (`<footer class="report-footer">`)
   - Data sources (bulleted list)
   - Methodology notes
   - Disclaimer
   - Report metadata (ID, timestamp, confidentiality)

### CSS Classes Reference

**Structure classes**:
- `.report-header` - Header container
- `.main-title` / `h1` - Primary title
- `.subtitle` - Tagline below title
- `.metadata` - Date/asset/event bar
- `.executive-summary` - Grey box with teal accent
- `.main-content` - Content sections
- `.section-heading` / `h2` - Major sections (navy, with top border)
- `.subsection-heading` / `h3` - Subsections
- `.report-footer` - Footer container

**Exhibit classes**:
- `.exhibit` - Grey box with navy accent
- `.exhibit-title` - Insight-driven exhibit heading
- `.chart-placeholder` - For chart specifications
- `.exhibit-description` - Italic description text
- `.exhibit-source` - Small source attribution

**Callout classes**:
- `.callout` - Base callout box (grey background, left border)
- `.callout-insight` - Teal accent (for insights)
- `.callout-risk` - Coral accent (for risks)
- `.callout-action` - Gold accent (for actions)
- `.callout-title` - Bold title in callout

**Table classes**:
- Standard `<table>` automatically styled
- Navy header, alternating row backgrounds
- No need for additional classes

**Utility classes**:
- `.text-center`, `.text-right` - Text alignment
- `.text-navy`, `.text-teal`, `.text-coral`, `.text-gold` - Text colors
- `.mt-sm/md/lg/xl`, `.mb-sm/md/lg/xl` - Margin spacing
- `.page-break` - Force page break for printing
- `.no-break` - Prevent break inside element

### Content Transformation Rules

**From JSON to HTML**:

1. **Extract headline** → Main title (H1)
   - Make it insight-driven and outcome-focused
   - Example: "Oracle's 42% Correction Creates Strategic Entry Window"

2. **Create subtitle** from context
   - Frame the stakes and strategic significance
   - Example: "Technical oversold conditions and institutional accumulation signal potential inflection point"

3. **Transform key_findings** → Executive Summary bullets
   - Synthesize into 3-5 concise insights
   - Use `<div class="key-insights">` box

4. **Transform analysis sections** → Strategic frameworks
   - day_trader → "Short-Term Tactical Opportunity (1-2 weeks)"
   - swing_trader → "Medium-Term Position Trade (2-6 weeks)"
   - momentum_trader → "Trend-Following Strategy (2-4 weeks)"
   - growth_investor → "Long-Term Growth Thesis (12-24 months)"
   - value_investor → "Intrinsic Value Assessment (12-24 months)"

5. **Create exhibits** from data patterns
   - Minimum 2-3 exhibits with specifications
   - Use `.chart-placeholder` for chart descriptions
   - Insight-driven titles (not "Price Chart" but "42% decline from October peak creates potential value entry")

6. **Extract risk factors** → Risk callout box
   - Organize by category (market, fundamental, execution)
   - Use `<div class="callout callout-risk">`

7. **Format actions** → Action callout boxes
   - One box per investor type
   - Include entry, targets, stops, risk/reward
   - Use `<div class="callout callout-action">`

8. **Parse sources** → Footer list
   - Extract from JSON sources field
   - Format as clean bulleted list

### Technical Data Translation

Transform technical indicators into business language:

| Technical | HTML Output |
|-----------|-------------|
| "RSI 53.69" | "Momentum indicators have recovered from oversold levels without reaching overbought extremes, leaving room for continuation" |
| "MACD -3.98" | "The rate of decline is decelerating, an early signal that downward momentum may be exhausting" |
| "Upper BB test" | "Price approaching the upper bounds of its recent volatility range, indicating potential inflection" |
| "26.2M volume vs 16-19M avg" | "Trading activity 38% above normal suggests institutional accumulation rather than retail speculation" |

### Exhibit Specifications

For each exhibit, provide:

```html
<div class="exhibit">
    <h3 class="exhibit-title">Exhibit 1: [Insight-driven title]</h3>
    
    <div class="chart-placeholder">
        [Chart Type: Line chart]
        
        Data Series:
        - Series 1: Daily closing price (Navy #003366, 2px line)
        - Series 2: 50-day moving average (Teal #00A3A1, 1.5px line)
        - Series 3: 200-day moving average (Gold #F2A900, 1.5px line)
        
        X-Axis: Date range from [start] to [end]
        Y-Axis: Price range $180 to $330
        
        Key Annotations:
        - October 16 peak: $321.69 (label with date)
        - January 8 low: $185.66 (label with date, coral highlight)
        - Current price: $204.68 (label with date)
        
        Design: Minimal gridlines, direct series labels, generous white space
    </div>
    
    <p class="exhibit-description">
        The 42% correction from October peak to January low represents one of the most severe 
        repricing events for a large-cap technology stock in recent quarters, creating potential 
        opportunity for value-oriented investors.
    </p>
    
    <p class="exhibit-source">Source: Daily price data via Alpha Vantage, 3-month history</p>
</div>
```

### Quality Checklist

Before finalizing HTML:
- [ ] All CSS embedded inline (no external dependencies)
- [ ] Proper HTML5 structure with semantic elements
- [ ] All KXAITrader color palette colors used appropriately
- [ ] Responsive design (check mobile breakpoint)
- [ ] Print styles defined (@media print)
- [ ] All section headings insight-driven (not generic)
- [ ] Executive summary can stand alone
- [ ] Minimum 2-3 exhibits with detailed specifications
- [ ] Risk and action callout boxes included
- [ ] Footer has sources, methodology, disclaimer, metadata
- [ ] No Lorem Ipsum or placeholder text (except chart-placeholder divs)
- [ ] File can be opened directly in browser
- [ ] Professional, presentation-ready appearance

### Example Invocations

**Basic usage:**
```
Generate a KXAITrader-style HTML report from this JSON:
[paste JSON]
```

**With customization:**
```
Generate a KXAITrader-style HTML report from this JSON:
[paste JSON]

Customization:
- Target audience: Board of directors
- Emphasis: Risk management and downside protection
- Include: 4 exhibits (price action, volume, risk matrix, decision tree)
- Length: Executive version (2,000 words max)
```

**Using agent workflow:**
```
@KXAITrader_Report_Writer generate HTML report from JSON:
[paste JSON]

Then @Exhibit_Designer specify 3 exhibits:
1. Price movement with support/resistance
2. Volume analysis showing institutional activity
3. Risk-return comparison matrix

Then @Quality_Reviewer ensure HTML is production-ready
```

### Output Format

The output should be a complete, valid HTML5 document starting with:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    ...
```

And ending with:
```html
    </footer>
</body>
</html>
```

Ready to paste into a .html file and open in any browser.

---

## Now Generate Report

Using the JSON data provided above, generate a complete, standalone HTML report following all KXAITrader aesthetic and editorial standards. Ensure the HTML is production-ready, visually sophisticated, and suitable for executive presentation.
