import os

import numpy as np
import pandas as pd
import plotly
from plotly import graph_objs as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler


def plot_ts(df1, df2=None, plot_file_name="plotly-ts.html", output_html=True, is_dismiss_no_trading_time=True,
            sig_df=None, output_obj=False, hover_cols_df=None):
    """
    df1 and df2 use different y-axis
    """
    # Create figure with secondary y-axis
    if type(df1) == pd.Series:
        df1 = pd.DataFrame(df1)

    if type(df2) == pd.DataFrame:
        df2 = pd.DataFrame(df2)

    if hover_cols_df is not None:
        df1['hover_text'] = ""
        for col in hover_cols_df.columns:
            df1['hover_text'] += col + ": " + hover_cols_df[col].astype(str) + "<br>"

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for col in df1.columns:
        fig.add_trace(
            go.Scatter(
                name=str(col),
                x=df1.index,
                y=df1[col],
                mode='lines',
                text=df1['hover_text'] if hover_cols_df is not None else None,
            ),
            secondary_y=False
        )

    if df2 is not None:
        for col in df2.columns:
            fig.add_trace(
                go.Scatter(
                    name=str(col),
                    x=df2.index,
                    y=df2[col],
                    mode='lines',
                ),
                secondary_y=True
            )

    if sig_df is not None:
        fig = add_sig_maker(sig_df, fig, df1['hover_text'])

    if is_dismiss_no_trading_time:
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=[11.5, 13], pattern="hour")
            ]
        )

    if output_obj:
        return fig

    if output_html:
        plotly.offline.plot(fig, filename=plot_file_name)
    else:
        fig.show()


def add_sig_maker(df, fig, hover_text_series=None):
    """
    plot signal scatters
    df should have ['signal', 'price']. signal values be 0, 1, -1
    'hover_text' is optional
    """

    df_buy = df.loc[df['signal'] == 1, ['price', 'signal']]
    fig.add_trace(
        go.Scatter(
            name='buy',
            x=df_buy.index,
            y=df_buy['price'],
            text=hover_text_series,
            mode='markers',
            marker=dict(
                color='red',
                size=10,
                symbol='triangle-up',
            )
        )
    )

    df_sell = df.loc[df['signal'] == -1, ['price', 'signal']]
    fig.add_trace(
        go.Scatter(
            name='sell',
            x=df_sell.index,
            y=df_sell['price'],
            text=hover_text_series,
            mode='markers',
            marker=dict(
                color='green',
                size=10,
                symbol='triangle-down',
            ),
        )
    )
    return fig


def plot_two_ts(series1, series2, plot_file_name="", series1_name="", series2_name="", output_html=False):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            name=series1_name if not series1_name == "" else str(series1.name),
            x=series1.index,
            y=series1,
            mode='lines',
        ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            name=series2_name if not series2_name == "" else str(series2.name),
            x=series2.index,
            y=series2,
            mode='lines',
        ),
        secondary_y=True
    )
    if output_html:
        plotly.offline.plot(fig, filename=plot_file_name)
    else:
        fig.show()


def add_lines(fig, df, cols_plot, **kwargs):
    """Add lines to fig with given y_plot"""
    if type(cols_plot) == str:
        cols_plot = [cols_plot]

    for col in cols_plot:
        fig.add_trace(
            go.Scatter(
                name=col,
                x=df.index,
                y=df[col],
                mode='lines',
            ),
            **kwargs
        )


def df_plot2(
        df, y, y2=(), yd=(), yd2=(), yd3=(), x=None, filter=None,
        output_html=False, output_name=None,
        break_time=None,  # break_time=(11.5, 13)
        auto_open=True,
):
    """
    using plotly to plot df with 2 y-axis
            +--------------+
            |              |
          y |              | y2
            |              |
            +--------------+
          yd|              | yd2
            +--------------+
          yd3|             |
            +--------------+

    """

    if len(yd) + len(yd2) == 0 and len(yd3) == 0:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
    elif len(yd3) > 0:
        fig = make_subplots(
            rows=3, cols=1, row_heights=(1.0, 0.25, 0.25),
            shared_xaxes=True, vertical_spacing=0.01,
            specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{"secondary_y": False}]]
        )
    else:
        fig = make_subplots(
            rows=2, cols=1, row_heights=(1.0, 0.25),
            shared_xaxes=True, vertical_spacing=0.01,
            specs=[[{"secondary_y": True}], [{"secondary_y": True}]]
        )

    if filter is not None:
        df = df[filter]

    if x is not None:
        df = df.set_index(x)

    add_lines(fig, df, y, row=1, col=1, secondary_y=False)
    add_lines(fig, df, y2, row=1, col=1, secondary_y=True)
    add_lines(fig, df, yd, row=2, col=1, secondary_y=False)
    add_lines(fig, df, yd2, row=2, col=1, secondary_y=True)
    if len(yd3) > 0:
        add_lines(fig, df, yd3, row=3, col=1, secondary_y=False)

    if break_time is not None:
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=break_time, pattern="hour")
            ]
        )

    if output_html or output_name is not None:
        output_name = output_name if output_name is not None else 'plot.html'
        os.makedirs(os.path.dirname(os.path.abspath(output_name)), exist_ok=True)
        plotly.offline.plot(fig, filename=output_name, auto_open=auto_open)
    else:
        fig.show()


