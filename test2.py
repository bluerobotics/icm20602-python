
import argparse
from fpdf import FPDF
from llog import LLogReader
import pandas as pd
import matplotlib.pyplot as plt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
defaultMeta = dir_path+'/icm20602.meta'



log = LLogReader('aaaa', defaultMeta)
# log.data.ll.plot(['ax', 'ay', 'az'], ['t'])



# log.data['ax', 'ay', 'az'].plot(d2=log.data.t)

an = log.data[['ax', 'ay', 'az']]
gn = log.data[['gx', 'gy', 'gz']]
t = log.data.t

# an.plot(d2=t)
# gn.plot(d2=t)
# t.plot(d2=an)
# an.plot()
# plt.figure()
# gn.plot()
# plt.figure()
# t.plot()
# plt.show()
