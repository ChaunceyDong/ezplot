# ezplot

Interactive plotting toolkit for time-series and HFT data, built on Plotly.

## Install

```bash
pip install easyplots
```

## Quick Start

### `df.ezplot()` Layout

```
        +--------------+
        |              |
      y |              | y2
        |              |
        +--------------+
     yd |              | yd2
        +--------------+
    yd3 |              |
        +--------------+
```

- **y / y2** — Main panel with dual y-axes (left / right)
- **yd / yd2** — Secondary panel with dual y-axes
- **yd3** — Third panel (single y-axis)

All panels share the x-axis and support zooming/panning together.

### Usage

```python
import ezplot  # auto-registers df.ezplot()

df.ezplot(
    y=["mid_price", "theo"],       # main panel, left y-axis
    y2=["pnl"],                    # main panel, right y-axis
    yd=["spread"],                 # secondary panel, left y-axis
    yd2=["volume"],                # secondary panel, right y-axis
    yd3=["position"],              # third panel
    break_time=(11.5, 13),         # hide lunch break
)
```
 
## License

MIT