def scale_size(size_series):
    size_series = pd.to_numeric(size_series)
    max = size_series.max()
    return size_series / max * 30


def plot_hft_analysis(df, output_html=True, output_name='plot.html', is_dismiss_no_trading_time=True):
    """
    plot hft analysis, including bid-ask price and our order info

    columns in df:
        bid1, ap1
        my_best_bid, my_best_ask
        pnl, sigv, pos
    """

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            name='bid1',
            x=df.index,
            y=df['bp1'],
            mode='lines',
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            name='ask1',
            x=df.index,
            y=df['ap1'],
            mode='lines',
        ),
        secondary_y=False
    )

    df['my_best_bid'].replace("0", np.nan, inplace=True)
    df['my_best_ask'].replace("0", np.nan, inplace=True)
    df['my_best_ask'].replace("9999999999999", np.nan, inplace=True)

    add_my_bid_ask(fig, df)

    fig = add_pnl_sigv_pos(fig, df)

    if is_dismiss_no_trading_time:
        dismiss_notrading_time(fig)

    if output_html:
        plotly.offline.plot(fig, filename=output_name)
    else:
        fig.show()


def add_pnl_sigv_pos(fig, df):
    """
    add pnl, sigv, pos to fig secondary_y
    """

    df_2y = df[['pnl', 'sigv', 'pos']].fillna(0).apply(pd.to_numeric)
    df_2y.iloc[0, 1] = 0  # in order to cache zero line
    pnl_max = df_2y['pnl'].max()
    pnl_min = df_2y['pnl'].min()
    pnl_range = pnl_max - pnl_min
    if pnl_min == pnl_max == 0:
        print("pnl not change, just return")
        return

    df_2y_scaler = pd.DataFrame(MinMaxScaler(feature_range=(pnl_min, pnl_max)).fit_transform(df_2y),
                                columns=df_2y.columns, index=df_2y.index)
    df_2y_scaler[['sigv', 'pos']] = (df_2y_scaler[['sigv', 'pos']] - pnl_range / 2) / 3
    df_2y_scaler['sigv_0'] = df_2y_scaler.iloc[0, 1]

    fig.add_trace(
        go.Scatter(
            name='pnl',
            x=df_2y_scaler.index,
            y=df_2y_scaler['pnl'],
            mode='lines',
            line=dict(color="#0000ff")
        ),
        secondary_y=True
    )

    fig.add_trace(
        go.Scatter(
            name='pos',
            x=df_2y_scaler.index,
            y=df_2y_scaler['pos'],
            mode='lines',
        ),
        secondary_y=True
    )

    fig.add_trace(
        go.Scatter(
            name='sigv_0',
            x=df_2y_scaler.index,
            y=df_2y_scaler['sigv_0'],
            mode='lines',
        ),
        secondary_y=True
    )

    fig.add_trace(
        go.Scatter(
            name='sigv',
            x=df_2y_scaler.index,
            y=df_2y_scaler['sigv'],
            mode='lines',
        ),
        secondary_y=True
    )

    return fig


def bbo_trade_plot(df, output_html=True, output_name='plot.html', is_dismiss_no_trading_time=True):
    """
    plot bbo & trade point
    """

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for col in ['bp', 'ap']:
        series = df[col]
        fig.add_trace(
            go.Scatter(
                name=col,
                x=series.index,
                y=series,
                mode='lines',
            ),
            secondary_y=False
        )

    plot_trade_triangle(df, fig)

    if is_dismiss_no_trading_time:
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=(11.5, 13), pattern="hour")
            ]
        )

    if output_html:
        plotly.offline.plot(fig, filename=output_name)
    else:
        fig.show()


def plot_trade_triangle(fig, df):
    """
    plot trade triangle, with columns 'price'
    """
    df['trade_up'] = np.where(df['aggressive_side'] == 0, df['price'], np.nan)
    df['trade_down'] = np.where(df['aggressive_side'] == 1, df['price'], np.nan)

    fig.add_trace(
        go.Scatter(
            name='my_bid',
            x=df.index,
            y=df['trade_up'],
            mode='markers',
            marker=dict(
                color="#800000",
                symbol='triangle-up'
            )
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            name='my_ask',
            x=df.index,
            y=df['trade_down'],
            mode='markers',
            marker=dict(
                color="#003300",
                symbol='triangle-down'
            )
        ),
        secondary_y=False,
    )


def dismiss_notrading_time(fig):
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=[11.5, 13], pattern="hour")
        ]
    )


def add_my_bid_ask(fig, df, bid_name='my_best_bid', ask_name='my_best_ask'):
    """
    add my bid-ask triangle scatter to plotly fig.
    """
    fig.add_trace(
        go.Scatter(
            name='my_bid',
            x=df.index,
            y=df[bid_name],
            mode='markers',
            marker=dict(
                color="#800000",
                symbol='triangle-up'
            )
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            name='my_ask',
            x=df.index,
            y=df[ask_name],
            mode='markers',
            marker=dict(
                color="#003300",
                symbol='triangle-down'
            )
        ),
        secondary_y=False,
    )
