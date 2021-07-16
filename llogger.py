#!/usr/bin/python3

import csv
import matplotlib.pyplot as plt
import pandas as pd
import json
import time
from io import StringIO

class LLogReader():
    def __init__(self, logfile):

        with open(logfile, newline='') as f:
            data = f.read()

            try:
                self.metadata = json.loads(data)
            except json.decoder.JSONDecodeError as e:
                # print(e.msg, e.pos, e.doc)
                import re
                # self.metadata = json.loads(data[:int(re.findall('char (d+)', e.pos)[0])])
                self.metadata = json.loads(data[:e.pos])
                self.data = data[e.pos:]
            
            print('available types:', self.metaNames())

            sio = StringIO(self.data)
            # self.df = pd.read_csv(sio, sep=' ', header=None, index_col=0)
            self.df = pd.read_csv(sio, sep=' ', header=None)

            self.df.rename(columns={0: 'time', 1: 'logtype'}, inplace=True)

            # self.df.index = pd.DatetimeIndex(self.df.index)


            # self.df.index = pd.to_datetime(self.df.index, unit='s')
            # self.df.index.name = 'time'

    def metaKeys(self):
        return self.metadata.keys()

    def metaNames(self):
        return [self.metadata[key]['name'] for key in self.metadata.keys()]

    def metaName2Key(self, name):
        for key in self.metaKeys():
            if name == self.metadata[key]['name']:
                return key
        raise KeyError

    def metaByName(self, name):
        return self.metadata[self.metaName2Key(name)]

    def dataByKey(self, key):
        df = self.df[self.df['logtype'] == int(key)]
        columns = self.metadata[key]['columns']

        # transform our tuple list into a dictionary for pandas df.rename
        ccolumns = {}
        for i in range(len(columns)):
            ccolumns[i+2] = columns[i][0]
        
        # https://stackoverflow.com/a/31495326
        return df.rename(columns=ccolumns).dropna(axis='columns').astype(float)

    def dataByName(self, name):

        return self.dataByKey(self.metaName2Key(name))

    
    def plot(self, name, y1, y2=None, kind='plot'):
        df = self.dataByName(name)

        ax = plt.gca()

        ax = df.plot(x='time', y=y1, marker='x', markersize=2)
        # for y in y1:
        #     ax.plot(kind=kind, x='time', y=y)
        cidx = df.columns.get_loc(y1[0])
        cmeta = self.metaByName(name)['columns'][cidx]
        clabel = f'{cmeta[0]} ({cmeta[1]})'
        ax.set_ylabel(clabel)
        ax.legend(loc="upper left")
        if y2 is not None:
            ax2 = ax.twinx()

            df.plot(x='time', y=y2, marker='x', markersize=2, ax=ax2, cmap=plt.cm.get_cmap())
            cidx = df.columns.get_loc(y2[0])
            cmeta = self.metaByName(name)['columns'][cidx]
            clabel = f'{cmeta[0]} ({cmeta[1]})'
            ax2.set_ylabel(clabel)
            ax2.legend(loc="upper right")

# reader = LLogReader('/home/jacob/asdf')
# reader.plot('measurement', ['temperature'], ['temperature', 'pressure'])