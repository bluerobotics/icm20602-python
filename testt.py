
import argparse
from fpdf import FPDF
import llog as ll
import pandas as pd
import matplotlib.pyplot as plt
import os


import math
dir_path = os.path.dirname(os.path.realpath(__file__))
defaultMeta = dir_path+'/icm20602.meta'

meta = 'test2.meta'
output = 'test2.csv'
log = ll.LLogWriter(meta, output)

log.log(ll.LLOG_CALIBRATION, f'                                            ')

for i in range(10):
    log.log(ll.LLOG_ERROR, f'error{i}')

for i in range(100):
    log.log(ll.LLOG_DATA, f'{i*i} {math.sin(i)}')

for i in range(10):
    log.log(ll.LLOG_ROM, f'{1.0/(i+1)} {i*100}')

log.close()

log = ll.LLogReader(output, meta)

da = log.data[['p', 't']]
dp = log.data['p']
dt = log.data['t']

## try scaling!

da.plot()
plt.figure()
dp.plot()
plt.figure()
dt.plot()
plt.figure()

da.meta
# log.df['pressure'].plot()
