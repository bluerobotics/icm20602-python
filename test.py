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

    def pplot(self, ll2=None, *args, **kwargs):
        print(f'sup {self.name}')

        columns = self.meta['columns']
        meta = {}
        for c in columns:
            print(c, self.name, c.get('llabel'))
            if self.name == c.get('llabel'):
                print('got', c)
                meta = c
                break
        # meta = self.meta[self.name]

        kwargs2 = kwargs | {'label': self.name}

        for opt in ["color", "style", "label"]:
            try:
                kwargs2 = kwargs2 | {opt:meta[opt]}
            except KeyError as e:
                # print(e)
                pass
        
        self.plot(*args, **kwargs2)
        plt.legend()
        plt.ylabel(meta.get('units'))

        if ll2 is not None:
            plt.twinx()
            ll2.pplot(*args, **kwargs)
        
    
# https://stackoverflow.com/questions/48325859/subclass-pandas-dataframe-with-required-argument
class LLogDataFrame(pd.DataFrame):
    _metadata = ['meta']

    def __init__(self, *args, **kwargs):
        # grab the keyword argument that is supposed to be my_attr
        self.meta = kwargs.pop('meta', None)

        super().__init__(*args, **kwargs)

        if self.meta is not None:
            # sometimes dataframe meta is not provided in intermediate operations
            # if self.meta is not None:
            columns = self.meta['columns']

            l = min(len(columns), len(self.columns)-2)

            print(l, len(columns), len(self),)
            for c in range(l):
                llabel = columns[c]['llabel']
                print(llabel)
                self.rename(columns={c+2:llabel}, inplace=True)
                # self[c+2].rename(llabel, inplace=True)

            print("hello", columns, self.columns, len(self), len(columns))
            for c in self.columns:
                print(self[c])

    @property
    def _constructor(self):
        def _c(*args, **kwargs):
            df = LLogDataFrame(*args, meta=self.meta, index=None, **kwargs)
            return df
        return _c
        
    @property
    def _constructor_sliced(self):
        print('ldsliced')
        return LLogSeries

    def pplot(self, d2=None, *args, **kwargs):
        for c in self:
            self[c].pplot(*args, **kwargs)
        # plot things on secondary axis
        if d2 is not None:
            plt.twinx()
            d2.pplot(*args, **kwargs)



# df = LLogDataFrame({1: [1,2], 1:[2,4], 3:[3,6]}, metadata, index=None)
dfmeta = {
    "llType": "data",
    "columns": [
        {"llabel": "gx", "style": "x-", "units": "C", "color": "black"},
        {"llabel": "gy", "units": "dps", "color": "red"},
        {"llabel": "gz", "style":"o", "color": "green", "units": "dps"}
    ]
}
df = LLogDataFrame({1: [1,2], 2:[2,4], 3:[3,6]}, meta=dfmeta, index=None)
df.pplot()
df.gx.pplot()
plt.show()
