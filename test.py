import matplotlib.pyplot as plt
import pandas as pd
import llog

# https://stackoverflow.com/questions/47466255/subclassing-a-pandas-dataframe-updates
# https://stackoverflow.com/questions/47466255/subclassing-a-pandas-dataframe-updates
class LLogSeries(pd.Series):
    _metadata = ['meta']

    @property
    def _constructor(self):
        # def _c(*args, **kwargs):
        #     print(f'lls constructor self{args} {kwargs.keys()}')
        #     return LLogSeries


        # return _c
        return LLogSeries

    @property
    def _constructor_expanddim(self):
        return LLogDataFrame

    def pplot(self, *args, **kwargs):
        print('asdfasdf')
        print('plotting', self.name, kwargs)

        try:
            meta = self.meta[self.name]
            print(f'got meta {meta}')
            kwargs = kwargs | meta
        except Exception as e:
            print(e)
        
        ax = super().plot(*args, **kwargs)
        ax.legend()

        # name = meta['name']
        # units = f' {meta["units"]}'
        # # color = f'{meta["color"]}'
        # # marker = f'{meta["marker"]}'

        # ax.set_ylabel(f'{name}{units}')
        # return ax

    
# https://stackoverflow.com/questions/48325859/subclass-pandas-dataframe-with-required-argument
class LLogDataFrame(pd.DataFrame):
    _metadata = ['meta']

    @property
    def _constructor(self):
        return LLogDataFrame

    @property
    def _constructor_sliced(self):
        return LLogSeries
        # def _c(*args, **kwargs):
        #     s = LLogSeries(*args, **kwargs)
        #     try:
        #         name = kwargs['name']
        #         meta = self.meta[name]
        #         s.smeta = meta
        #     except Exception as e:
        #         print(e)
        #         pass
        #     return s
        # return _c

    def pplot(self, *args, **kwargs):

        for c in self:
            print(f'plotting {c}')
            self[c].pplot(*args, **kwargs)
# a = LLogSeries(['a','a'], name='A')
# b = LLogSeries(['b','b'], name='B')
# c = LLogSeries(['c','c'], name='C')

# 
# a.metas = 'ameta'
# b.metas = 'bmeta'
# c.metas = 'cmeta'
dfmeta = {
    "one": "metaone",
    "two": "metatwo",
    "three": "metathree",
}
# df = LLogDataFrame({"one": a, "two":b, "three":c}, index=None)
df = LLogDataFrame({"one": [1,2], "two":[2,4], "three":[3,6]}, index=None)

df.meta = dfmeta

print(f'ameta {df["one"].meta}')
df2 = df[['one','two']]
print(f'df2meta: {df2.meta}')
print(f'df2meta: {df2["one"].meta}')

# df2['one'].plot()
df2.plot()
