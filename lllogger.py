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

# frozen (read only)?
@dataclass
class LLogDesc:
    data: typing.TextIO

    def __post_init__(self):
        print(self.data)
        setattr(self, 'n', 2)
        self.df = pd.read_csv(self.data, sep=',', header=None)

class LLa:
    pass

class LLogReader:
    def __init__(self, logfile):
            self.meta, self.df = self.open(logfile)

    def open(self, path):
        headerData = None
        headerInfo = '### llog v0.0.1 ###\n'
        with open(path) as f:
            if f.readline() == headerInfo:
                headerData = ''
                line = f.readline()
                while line:
                    if line == headerInfo:
                        break
                    headerData += line
                    line = f.readline()
            data = f.read()

        sio = StringIO(headerData)
        # header = LLogDesc(sio)
        print("!!!!!")
        print(headerData)
        headerDf = pd.read_csv(sio, sep=',', header=None)
        # drop the first row (empty placeholder values to set the width of the dataframe)
        print(headerDf)
        print("!!!!!")

        headerDf.drop(index=0, inplace=True)

        # convert our ints back to ints
        headerDf[0] = headerDf[0].astype(int)
        
        meta = {}
        for type in headerDf[0].unique():
            df = headerDf[headerDf[0] == type]
            # metaOb = LLa
            # setattr(metaOb, 'llogType', type)

            metaOb = {}

            for m in df.itertuples():
                name = m[2]
                value = m[3:]
                metaOb[name] = value
                # # setattr(metaOb, str(m[1]), m[2:])
                # print(metaOb)
                meta[type] = metaOb


        print(meta)


        # # print('hello?', sio.readline())
        # print('fuck')
        # print(data)
        # # holy shit this doesn't work if the number is not an epoch timestamp
        # df = pd.read_csv(sio, sep=' ', header=None, error_bad_lines=False)

        sio = StringIO(data)
        df = pd.read_csv(sio, sep=',', header=None, index_col=False, engine='python')
        df.drop(index=0, inplace=True)

        # convert our ints back to ints
        df[1] = df[1].astype(int)
        # print(df)
        # self.df = df
        # print('ffuck')
        # print(data)
        # print(df)
        # print(header)
        return (meta, df)

    def dfByName(self, name):
        for key,value in self.meta.items():
            # try:...
            if(value['type'][0] == name):
                df = self.df[self.df[1] == key]

                # df.rename(mapper=lambda i: value['label'][i-2], axis='columns')
                #todo omit type
                for key, value in value.items():
                    for c in df.loc[:, 2:]:
                        # we subtract 2, timestamp and type
                        # this is the column name/index
                        c = c-2
                        print(f'adding key {key} to {c}')
                        # df[c][key] = value[c]
                        if key == 'name':
                            ccolumns = {}
                            print(value)
                            for i in range(len(value)):
                                print(i)
                                ccolumns[i+2] = value[i]
                            # df.rename(columns={c+2:value[c]}, inplace=True)
                        else:
                            setattr(df[c], key, value[c])
                return df.rename(columns=ccolumns).dropna(axis='columns').astype(float)
    # def plot(self, x1, y1, y2=None):


ll = LLogReader('bme.csv')
df = ll.dfByName('data')
ax = df[['gx', 't']].plot()
df[['gx', 'gy', 'gz']].plot(secondary_y=True, ax=ax)
plt.show()