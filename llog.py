#!/usr/bin/python3

import pandas as pd
import json
import time

LLOG_ERROR = '0'
# measurement data
LLOG_DATA = '1'
# read only memory + factory calibration and serialization type information
LLOG_ROM = '2'
# application-specific configuration information
LLOG_CONFIG = '3'
# calibration data
LLOG_CALIBRATION = '4'

# the fields that are expected to be present in metadata
llRequired = [
    'name'
]

llOptional = {
    #todo random
    'color': 'black',
    'marker': 'x',
    'marker_size': 2,
    'units': '',
    'dtype': float
}

# https://stackoverflow.com/questions/47466255/subclassing-a-pandas-dataframe-updates
class LLogSeries(pd.Series):
    _metadata = ['meta']

    @property
    def _constructor(self):
        print('lls constructor')
        return LLogSeries

    @property
    def _constructor_expanddim(self):
        print('lls constructor expand')
        return LLogDataFrame

    def plot(self, *args, **kwargs):
        print('plotnig', self.name, self.meta)
        for k,v in self.meta.items():
            print(f'{k}:{v}')
            # if v['name'] == self.name:
            #     self.meta = v
        # meta = self.meta[]
        # meta = self.meta

        # kwargs = meta|kwargs
        # ax = super().plot(*args, **kwargs)
        # ax.legend()

        # name = meta['name']
        # units = f' {meta["units"]}'
        # # color = f'{meta["color"]}'
        # # marker = f'{meta["marker"]}'

        # ax.set_ylabel(f'{name}{units}')
        # return ax

#llTypes must be unique
    
# https://stackoverflow.com/questions/48325859/subclass-pandas-dataframe-with-required-argument
class LLogDataFrame(pd.DataFrame):
    _metadata = ['meta']

    @property
    def _constructor(self):
        # def _c = 
        print('lld constructor')
        # print(f'meta {self.columns}')
        # return lambda o(): LLogDataFrame(columns=)

        # def _c(*args, **kwargs):
        #     # print(self.meta)
        #     # print([c for c in self.meta['columns']])

        #     print(kwargs)
        #     df = LLogDataFrame(*args, **kwargs)
        #     # print(df)
        #     # kwargs['columns'] = {i+2:self.meta['columns'][i]['name'] for i in range(len(self.meta['columns']))}
        #     # df = LLogDataFrame(*args, **kwargs)
        #     print(df)

        #     df.meta = self.meta
        #     c = {i+2:df.meta['columns'][i]['name'] for i in range(len(df.meta['columns']))}
        #     df.rename(columns=c, inplace=True)
        #     # columns = {i:c['name'] for c in self.meta[columns]}
        #     # df.rename(columns=columns, inplace=True)
        #     # l = min(len(columns), len(value.columns)-2)

        #     # # rename columns
        #     # for c in range(l):
        #     #     i = c + 2
        #     #     name = columns[c]['name']
        #     #     df.rename(columns=columns, inplace=True)
        #     return df
        # return _c

        return LLogDataFrame

    @property
    def _constructor_sliced(self):
        print('lld constructor_sliced')
        # print(self.meta)
        # def _c(*args, **kwargs):
            
        #     s = LLogSeries(*args, **kwargs)
        #     try:
        #         print(kwargs)
        #         name = kwargs['name']
        #         print(f'set series meta {name} to {meta}')
        #         meta = self.meta[name]
        #         s.meta = meta
        #     except:
        #         print(f'failure setting series meta {name} {self.meta}')
        #         pass
        #     return s
        # return _c

        # def _c(*args, **kwargs):
        #     s = LLogSeries(*args, **kwargs)
        #     try:
        #         print(kwargs)
        #         name = kwargs['name']
        #         print(f'set series meta {name} to {meta}')
        #         meta = self.meta[name]
        #         s.meta = meta
        #     except:
        #         print(f'failure setting series meta {name} {self.meta}')
        #         pass
        #     return s
        # return _c
        return LLogSeries

    def plot(self, *args, **kwargs):
        for c in self:
            self[c].plot(*args, **kwargs)

# # https://pandas.pydata.org/pandas-docs/stable/development/extending.html
# @pd.api.extensions.register_series_accessor("ll")
# class LLAxis:
#     def __init__(self, pandas_obj):
#         print(f'LL: {pandas_obj.attrs}')
#         self._obj = pandas_obj
#         self.meta = self._obj.attrs['llMeta']

#     def plot(self, **kwargs):
#         meta = self._obj.attrs['llMeta']
#         name = meta['name']
#         units = f' {meta["units"]}'
#         color = f'{meta["color"]}'
#         marker = f'{meta["marker"]}'

#         ax = self._obj.plot(c=color, style=marker, markersize=2, **kwargs)
#         ax.legend()
#         ax.set_ylabel(f'{name}{units}')
#         return ax

#     def pplot(self, y2=None):
#         ax = self.plot()
#         if y2 is not None:
#             y2.ll.plot(ax)
#         return ax

#     def ppplot(self):
#         return self._obj

# @pd.api.extensions.register_dataframe_accessor("ll")
# class LLDataFrame:
#     def __init__(self, pandas_obj):
#         print(f'DF: {pandas_obj["pressure"].attrs}')
#         self._obj = pandas_obj
#         print(f'DF: {pandas_obj["pressure"].attrs}')
#         print(f'DF: {self._obj["pressure"].attrs}')



