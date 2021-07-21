import pandas as pd
import llog

# https://stackoverflow.com/questions/47466255/subclassing-a-pandas-dataframe-updates
class LLogSeries(pd.Series):
    _metadata = ['metas']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
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
        # return LLogDataFrame._internal_ctor

    # @classmethod
    # def _internal_ctor(cls, *args, **kwargs):
    #     kwargs['meta'] = None
    #     return cls(*args, **kwargs)


    @property
    def _constructor_sliced(self):
        def _c(*args, **kwargs):
            print('dataframe fuck2', args, kwargs)

            name = kwargs['name']

            meta = self.metad[name]
            a = LLogSeries(*args, **kwargs)
            a.metas = meta
            return a

        return _c

a = LLogSeries(['a','a'], name='A')
b = LLogSeries(['b','b'], name='B')
c = LLogSeries(['c','c'], name='C')


a.metas = 'ameta'
b.metas = 'bmeta'
c.metas = 'cmeta'
dfmeta = {
    "one": "metaone",
    "two": "metatwo",
    "three": "metathree",
}
df = LLogDataFrame({"one": a, "two":b, "three":c}, index=None)

df.metad = dfmeta

print(f'ameta {df["one"].metas}')
df2 = df[['one','two']]
print(f'df2meta: {df2.metad}')
print(f'df2meta: {df2["one"].metas}')
