#!/usr/bin/python3

# import argparse
# from datetime import datetime
# from fpdf import FPDF
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np
# import os
# import pandas as pd


import argparse
from fpdf import FPDF
from llog import LLogReader
import pandas as pd
import matplotlib.pyplot as plt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
defaultMeta = dir_path+'/icm20602.meta'

# TODO Can I put this into a function?
parser = argparse.ArgumentParser(description='icm20602 test report')
parser.add_argument('--input', action='store', type=str, required=True)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
args = parser.parse_args()


log = LLogReader(args.input, args.meta)
# log.data.ll.plot(['ax', 'ay', 'az'], ['t'])



# log.data['ax', 'ay', 'az'].plot(d2=log.data.t)

an = log.data[['ax', 'ay', 'az']]
gn = log.data[['gx', 'gy', 'gz']]
t = log.data.t

an.plot(d2=t)
gn.plot(d2=t)
t.plot(d2=an)




# with a series, less important
log.data.ay.plot()


# plt.twinx()
# log.data.plot('t')


# plot acceleration
log.data.ay.ll.plot()
log.data.az.ll.plot()
log.data.ax.ll.plot()
plt.twinx()
log.data.t.ll.plot()

# log.data.ll.plot(['ax', 'ay', 'az'], ['t'])

plt.figure()

print(f'f1 {log.data["ax"].attrs}')

log.data.plot()
an = log.data['ax', 'ay', 'az']
gn = log.data['gx', 'gy', 'gz']
t = log.data.temperature

an.plot(t)
gn.plot(t)
# axn = d1[['ax', 'ay', 'az']]
# this doesn't delete original, but doesn't copy
axn = log.data.loc[:,['ax','ay']]

print(f'f2 {log.data["ax"].attrs}')
print(axn['ax'].attrs)
print('')
# for c in axn:
#     print(c)
#     print(axn[c].attrs)
print(axn)
axn.ll.plot()
# plot acceleration
log.data.ay.ll.plot()
log.data.az.ll.plot()
log.data.ax.add(1.0).ll.plot()
plt.twinx()
log.data.t.ll.plot()

# log.data.ll.plot(['ax', 'ay', 'az'], ['t'])

plt.figure()

log.data.gx.ll.plot()
log.data.gy.ll.plot()
log.data.gz.ll.plot()
plt.twinx()
log.data.t.ll.plot()

# https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.html#custom-describe
from functools import partial

q_25 = partial(pd.Series.quantile, q=0.25)
q_25.name = "25%"
q_75 = partial(pd.Series.quantile, q=0.75)
q_75.name = "75%"
print(log.data.agg(["count", "mean", "std", "min", q_25, "median", q_75, "max"]))

plt.show()


exit(0)
# d = log.data
# a = d[['ax','ay','az']]
# g = d[['gx','gy','gz']]

# log.pplot(m['time'], m[['ax', 'gy']])
# plt.show()
pdf = FPDF()
epw = pdf.w - 2*pdf.l_margin
eph = pdf.w - 2*pdf.l_margin
pdf.add_page()
pdf.set_font('Courier')






def addfig(fig, w, h):
    pdf.cell(w, h, f'{w} {h}', border=1)

def table_helper(pdf, epw, th, table_data, col_num):
    for row in table_data:
        maxwidth=0
        for datum in row:
            d = str(datum)
            w = pdf.get_string_width(d)
            if w > maxwidth:
                maxwidth = w
        for datum in row:
            # Enter data in columns
            d = str(datum)
            pdf.cell(maxwidth + 2, 2 * th, d, border=1)
        pdf.ln(2 * th)

table = [
    ['a','bda','c'],
    ['1','2','3'],
]
table_helper(pdf, epw, 4, table, 3)
addfig(1, 10, 10)
addfig(1, 10, 20)
pdf.output('test.pdf')