#     def plot(self, **kwargs):
#         print(f'DFTIME: {self._obj["time"].attrs}')
#         for c, s in self._obj.iteritems():

#             # don't process these
#             if c in ['time', 'llType']:
#                 continue

#             print(f'DF: {c}, {s.attrs}')
#             s.ll.plot(**kwargs)
#             # print(f'DF: {self._obj.pressure.attrs}')
#             # print(f'DF: {self._obj[c].attrs}')
#             # print(f'DF: {self._obj.pressure.attrs}')
#             # self._obj[c].ll.plot(kwargs)


# @pd.api.extensions.register_dataframe_accessor("pdf")
# class LLPdf:
#     def __init__(self, pandas_obj):
#         self._obj = pandas_obj
#         self.pdf = 
#     def header(self):
#         return 'llog v0.0.1 pdf'


#     def addfig(self, fig, w, h):
#         pdf.cell(w, h, f'{w} {h}')
#         # if y1 is None:
#         #     #plot the dataframe
#         for y in y1:
#             ax = self._obj[y].ll.plot()
#         for y in y2:
#             self._obj[y].ll.plot(ax=ax)
#         return ax

# class LLogSeries(pd.Series):
    
#     _metadata = ['llMeta']

#     @property
#     def _constructor(self):
#         self.llMeta = { 'a': 'aasdf', 'b': ';aklj'}
#         print(self.llMeta)
#         return LLogSeries

#     def me(self):
#         print('hello')
        
# class LLogDataframe(pd.Dataframe):
    

class LLogReader:
    def __init__(self, logfile, metafile):
        # self.meta = self.metaOpen(metafile)
        self.df = self.logOpen(logfile)
        
        self.meta = self.metaOpen(metafile)
        # self.df.meta = self.metaOpen(metafile)

        self.df.rename(columns={0:'time', 1:'llKey'}, inplace=True)
        self.df['llKey'] = self.df['llKey'].astype(int)

        # for llType, llDesc in self.meta.items():
        #     DF = self.df

        #     attr = llDesc['type']
        #     value = DF[DF['llType'] == int(llType)].dropna(axis='columns', how='all')

        #     try:
        #         columns = llDesc['columns']
        #         l = min(len(columns), len(value.columns)-2)

        #         # rename columns
        #         for c in range(l):
        #             i = c + 2
        #             name = columns[c]['name']
        #             value.rename(columns={i: name}, inplace=True)
        #     except:
        #         pass
        # #         # convert field type
        #         for c in range(l):
        #             name = columns[c]['name']
        #             try:
        #                 dtype = columns[c]['dtype']
        #                 print('dtype is', dtype, type(dtype), dtype=="int")
        #                 if dtype == "int":
        #                     value[name] = value[name].astype(int)
        #                 elif dtype == "float":
        #                     value[name] = value[name].astype(float)
        #             except KeyError:
        #                 try:
        #                     value[name] = value[name].astype(float)
        #                 except:
        #                     pass

        #         # # attach metadata !! this must be done last
        #         # for c in range(l):
        #         #     name = columns[c]['name']
        #         #     value[name].attrs['llMeta'] = llOptional | columns[c]

        #     except ValueError:
        #         print(f'{attr} could not convert string to float')
        #         pass
        #     except KeyError:
        #         print(f'{attr} does not have columns definition')
        #         pass
        # for llType, llDesc in self.meta.items():
        #     DF = self.df

        #     attr = llDesc['type']
        #     value = DF[DF['llType'] == int(llType)].dropna(axis='columns', how='all')

            # eg for each type name in log, set self.type to
            # the dataframe representing only that type
            # setattr(self, attr, value)





        

        for llKey, llDesc in self.meta.items():
            DF = self.df

            value = DF[DF['llKey'] == int(llKey)].dropna(axis='columns', how='all')

            # eg for each type name in log, set self.type to
            # the dataframe representing only that type
            print(llKey, llDesc)
            try:

                c = {i+2:llDesc['columns'][i]['name'] for i in range(len(llDesc['columns']))}
            except:
                c = {}
            value = LLogDataFrame(value)
            value.meta = llDesc
            value.rename(columns=c, inplace=True)


            llType = llDesc['type']


            # create LLDF..
            setattr(self, llType, value)

    def metaOpen(self, metafile):
        with open(metafile, 'r') as f:
            return json.load(f)
    
    def logOpen(self, logfile):
        return pd.read_csv(logfile,sep=' ', header=None).dropna(axis='columns', how='all').set_index(0, drop=False)
        # df = pd.read_csv(logfile,sep=' ', header=None).dropna(axis='columns', how='all').set_index(0, drop=False)
        # return LLogDataFrame(df)

class LLogWriter:
    def __init__(self, meta, logfile=None, console=True):
        self.meta = self.metaOpen(meta)
        self.logfile = logfile
        self.console = console

        if self.logfile:
            self.logfile = open(self.logfile, 'w')

    def log(self, type, data):
        t = time.time()
        try:
            llType = self.meta[type]
        except Exception as e:
            raise e

        logstring = f'{t:.6f} {type} {data}\n'
        if self.console:
            print(logstring, end='')
        if self.logfile:
            self.logfile.write(logstring)
        
    def close(self):
        if self.logfile:
            self.logfile.close()

    def metaOpen(self, metafile):
        with open(metafile, 'r') as f:
            return json.load(f)
