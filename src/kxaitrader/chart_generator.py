"""
Chart generation using Plotly for professional trading visualizations.
"""

import base64
from io import BytesIO
from typing import Optional

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .config import Config


class ChartGenerator:
    """Generate professional trading charts using Plotly."""

    def __init__(self, config: Config, use_interactive: bool = True):
        """
        Initialize the chart generator with configuration.

        Args:
            config: Configuration object
            use_interactive: If True, generate interactive HTML charts instead of static images
        """
        self.config = config
        self.colors = config.colors
        self.use_interactive = use_interactive

    def _fig_to_base64(self, fig: go.Figure, format: str = "png") -> str:
        """
        Convert a Plotly figure to output format.

        If use_interactive is True, returns an HTML div with the interactive chart.
        Otherwise, attempts to generate a base64 encoded static image.
        """
        if self.use_interactive:
            # Return interactive HTML div
            return fig.to_html(
                full_html=False,
                include_plotlyjs=False,  # We'll include it once in the main HTML
                config={
                    "displayModeBar": True,
                    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                    "displaylogo": False,
                    "responsive": True,
                },
            )

        # Try static image generation (requires kaleido + Chrome)
        try:
            img_bytes = fig.to_image(
                format=format,
                width=self.config.chart_width,
                height=self.config.chart_height,
                scale=2,
            )
            b64 = base64.b64encode(img_bytes).decode("utf-8")
            return f"data:image/{format};base64,{b64}"
        except Exception:
            # Fall back to interactive if static fails
            return fig.to_html(
                full_html=False,
                include_plotlyjs=False,
                config={"displayModeBar": True, "displaylogo": False, "responsive": True},
            )

    def _apply_professional_layout(self, fig: go.Figure, title: str = "") -> go.Figure:
        """Apply professional styling to a figure."""
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(size=16, color=self.colors["navy"], family="Helvetica Neue, Arial, sans-serif"),
                x=0,
                xanchor="left",
            ),
            font=dict(family="Helvetica Neue, Arial, sans-serif", size=11, color=self.colors["charcoal"]),
            plot_bgcolor=self.colors["white"],
            paper_bgcolor=self.colors["white"],
            margin=dict(l=60, r=40, t=60, b=60),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor=self.colors["medium_grey"],
                borderwidth=1,
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor=self.colors["light_grey"],
                gridwidth=1,
                linecolor=self.colors["medium_grey"],
                linewidth=1,
                tickfont=dict(size=10),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=self.colors["light_grey"],
                gridwidth=1,
                linecolor=self.colors["medium_grey"],
                linewidth=1,
                tickfont=dict(size=10),
            ),
            hovermode="x unified",
        )
        return fig

    def generate_price_chart(
        self,
        df: pd.DataFrame,
        symbol: str,
        include_sma: bool = True,
        include_volume: bool = True,
        annotations: Optional[list] = None,
    ) -> str:
        """
        Generate a price chart with moving averages and volume.

        Args:
            df: DataFrame with OHLCV data and technical indicators
            symbol: Stock ticker symbol
            include_sma: Whether to include moving averages
            include_volume: Whether to include volume subplot
            annotations: Optional list of annotation dicts

        Returns:
            Base64 encoded PNG image
        """
        if include_volume:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3],
                subplot_titles=("", "Volume (M)"),
            )
        else:
            fig = go.Figure()

        # Main price line
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["close"],
                mode="lines",
                name="Price",
                line=dict(color=self.colors["navy"], width=2),
                hovertemplate="$%{y:.2f}<extra></extra>",
            ),
            row=1 if include_volume else None,
            col=1 if include_volume else None,
        )

        # Moving averages
        if include_sma and "sma_50" in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["sma_50"],
                    mode="lines",
                    name="50-day SMA",
                    line=dict(color=self.colors["teal"], width=1.5, dash="dash"),
                    hovertemplate="$%{y:.2f}<extra></extra>",
                ),
                row=1 if include_volume else None,
                col=1 if include_volume else None,
            )

        if include_sma and "sma_200" in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["sma_200"],
                    mode="lines",
                    name="200-day SMA",
                    line=dict(color=self.colors["gold"], width=1.5, dash="dash"),
                    hovertemplate="$%{y:.2f}<extra></extra>",
                ),
                row=1 if include_volume else None,
                col=1 if include_volume else None,
            )

        # Volume bars
        if include_volume:
            colors = [
                self.colors["green"] if df["close"].iloc[i] >= df["open"].iloc[i] else self.colors["coral"]
                for i in range(len(df))
            ]
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df["volume"] / 1_000_000,
                    name="Volume",
                    marker_color=colors,
                    opacity=0.7,
                    hovertemplate="%{y:.1f}M<extra></extra>",
                ),
                row=2,
                col=1,
            )

            # Volume average line
            if "volume_sma" in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df["volume_sma"] / 1_000_000,
                        mode="lines",
                        name="20-day Avg",
                        line=dict(color=self.colors["charcoal"], width=1),
                        hovertemplate="%{y:.1f}M<extra></extra>",
                    ),
                    row=2,
                    col=1,
                )

        # Add annotations
        if annotations:
            for ann in annotations:
                fig.add_annotation(
                    x=ann.get("x"),
                    y=ann.get("y"),
                    text=ann.get("text", ""),
                    showarrow=ann.get("showarrow", True),
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=1,
                    arrowcolor=ann.get("color", self.colors["navy"]),
                    font=dict(size=10, color=ann.get("color", self.colors["navy"])),
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor=ann.get("color", self.colors["navy"]),
                    borderwidth=1,
                )

        fig = self._apply_professional_layout(fig, f"{symbol} - Price & Volume Analysis")

        if include_volume:
            fig.update_yaxes(title_text="Price ($)", row=1, col=1)
            fig.update_yaxes(title_text="Volume (M)", row=2, col=1)

        return self._fig_to_base64(fig)

    def generate_candlestick_chart(
        self,
        df: pd.DataFrame,
        symbol: str,
        include_bollinger: bool = True,
    ) -> str:
        """
        Generate a candlestick chart with Bollinger Bands.

        Args:
            df: DataFrame with OHLCV data and technical indicators
            symbol: Stock ticker symbol
            include_bollinger: Whether to include Bollinger Bands

        Returns:
            Base64 encoded PNG image
        """
        fig = go.Figure()

        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="OHLC",
                increasing_line_color=self.colors["green"],
                decreasing_line_color=self.colors["coral"],
            )
        )

        # Bollinger Bands
        if include_bollinger and "boll_upper" in df.columns:
            # Upper band
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["boll_upper"],
                    mode="lines",
                    name="Upper Band",
                    line=dict(color=self.colors["medium_grey"], width=1),
                    hovertemplate="$%{y:.2f}<extra></extra>",
                )
            )
            # Lower band
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["boll_lower"],
                    mode="lines",
                    name="Lower Band",
                    line=dict(color=self.colors["medium_grey"], width=1),
                    fill="tonexty",
                    fillcolor="rgba(204, 204, 204, 0.2)",
                    hovertemplate="$%{y:.2f}<extra></extra>",
                )
            )
            # Middle band (20 SMA)
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["boll_mid"],
                    mode="lines",
                    name="20-day SMA",
                    line=dict(color=self.colors["teal"], width=1, dash="dot"),
                    hovertemplate="$%{y:.2f}<extra></extra>",
                )
            )

        fig = self._apply_professional_layout(fig, f"{symbol} - Candlestick with Bollinger Bands")
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_yaxes(title_text="Price ($)")

        return self._fig_to_base64(fig)

    def generate_technical_indicators_chart(
        self,
        df: pd.DataFrame,
        symbol: str,
    ) -> str:
        """
        Generate a multi-panel chart with RSI and MACD.

        Args:
            df: DataFrame with technical indicators
            symbol: Stock ticker symbol

        Returns:
            Base64 encoded PNG image
        """
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.5, 0.25, 0.25],
            subplot_titles=("Price", "RSI (14)", "MACD (12,26,9)"),
        )

        # Price
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["close"],
                mode="lines",
                name="Price",
                line=dict(color=self.colors["navy"], width=2),
            ),
            row=1, col=1,
        )

        # RSI
        if "rsi" in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["rsi"],
                    mode="lines",
                    name="RSI",
                    line=dict(color=self.colors["teal"], width=1.5),
                ),
                row=2, col=1,
            )
            # Overbought/Oversold lines
            fig.add_hline(y=70, line_dash="dash", line_color=self.colors["coral"], row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color=self.colors["green"], row=2, col=1)
            fig.add_hline(y=50, line_dash="dot", line_color=self.colors["medium_grey"], row=2, col=1)

        # MACD
        if "macd" in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["macd"],
                    mode="lines",
                    name="MACD",
                    line=dict(color=self.colors["navy"], width=1.5),
                ),
                row=3, col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["macd_signal"],
                    mode="lines",
                    name="Signal",
                    line=dict(color=self.colors["coral"], width=1),
                ),
                row=3, col=1,
            )
            # Histogram
            colors = [
                self.colors["green"] if val >= 0 else self.colors["coral"]
                for val in df["macd_hist"].fillna(0)
            ]
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df["macd_hist"],
                    name="Histogram",
                    marker_color=colors,
                    opacity=0.5,
                ),
                row=3, col=1,
            )

        fig = self._apply_professional_layout(fig, f"{symbol} - Technical Indicators Dashboard")

        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)
        fig.update_yaxes(title_text="MACD", row=3, col=1)

        return self._fig_to_base64(fig)

    def generate_volume_analysis_chart(
        self,
        df: pd.DataFrame,
        symbol: str,
    ) -> str:
        """
        Generate a volume analysis chart showing price vs volume correlation.

        Args:
            df: DataFrame with OHLCV data
            symbol: Stock ticker symbol

        Returns:
            Base64 encoded PNG image
        """
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.6, 0.4],
        )

        # Price with daily change color coding
        colors = [
            self.colors["green"] if df["close"].iloc[i] >= df["open"].iloc[i] else self.colors["coral"]
            for i in range(len(df))
        ]

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["close"],
                mode="lines+markers",
                name="Close Price",
                line=dict(color=self.colors["navy"], width=2),
                marker=dict(size=4, color=colors),
            ),
            row=1, col=1,
        )

        # Volume bars with color coding
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df["volume"] / 1_000_000,
                name="Volume",
                marker_color=colors,
                opacity=0.7,
            ),
            row=2, col=1,
        )

        # Volume average
        if "volume_sma" in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["volume_sma"] / 1_000_000,
                    mode="lines",
                    name="20-day Avg Volume",
                    line=dict(color=self.colors["charcoal"], width=1.5, dash="dash"),
                ),
                row=2, col=1,
            )

        fig = self._apply_professional_layout(fig, f"{symbol} - Price & Volume Correlation")
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Volume (M)", row=2, col=1)

        return self._fig_to_base64(fig)

    def generate_performance_summary_chart(
        self,
        df: pd.DataFrame,
        symbol: str,
        period_days: int = 90,
    ) -> str:
        """
        Generate a performance summary showing returns over different periods.

        Args:
            df: DataFrame with OHLCV data
            symbol: Stock ticker symbol
            period_days: Number of days to analyze

        Returns:
            Base64 encoded PNG image
        """
        # Calculate returns for different periods
        current_price = df["close"].iloc[-1]

        periods = {
            "1 Week": 5,
            "1 Month": 21,
            "3 Months": 63,
            "YTD": min(len(df) - 1, 252),
        }

        returns = []
        labels = []
        for label, days in periods.items():
            if len(df) > days:
                past_price = df["close"].iloc[-(days + 1)]
                ret = ((current_price - past_price) / past_price) * 100
                returns.append(ret)
                labels.append(label)

        colors = [self.colors["green"] if r >= 0 else self.colors["coral"] for r in returns]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=labels,
                y=returns,
                marker_color=colors,
                text=[f"{r:+.1f}%" for r in returns],
                textposition="outside",
                textfont=dict(size=12, color=self.colors["charcoal"]),
            )
        )

        fig = self._apply_professional_layout(fig, f"{symbol} - Period Returns (%)")
        fig.update_yaxes(title_text="Return (%)")
        fig.add_hline(y=0, line_color=self.colors["charcoal"], line_width=1)

        return self._fig_to_base64(fig)
