#!/usr/bin/python3

import argparse
from datetime import datetime
from fpdf import FPDF
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from llllogger import LLogReader

parser = argparse.ArgumentParser(description='icm20602 test report')
parser.add_argument('--input', action='store', type=str, required=True)
# parser.add_argument('--output', action='store', type=str, required=True)
args = parser.parse_args()

log = LLogReader(args.input, 'bme.meta')

# g = log.data['gx', 'gy', 'gz']
# a = log.data['ax', 'ay', 'az']

# a.plot(g)

p = log.data.pressure
t = log.data.temperature

ax = p.ll.plot()
t.ll.plot(ax)
plt.show()

