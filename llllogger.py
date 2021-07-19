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
            setattr(self, llDesc['type'], DF[DF['llType'] == int(llType)])

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
# ax = df[['gx', 't']].plot()
# ax.set_ylabel(df['gx'].units)
# df[['gx', 'gy', 'gz']].plot(secondary_y=True, ax=ax)

# plt.show()