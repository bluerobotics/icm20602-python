
import argparse
from matplotlib.backends.backend_pdf import PdfPages
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

# log.log(ll.LLOG_INFO, f'infox shax cmdx')

for i in range(10):
    log.log(ll.LLOG_ERROR, f'error{i}')

for i in range(100):
    log.log(ll.LLOG_DATA, f'{math.sin(i/5.0)} {i*i} {math.sin(i/4.0)} {math.sin(i/4.0 + 2)} {math.sin(i/4.0 + 4)}')

for i in range(5):
    log.log(ll.LLOG_ROM, f'{1.0/(i+1)} {i*100}')

log.close()

log = ll.LLogReader(output, meta)

dp = log.data['p']
dt = log.data['t']
dg = log.data[['gx', 'gy', 'gz']]

spec = log.figure()


plt.subplot(spec[0,:])
log.rom.table()

plt.subplot(spec[1,0])
dp.pplot(d2=dt)

plt.subplot(spec[1,1])
dt.pplot()

plt.subplot(spec[2,:])
dg.pplot()
plt.tight_layout()
plt.subplots_adjust(wspace=0.5)

with PdfPages('test.pdf') as pdf:
    pdf.savefig()
    pdf.savefig()    

plt.show()


## try scaling!

# da.plot()
# plt.figure()
# dp.plot()
# plt.figure()
# dt.plot()
# plt.figure()

# da.meta
# log.df['pressure'].plot()
