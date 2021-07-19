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

# class LLAxis:
@pd.api.extensions.register_series_accessor("ll")
class LLAxis:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def plot(self, ax=None):
        meta = pressure.attrs['llMeta']


        name = meta['name']
        units = meta['units']
        color = meta['color']
        marker = meta['marker']
        if ax is None:

            ax = self._obj.plot(c=color, marker=marker)

        else:
            ax = self._obj.plot(c=color, marker=marker, secondary_y=True, mark_right=False, ax=ax)
        ax.set_ylabel(f'{name} ({units})')
        return ax
    # def subplot(self, ax):
    #     meta = pressure.attrs['llMeta']


    #     name = meta['name']
    #     units = meta['units']
    #     color = meta['color']
    #     marker = meta['marker']
    #     ax = self._obj.plot(c=color, marker=marker)
    #     ax.set_ylabel(f'{name} ({units})')




# frozen (read only)?
@dataclass
class LLogDesc:
    data: typing.TextIO

    def __post_init__(self):
        print(self.data)
        setattr(self, 'n', 2)
        self.df = pd.read_csv(self.data, sep=',', header=None)


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
                    value[name].attrs['llMeta'] = columns[c]
                
            
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
        
    def metaByName(self, name):
        pass

    def dfByName(self, name):
        pass


ll = LLogReader('bme.csv', 'bme.meta')
# df = ll.dfByName('data')

data = ll.data
pressure = data.pressure

meta = pressure.attrs['llMeta']
name = meta['name']
units = meta['units']
color = meta['color']
marker = meta['marker']


# data.plot()
ax = pressure.plot(c=color)
ax.set_ylabel(f'{name} ({units})')

# https://pandas.pydata.org/pandas-docs/stable/development/extending.html
temperature = data.temperature

meta = temperature.attrs['llMeta']
name = meta['name']
units = meta['units']
color = meta['color']
marker = meta['marker']
ax2 = temperature.plot(c=color, secondary_y=True, mark_right=False)
ax2.set_ylabel(f'{name} ({units})')

plt.show()

print(temperature)


# ax = df[['gx', 't']].plot()
# ax.set_ylabel(df['gx'].units)
# df[['gx', 'gy', 'gz']].plot(secondary_y=True, ax=ax)

# plt.show()