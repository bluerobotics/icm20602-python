#!/usr/bin/python3

import pandas as pd
import json
import time

LLOG_ERROR = '0'
# read only memory + factory calibration and serialization type information
LLOG_ROM = '1'
# application-specific configuration information
LLOG_CONFIG = '2'
# measurement data
LLOG_DATA = '4'
# calibration data
LLOG_CALIBRATION = '5'

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

# https://pandas.pydata.org/pandas-docs/stable/development/extending.html
@pd.api.extensions.register_series_accessor("ll")
class LLAxis:
    def __init__(self, pandas_obj):
        print(f'LL: {pandas_obj.attrs}')
        self._obj = pandas_obj
        self.meta = self._obj.attrs['llMeta']

    def plot(self, **kwargs):
        meta = self._obj.attrs['llMeta']
        name = meta['name']
        units = f' {meta["units"]}'
        color = f'{meta["color"]}'
        marker = f'{meta["marker"]}'

        ax = self._obj.plot(c=color, style=marker, markersize=2, **kwargs)
        ax.legend()
        ax.set_ylabel(f'{name}{units}')
        return ax

    def pplot(self, y2=None):
        ax = self.plot()
        if y2 is not None:
            y2.ll.plot(ax)
        return ax

    def ppplot(self):
        return self._obj

@pd.api.extensions.register_dataframe_accessor("ll")
class LLDataFrame:
    def __init__(self, pandas_obj):
        print(f'DF: {pandas_obj["pressure"].attrs}')
        self._obj = pandas_obj
        print(f'DF: {pandas_obj["pressure"].attrs}')
        print(f'DF: {self._obj["pressure"].attrs}')



    def plot(self, **kwargs):
        print(f'DFTIME: {self._obj["time"].attrs}')
        for c, s in self._obj.iteritems():

            # don't process these
            if c in ['time', 'llType']:
                continue

            print(f'DF: {c}, {s.attrs}')
            s.ll.plot(**kwargs)
            # print(f'DF: {self._obj.pressure.attrs}')
            # print(f'DF: {self._obj[c].attrs}')
            # print(f'DF: {self._obj.pressure.attrs}')
            # self._obj[c].ll.plot(kwargs)


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

class LLogReader:
    def __init__(self, logfile, metafile):
        self.meta = self.metaOpen(metafile)
        self.df = self.logOpen(logfile)
        self.df.rename(columns={0:'time', 1:'llType'}, inplace=True)
        self.df['llType'] = self.df['llType'].astype(int)

        for llType, llDesc in self.meta.items():
            DF = self.df

            attr = llDesc['type']
            value = DF[DF['llType'] == int(llType)].dropna(axis='columns', how='all')

            try:
                columns = llDesc['columns']
                l = min(len(columns), len(value.columns)-2)

                # rename columns
                for c in range(l):
                    i = c + 2
                    name = columns[c]['name']
                    value.rename(columns={i: name}, inplace=True)

                # convert field type
                for c in range(l):
                    name = columns[c]['name']
                    try:
                        dtype = columns[c]['dtype']
                        print('dtype is', dtype, type(dtype), dtype=="int")
                        if dtype == "int":
                            value[name] = value[name].astype(int)
                        elif dtype == "float":
                            value[name] = value[name].astype(float)
                    except KeyError:
                        try:
                            value[name] = value[name].astype(float)
                        except:
                            pass

                # attach metadata !! this must be done last
                for c in range(l):
                    name = columns[c]['name']
                    value[name].attrs['llMeta'] = llOptional | columns[c]

            except ValueError:
                print(f'{attr} could not convert string to float')
                pass
            except KeyError:
                print(f'{attr} does not have columns definition')
                pass

            # eg for each type name in log, set self.type to
            # the dataframe representing only that type
            setattr(self, attr, value)

    def metaOpen(self, metafile):
        with open(metafile, 'r') as f:
            return json.load(f)
    
    def logOpen(self, logfile):
        return pd.read_csv(logfile,sep=' ', header=None).dropna(axis='columns', how='all').set_index(0, drop=False)

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
