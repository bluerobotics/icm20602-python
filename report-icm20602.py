#!/usr/bin/python3

import argparse
from llog import LLogReader
import matplotlib.pyplot as plt
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

defaultMeta = dir_path + '/icm20602.meta'
parser = argparse.ArgumentParser(description='icm20602 test report')
parser.add_argument('--input', action='store', type=str, required=True)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
parser.add_argument('--output', action='store', type=str)
args = parser.parse_args()

log = LLogReader(args.meta, args.input)

