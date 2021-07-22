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

        # print(self.index.get_loc(self.name))
        meta = self.meta[self.name]
        
        kwargs2 = kwargs | {'label': self.name}

        for opt in ["color", "style", "label"]:
            try:
                kwargs2 = kwargs2 | {opt:meta[opt]}
            except KeyError as e:
                # print(e)
                pass

        self.plot(*args, **kwargs2)
        plt.legend()
        plt.ylabel(meta['units'])

        if ll2 is not None:
            plt.twinx()
            ll2.pplot(*args, **kwargs)
        
    
# https://stackoverflow.com/questions/48325859/subclass-pandas-dataframe-with-required-argument
class LLogDataFrame(pd.DataFrame):
    _metadata = ['meta']


    def __init__(self, *args, **kwargs):
        # grab the keyword argument that is supposed to be my_attr
        self.meta = kwargs.pop('meta', None)
        columns = self.meta['columns']

        # ########
        # put this stuf after super.init!
        # for c in df[1:]:
        # #     print(c)
        # l = min(len(columns), len(self)-2)

        # for c in range(l):
        #     llabel = columns[i]['llabel']
        #     print(llabel, self[c], self[c+2])
        #     self[c+2].rename(llabel, inplace=True)

            # value.rename(columns={i+2: name}, inplace=True)
            # value[name].llSeriesMeta = columns[i]
            # print(f'!!!! {i} {value[name].llSeriesMeta}')
        super().__init__(*args, **kwargs)
        print("hello", columns, self.columns)
        for c in self.columns:
            print(self[c])

    # @propertydf
    # def _constructor(self):
    #     return LLogDataFrame


    @property
    def _constructor(self):
        """This is the key to letting Pandas know how to keep
        derivative `SomeData` the same type as yours.  It should
        be enough to return the name of the Class.  However, in
        some cases, `__finalize__` is not called and `my_attr` is
        not carried over.  We can fix that by constructing a callable
        that makes sure to call `__finlaize__` every time."""
        def _c(*args, **kwargs):

            # a = LLogDataFrame(*args, **kwargs).__finalize__(self)
            a = LLogDataFrame(*args, meta=self.meta, **kwargs)
            print('fffuck')
            print(len(a.columns))
            # for c in a:
            #     a[c].rename()
            # a.rename(...)
            return a

        return _c
        
    @property
    def _constructor_sliced(self):
        print('fuck')
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
        {"llabel": "gx", "style": "x-", "units": "C"},
        {"llabel": "gy", "units": "dps"},
        {"llabel": "gz", "style":"o", "color": "green", "units": "dps"}
    ]
}
df = LLogDataFrame({1: [1,2], 2:[2,4], 3:[3,6]}, meta=dfmeta, index=None)

# dfmeta = {
#     "llType": "data",
#     "columns": [
#         {"label": "gx", "style": "x-", "units": "C"},
#         {"label": "gy", "units": "dps"},
#         {"label": "gz", "style":"o", "color": "green", "units": "dps"}
#     ]
# }

# df.meta = dfmeta

# df2 = df[['gx', 'gy']]

# df.pplot()
# plt.show()
