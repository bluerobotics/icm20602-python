#!/usr/bin/python3

import argparse
from llog import LLogReader
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
defaultMeta = dir_path+'/icm20602.meta'

parser = argparse.ArgumentParser(description='icm20602 test report')
parser.add_argument('--input', action='store', type=str, required=True)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
parser.add_argument('--output', action='store', type=str)
args = parser.parse_args()

log = LLogReader(args.input, 'bme.meta')

gn = log.data[['gx', 'gy', 'gz']]
an = log.data[['ax', 'ay', 'az']]
t = log.data.t

header = 'icm20602 test report'
f, spec = log.figure(height_ratios=[1,4,4,4])

plt.subplot(spec[1,:])
gn.pplot()
plt.subplot(spec[2,:])
an.pplot()
plt.subplot(spec[3,:])
t.pplot()

plt.show()
