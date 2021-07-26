#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import json
import time

# https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#custom-describe
from functools import partial

q_25 = partial(pd.Series.quantile, q=0.25)
q_25.name = "25%"
q_75 = partial(pd.Series.quantile, q=0.75)
q_75.name = "75%"

LLOG_ERROR = '0'
# measurement data
LLOG_DATA = '1'
# application-specific configuration information
LLOG_CONFIG = '2'
# calibration data
LLOG_CALIBRATION = '4'
# read only memory + factory calibration and serialization type information
LLOG_ROM = '5'
# information/notes
LLOG_INFO = '6'
LLOG_NONE= '666'

# https://stackoverflow.com/questions/47466255/subclassing-a-pandas-dataframe-updates
class LLogSeries(pd.Series):
    _metadata = ['meta']

    @property
    def _constructor(self):
        return LLogSeries

    @property
    def _constructor_expanddim(self):
        return LLogDataFrame

    def pplot(self, d2=None, *args, **kwargs):
        columns = self.meta['columns']
        meta = {}
        for c in columns:
            if self.name == c.get('llabel'):
                meta = c
                break

        kwargs2 = kwargs | {'label': self.name}

        for opt in ["color", "style", "label", "colormap"]:
            try:
                kwargs2 = kwargs2 | {opt:meta[opt]}
            except KeyError as e:
                # print(e)
                pass
        
        self.plot(*args, **kwargs2)
        plt.legend()
        plt.ylabel(meta.get('units'))

        if d2 is not None:
            plt.twinx()
            d2.pplot(*args, **kwargs)
        
        plt.grid(True)
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.5, hspace=0.5)

    def stats(self):
        return self.agg(["count", "mean", "std", "min", q_25, "median", q_75, "max"])
        

# https://stackoverflow.com/questions/48325859/subclass-pandas-dataframe-with-required-argument
class LLogDataFrame(pd.DataFrame):
    _metadata = ['meta']

    def __init__(self, *args, **kwargs):
        self.meta = kwargs.pop('meta', None)
        super().__init__(*args, **kwargs)

        # sometimes dataframe meta is not provided in intermediate operations
        # so we need to check if self.meta exists
        # rename column index labels, and change column
        # series types according to metadata
        if self.meta is not None:
            columns = self.meta.get('columns', [])
            l = min(len(columns), len(self.columns)-2)
            for c in range(l):
                try:
                    dtype = columns[c]['dtype']
                    i = c+2
                    if dtype == "int":
                        self[i] = self[i].astype(int)

                    elif dtype == "float":
                        self[i] = self[i].astype(float)

                except KeyError as e:
                    try:
                        self[i] = self[i].astype(float)
                    except Exception as e:
                        pass
                llabel = columns[c]['llabel']
                self.rename(columns={c+2:llabel}, inplace=True)
                # self[c+2].rename(llabel, inplace=True)

    @property
    def _constructor(self):
        def _c(*args, **kwargs):
            df = LLogDataFrame(*args, meta=self.meta, **kwargs)
            return df
        return _c
        
    @property
    def _constructor_sliced(self):
        return LLogSeries

    def pplot(self, *args, **kwargs):
        d2 = kwargs.pop('d2', None)
        for c in self:
            self[c].pplot(*args, **kwargs)
        # plot d2 dataframe on secondary axis
        if d2 is not None:
            plt.twinx()
            d2.pplot(*args, **kwargs)

    def table(self, rl=False, *args, **kwargs):
        if rl is True:
            kwargs['rowLabels'] = self.index
        plt.table(cellText=self.to_numpy(dtype=str), colLabels=self.columns, loc='bottom', cellLoc='center', bbox=[0,0,1,1], *args, **kwargs)
        plt.axis('off')
        plt.title(self.meta['llType'])
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.5, hspace=0.5)

    def stats(self):
        stats = self.agg(["count", "mean", "std", "min", q_25, "median", q_75, "max"])
        return LLogDataFrame(stats, meta=self.meta)


class LLogReader:
    def __init__(self, logfile, metafile):
        self.df = pd.read_csv(logfile, sep=' ', header=None).dropna(axis='columns', how='all').set_index(0, drop=False)
        with open(metafile, 'r') as f:
            self.meta = json.load(f)

        # todo move this to LLogDataFrame constructor
        # or remove these columns from the logdataframe completely
        self.df.rename(columns={0:'time', 1:'llKey'}, inplace=True)
        self.df['llKey'] = self.df['llKey'].astype(int)

        for llKey, llDesc in self.meta.items():
            DF = self.df
            value = DF[DF['llKey'] == int(llKey)].dropna(axis='columns', how='all')
            # eg for each llType name in log, set self.type to
            # the dataframe representing only that type
            value = LLogDataFrame(value, meta=llDesc)
            llType = llDesc['llType']
            setattr(self, llType, value)

    def figure(self, height_ratios=[1,4,4], columns=2, suptitle='', header='', footer=''):
        f = plt.figure(suptitle, figsize=(8.5, 11.0))
        plt.suptitle(suptitle)
        footer_buffer_ratio = sum(height_ratios) * 0.02
        height_ratios.append(footer_buffer_ratio)
        rows = len(height_ratios)
        spec = f.add_gridspec(rows, columns, height_ratios=height_ratios)
        f.text(0.98, 0.98, header, size=8, horizontalalignment='right', verticalalignment='bottom')
        f.text(0.98, 0.02, footer, size=8, horizontalalignment='right')
        
        # add a line, using our footer buffer subplot (the line is plotted in figure coords)
        f.add_subplot(spec[-1,:])
        plt.plot([0.35, 0.65], [0.02, 0.02], color='#2c99ce', lw=3, clip_on=False, transform=f.transFigure)
        plt.axis('off')

        # add br logo image
        im = plt.imread('br.png')
        f.figimage(im, 2, 2)
        return f, spec


class LLogWriter:
    def __init__(self, metafile, logfile=None, console=True):
        with open(metafile, 'r') as f:
            self.meta = json.load(f)
        self.logfile = logfile
        self.console = console

        if self.logfile:
            # todo error if it exists
            self.logfile = open(self.logfile, 'w')
            # this is a hack
            # pandas will have an error if any row has
            # fewer columns than the first row
            self.log(LLOG_NONE, '                                                 ')

    def log(self, type, data):
        t = time.time()
        logstring = f'{t:.6f} {type} {data}\n'
        if self.console:
            print(logstring, end='')
        if self.logfile:
            self.logfile.write(logstring)

    def close(self):
        if self.logfile:
            self.logfile.close()
