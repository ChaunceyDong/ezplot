"""ezplot - Interactive plotting toolkit for time-series and HFT data."""

__version__ = "0.2.1"

from .core import (
    add_lines,
    add_my_bid_ask,
    add_pnl_sigv_pos,
    bbo_trade_plot,
    df_plot2,
    dismiss_notrading_time,
    plot_hft_analysis,
    plot_trade_triangle,
    scale_size,
)

# Auto-register DataFrame.ezplot()
from . import patch  # noqa: F401

__all__ = [
    "__version__",
    "add_lines",
    "add_my_bid_ask",
    "add_pnl_sigv_pos",
    "bbo_trade_plot",
    "df_plot2",
    "dismiss_notrading_time",
    "plot_hft_analysis",
    "plot_trade_triangle",
    "scale_size",
]
