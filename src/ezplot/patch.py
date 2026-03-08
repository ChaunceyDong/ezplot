import pandas as pd
from .core import df_plot2


def ezplot(self, *args, **kwargs):
    return df_plot2(self, *args, **kwargs)


pd.DataFrame.ezplot = ezplot
