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
        sio.readline()
        print('fuck')
        print(data)
        df = pd.read_csv(sio, header=None, sep=',')

        print(df)
        # print('ffuck')
        # print(data)
        # print(df)
        # print(header)
        return (header, data) 

l = LLogDesc('hello')
ll = LLogReader('bme.csv')