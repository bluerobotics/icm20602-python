#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import json
import time

LLOG_ERROR = '0'
# measurement data
LLOG_DATA = '1'
# read only memory + factory calibration and serialization type information
LLOG_ROM = '2'
# application-specific configuration information
LLOG_CONFIG = '3'
# calibration data
LLOG_CALIBRATION = '4'

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

# https://stackoverflow.com/questions/47466255/subclassing-a-pandas-dataframe-updates
# https://stackoverflow.com/questions/47466255/subclassing-a-pandas-dataframe-updates
class LLogSeries(pd.Series):
    _metadata = ['meta']

    @property
    def _constructor(self):
        return LLogSeries

    @property
    def _constructor_expanddim(self):
        return LLogDataFrame

    def pplot(self, ll2=None, *args, **kwargs):
        print(f'sup {self.name}')

        columns = self.meta['columns']
        meta = {}
        for c in columns:
            print(c, self.name, c.get('llabel'))
            if self.name == c.get('llabel'):
                print('got', c)
                meta = c
                break
        # meta = self.meta[self.name]

        kwargs2 = kwargs | {'label': self.name}

        for opt in ["color", "style", "label"]:
            try:
                kwargs2 = kwargs2 | {opt:meta[opt]}
            except KeyError as e:
                # print(e)
                pass
        
        self.plot(*args, **kwargs2)
        plt.legend()
        plt.ylabel(meta.get('units'))

        if ll2 is not None:
            plt.twinx()
            ll2.pplot(*args, **kwargs)
        
    
# https://stackoverflow.com/questions/48325859/subclass-pandas-dataframe-with-required-argument
class LLogDataFrame(pd.DataFrame):
    _metadata = ['meta']

    def __init__(self, *args, **kwargs):
        # grab the keyword argument that is supposed to be my_attr
        self.meta = kwargs.pop('meta', None)

        super().__init__(*args, **kwargs)

        # sometimes dataframe meta is not provided in intermediate operations
        # if self.meta is not None:
        if self.meta is not None:
            columns = self.meta.get('columns', [])

            l = min(len(columns), len(self.columns)-2)

            for c in range(l):
                try:
                    dtype = columns[c]['dtype']
                    i = c+2
                    if dtype == "int":
                        print('setting is', c, dtype)
                        self[i] = self[i].astype(int)

                    elif dtype == "float":
                        self[i] = self[i].astype(float)

                except KeyError as e:
                    try:
                        self[i] = self[i].astype(float)
                    except Exception as e:
                        pass
                llabel = columns[c]['llabel']
                print(llabel)
                self.rename(columns={c+2:llabel}, inplace=True)
                # self[c+2].rename(llabel, inplace=True)

            print("hello", columns, self.columns, len(self), len(columns))
            for c in self.columns:
                print(self[c])

    @property
    def _constructor(self):
        def _c(*args, **kwargs):
            df = LLogDataFrame(*args, meta=self.meta, index=None, **kwargs)
            return df
        return _c
        
    @property
    def _constructor_sliced(self):
        print('ldsliced')
        return LLogSeries

    def pplot(self, d2=None, *args, **kwargs):
        for c in self:
            self[c].pplot(*args, **kwargs)
        # plot things on secondary axis
        if d2 is not None:
            plt.twinx()
            d2.pplot(*args, **kwargs)

class LLogReader:
    def __init__(self, logfile, metafile):
        # self.meta = self.metaOpen(metafile)
        self.df = self.logOpen(logfile)
        
        self.meta = self.metaOpen(metafile)
        # self.df.meta = self.metaOpen(metafile)

        self.df.rename(columns={0:'time', 1:'llKey'}, inplace=True)
        self.df['llKey'] = self.df['llKey'].astype(int)

        # for llType, llDesc in self.meta.items():
        #     DF = self.df

        #     attr = llDesc['type']
        #     value = DF[DF['llType'] == int(llType)].dropna(axis='columns', how='all')

        #     try:
        #         columns = llDesc['columns']
        #         l = min(len(columns), len(value.columns)-2)

        #         # rename columns
        #         for c in range(l):
        #             i = c + 2
        #             name = columns[c]['name']
        #             value.rename(columns={i: name}, inplace=True)
        #     except:
        #         pass
        # #         # convert field type
        #         for c in range(l):
        #             name = columns[c]['name']
        #             try:
        #                 dtype = columns[c]['dtype']
        #                 print('dtype is', dtype, type(dtype), dtype=="int")
        #                 if dtype == "int":
        #                     value[name] = value[name].astype(int)
        #                 elif dtype == "float":
        #                     value[name] = value[name].astype(float)
        #             except KeyError:
        #                 try:
        #                     value[name] = value[name].astype(float)
        #                 except:
        #                     pass

        #         # # attach metadata !! this must be done last
        #         # for c in range(l):
        #         #     name = columns[c]['name']
        #         #     value[name].attrs['llMeta'] = llOptional | columns[c]

        #     except ValueError:
        #         print(f'{attr} could not convert string to float')
        #         pass
        #     except KeyError:
        #         print(f'{attr} does not have columns definition')
        #         pass
        # for llType, llDesc in self.meta.items():
        #     DF = self.df

        #     attr = llDesc['type']
        #     value = DF[DF['llType'] == int(llType)].dropna(axis='columns', how='all')

            # eg for each type name in log, set self.type to
            # the dataframe representing only that type
            # setattr(self, attr, value)





        

        for llKey, llDesc in self.meta.items():
            DF = self.df

            value = DF[DF['llKey'] == int(llKey)].dropna(axis='columns', how='all')

            # eg for each type name in log, set self.type to
            # the dataframe representing only that type
            print(llKey, llDesc)
            value = LLogDataFrame(value, meta=llDesc)
            # value.meta = llDesc
            

            # try:
            #     c = {i+2:llDesc['columns'][i]['name'] for i in range(len(llDesc['columns']))}
            #     value.rename(columns=c, inplace=True)
        
            # except:
            #     pass
            
            # try:
            #     # do this first to go by index
            #     columns = llDesc['columns']
           

            #     # subtract 2 for the required timestamp and llType
            #     l = min(len(columns), len(value.columns)-2)
            #     for i in range(l):
            #         name = columns[i]['name']
            #         value.rename(columns={i+2: name}, inplace=True)
            #         value[name].llSeriesMeta = columns[i]
            #         print(f'!!!! {i} {value[name].llSeriesMeta}')

            # except Exception as e:
            #     print(e)


            # try:
            #     for s in value:
            #         print(f'~~~~~~{value[s].llSeriesMeta}')
                
            # except Exception as e:
            #     print(e)

            # todo global llType
            llType = llDesc['llType']


            # create LLDF..
            setattr(self, llType, value)

    def metaOpen(self, metafile):
        with open(metafile, 'r') as f:
            return json.load(f)
    
    def logOpen(self, logfile):
        return pd.read_csv(logfile,sep=' ', header=None).dropna(axis='columns', how='all').set_index(0, drop=False)
        # df = pd.read_csv(logfile,sep=' ', header=None).dropna(axis='columns', how='all').set_index(0, drop=False)
        # return LLogDataFrame(df)

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
