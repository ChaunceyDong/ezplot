# ezplot

Interactive plotting toolkit for time-series and HFT data, built on Plotly.

## Install

```bash
pip install easyplots
```

## Quick Start

```python
import pandas as pd
import ezplot  # auto-registers df.ezplot()

# DataFrame quick plot — dual y-axis with subplots
df.ezplot(y=['price', 'volume'], y2=['signal'], yd=['pnl'])

# Or call directly
from ezplot import df_plot2, plot_ts

df_plot2(df, y=['bid', 'ask'], y2=['spread'])
plot_ts(df[['mid']], df[['volume']])
```

## API

### `df.ezplot(y, y2, yd, yd2, yd3, ...)`

Monkey-patched onto `pd.DataFrame`. Shortcut for `df_plot2()`.

### `df_plot2(df, y, y2, yd, yd2, yd3, ...)`

Multi-panel plotly chart with dual y-axes.

### `plot_ts(df1, df2, ...)`

Plot one or two DataFrames with dual y-axis.

## License

MIT
