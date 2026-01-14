"""
Configuration management for KXAITrader report generation.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """Configuration for report generation."""

    alpha_vantage_api_key: str
    output_dir: Path = field(default_factory=lambda: Path("./output"))
    chart_format: str = "png"

    # Color palette for charts and reports
    colors: dict = field(default_factory=lambda: {
        "navy": "#003366",
        "charcoal": "#404040",
        "teal": "#00A3A1",
        "gold": "#F2A900",
        "coral": "#E06055",
        "light_grey": "#F5F5F5",
        "medium_grey": "#CCCCCC",
        "white": "#FFFFFF",
        "green": "#2ECC71",
        "red": "#E74C3C",
    })

    # Chart styling defaults
    chart_height: int = 400
    chart_width: int = 850

    def __post_init__(self):
        """Ensure output directory exists."""
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
