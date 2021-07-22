import matplotlib.pyplot as plt
import pandas as pd
import llog

# https://stackoverflow.com/questions/47466255/subclassing-a-pandas-dataframe-updates
# https://stackoverflow.com/questions/47466255/subclassing-a-pandas-dataframe-updates
class LLogSeries(pd.Series):
    _metadata = ['meta']

    @property
    def _constructor(self):
        return LLogSeries

    @property
    def _constructor_expanddim(self):
        return LLogDataFrame

    def pplot(self, *args, **kwargs):
        print(f'sup {self.name}')

        # print(self.index.get_loc(self.name))
        meta = self.meta[self.name]
        kwargs = kwargs | {'label': self.name}

        for opt in ["color", "style", "label"]:
            try:
                kwargs = kwargs | {opt:meta[opt]}
            except KeyError as e:
                # print(e)
                pass

        self.plot(*args, **kwargs)
        plt.legend()
        plt.ylabel(meta['units'])
        
    
# https://stackoverflow.com/questions/48325859/subclass-pandas-dataframe-with-required-argument
class LLogDataFrame(pd.DataFrame):
    _metadata = ['meta']

    @property
    def _constructor(self):
        return LLogDataFrame

    @property
    def _constructor_sliced(self):
        print('fuck')
        return LLogSeries

    def pplot(self, *args, **kwargs):
        for c in self:
            self[c].pplot(*args, **kwargs)

# df = LLogDataFrame({1: [1,2], 1:[2,4], 3:[3,6]}, metadata, index=None)
df = LLogDataFrame({1: [1,2], 1:[2,4], 3:[3,6]}, index=None)
df = LLogDataFrame({1: [1,2], 2:[2,4], 3:[3,6]}, index=None)

dfmeta = {
    "llType": "data",
    "columns": [
        {"label": "gx", "style": "x-", "units": "C"},
        {"label": "gy", "units": "dps"},
        {"label": "gz", "style":"o", "color": "green", "units": "dps"}
    ]
}

df.meta = dfmeta

df2 = df[['gx', 'gy']]

df.pplot()
plt.show()
