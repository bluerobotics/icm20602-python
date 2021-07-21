import pandas as pd
import llog

class LLogSeries(pd.Series):
    _metadata = ['metas']
    def __init__(self, meta):
        self.meta = meta
    # metas = 'boing'
    @property
    def _constructor(self):
        print('series fuck')
        return LLogSeries()
        # self.hello = 'goodbye'
        # return self
    @property
    def _constructor_expanddim(self):
        print('series fuck2')
        return LLogDataFrame
# https://stackoverflow.com/questions/48325859/subclass-pandas-dataframe-with-required-argument
class LLogDataFrame(pd.DataFrame):
    _metadata = ['metad']
    # metad = 'bingbong'
    @property
    def _constructor(self):
        print('dataframe fuck')
        return LLogDataFrame
    @property
    def _constructor_sliced(self):
        print('dataframe fuck2')
        return LLogSeries(self.meta)

a = LLogSeries(['a','a'], name='A')
b = LLogSeries(['b','b'], name='B')
c = LLogSeries(['c','c'], name='C')


a.metas = 'ameta'
b.metas = 'bmeta'
c.metas = 'cmeta'
df = LLogDataFrame({"one": a, "two":b, "three":c}, index=None)

print(f'ameta {a.metas}')
# df['one'].metas = 'test'
df['one'].metas = 'metasone'
print(f'ameta {df["one"].metas}')
df.metad = 'metadone'
df2 = df[['one','two']]
print(f'df2meta: {df2.metad}')
print(f'df2meta: {df2["one"].metas}')
