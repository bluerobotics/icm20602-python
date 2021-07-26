#!/usr/bin/python3

import argparse
from llog import LLogReader
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

defaultMeta = dir_path + '/icm20602.meta'
parser = argparse.ArgumentParser(description='icm20602 test report')
parser.add_argument('--input', action='store', type=str, required=True)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
parser.add_argument('--output', action='store', type=str)
parser.add_argument('--show', action='store_true')
args = parser.parse_args()

log = LLogReader(args.input, args.meta)

an = log.data[['ax', 'ay', 'az']]
gn = log.data[['gx', 'gy', 'gz']]
t = log.data.t

pdf = None
if args.output:
    outfile = open('icm20602.pdf', 'wb')
    pdf = PdfPages(outfile)

def saveFig():
    if pdf:
        pdf.savefig()

def closeFig():
    if pdf:
        pdf.close()

footer = 'icm20602 test report'

f, spec = log.figure(height_ratios=[1,1], suptitle='icm20602 data statistics', footer=footer)
plt.subplot(spec[0,:])
an.stats().table(rl=True)

plt.subplot(spec[1,:])
gn.stats().table(rl=True)

saveFig()

f, spec = log.figure(height_ratios=[1,1,1], suptitle='icm20602 data plots', footer=footer)

plt.subplot(spec[0,:])
an.pplot()

plt.subplot(spec[1,:])
gn.pplot()

plt.subplot(spec[2,:])
t.pplot()

saveFig()

closeFig()

if args.show:
    plt.show()
