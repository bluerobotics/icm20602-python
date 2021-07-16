#!/usr/bin/python3

from dataclasses import dataclass
import csv
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

class LLogReader:
    def __init__(self, logfile):
            self.header, self.data = self.open(logfile)

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
            header = LLogDesc(headerData)
            data = f.read()

        sio = StringIO(data)
        # print('hello?', sio.readline())
        print('fuck')
        print(data)
        # holy shit this doesn't work if the number is not an epoch timestamp
        df = pd.read_csv(sio, sep=' ', header=None, error_bad_lines=False)

        print(df)
        self.df = df
        # print('ffuck')
        # print(data)
        # print(df)
        # print(header)
        return (header, data) 

l = LLogDesc('hello')
ll = LLogReader('bme.csv')