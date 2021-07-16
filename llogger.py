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

    
    def plot(self, name, y1, y2=None):
        df = self.dataByName(name)


        ax = df.plot(x='time', y=y1)
        cidx = df.columns.get_loc(y1[0])
        cmeta = self.metaByName(name)['columns'][cidx]
        clabel = f'{cmeta[0]} ({cmeta[1]})'
        ax.set_ylabel(clabel)
        ax.legend(loc="upper left")
        if y2 is not None:
            ax2 = ax.twinx()

            df.plot(x='time', y=y2, ax=ax2, cmap=plt.cm.get_cmap())
            cidx = df.columns.get_loc(y2[0])
            cmeta = self.metaByName(name)['columns'][cidx]
            clabel = f'{cmeta[0]} ({cmeta[1]})'
            ax2.set_ylabel(clabel)
            ax2.legend(loc="upper right")

    def scatter(self, name, y1, y2=None):

        colors = [
            "#FFA630",
            "#4DA1A9",
            "#611C35",
            "#2E5077",
            "#D7E8BA",
            ]
        markers = [
            '+',
            'x',
            'o',
            '*',
            '.',
        ]
        df = self.dataByName(name)
        meta = self.metaByName(name)
        if len(args):
            # this doesn't work for some reason, so the time needs to stay in it's own column
            # p = df.plot.scatter(x=df.index.to_list(), y=args[0], color=colors[0], marker=markers[0])

            arg = args[0]
            axn = None
            for data in arg:
                p = df.plot.scatter(x='time', y=data, color=colors[0], marker=markers[0], ax=axn)
                p = df.plot.scatter(x='time', y=data, color=colors[0], marker=markers[0], ax=axn)

                if axn is None:
                    print('axn')
                    axn = p.twinx()
            # p = df.plot.scatter(x='time', y=args[0], color=colors[0], marker=markers[0])

            n=1
            if len(args) > 1:
                for arg in args[1:]:
                    axn = p.twinx()
                    for data in arg:
                        df.plot.scatter(x='time', y=data, ax=axn, color=colors[n], marker=markers[n])
                        n += 1
        else:
            df.plot()



class LLogger():
    def __init__(self, categories, console=True, logfile=None):
        self.categories = categories
        self.logfile = logfile
        self.console = console

        if self.logfile:
            self.logfile = open(self.logfile, 'w')
            self.logfile.write(json.dumps(categories, indent=2, sort_keys=True, default=lambda o: '') + '\n')
    
    def log(self, type, data):
        t = time.time()
        try:
            category = self.categories[type]
        except Exception as e:
            raise e

        try:
            data = category['format'](data)
        except KeyError:
            pass

        logstring = f'{t:.6f} {type} {data}\n'
        if self.console:
            print(logstring, end='')
        if self.logfile:
            self.logfile.write(logstring)
        
    def close(self):
        if self.logfile:
            self.logfile.close()


# reader = LLogReader('/home/jacob/asdf')
# reader.plot('measurement', ['temperature'], ['temperature', 'pressure'])