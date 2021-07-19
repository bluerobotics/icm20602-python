#!/usr/bin/python3

from dataclasses import dataclass
import csv
from collections import namedtuple
import matplotlib.pyplot as plt
import pandas as pd
import json
import time
import typing
from io import StringIO

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
# class LLAxis:
# https://pandas.pydata.org/pandas-docs/stable/development/extending.html
@pd.api.extensions.register_series_accessor("ll")
class LLAxis:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def plot(self, ax=None):
        meta = self._obj.attrs['llMeta']
        name = meta['name']
        units = f' {meta["units"]}'
        color = f'{meta["color"]}'
        marker = f'{meta["marker"]}'

        if ax is None:
            ax = self._obj.plot(c=color, marker=marker)
        else:
            ax = self._obj.plot(c=color, marker=marker, secondary_y=True, mark_right=False, ax=ax)
        ax.set_ylabel(f'{name}{units}')
        return ax

class LLogReader:
    def __init__(self, logfile, metafile):
        self.meta = self.metaOpen(metafile)
        self.df = self.logOpen(logfile)
        self.df.rename(columns={0:'time', 1:'llType'}, inplace=True)
        self.df['llType'] = self.df['llType'].astype(int)

        for llType, llDesc in self.meta.items():
            # find matching rows
            # create new view
            # todo make it a dataframe
            DF = self.df

            attr = llDesc['type']
            value = DF[DF['llType'] == int(llType)].dropna(axis='columns', how='all')

            try:
                columns = llDesc['columns']
                for c in range(len(columns)):
                    i = c + 2
                    print(f'renaming {i}, {columns[c]["name"]}')
                    name = columns[c]['name']
                    value.rename(columns={i: name}, inplace=True)
                # convert numeric fields to float
                for c in range(len(columns)):
                    name = columns[c]['name']
                    value[name] = value[name].astype(float)

                # attach metadata !! this must be done last
                for c in range(len(columns)):
                    name = columns[c]['name']
                    value[name].attrs['llMeta'] = llOptional | columns[c]

            except ValueError:
                # 'could not convert stringt o flouat'
                print(f'{attr} could not convert string to float')
                pass
            except KeyError:
                print(f'{attr} does not have columns definition')

            # eg for each type name in log, set self.type to
            # the dataframe representing only that type
            print(f'setting {attr} to \n{value}')
            setattr(self, attr, value)

    def metaOpen(self, metafile):
        print(metafile)
        with open(metafile, 'r') as f:
            return json.load(f)
    
    def logOpen(self, logfile):
        return pd.read_csv(logfile,sep=',', header=None).drop(index=0).dropna(axis='columns', how='all')


ll = LLogReader('bme.csv', 'bme.meta')

data = ll.data
pressure = data.pressure
temperature = data.temperature

ax = pressure.ll.plot()
data.pressure_raw.ll.plot()
temperature.ll.plot(ax)

plt.figure()
temperature.ll.plot()

plt.show()
