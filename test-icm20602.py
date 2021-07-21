#!/usr/bin/python3

import argparse
from icm20602 import ICM20602
from llog import *
import os
import signal
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
defaultMeta = dir_path + '/icm20602.meta'

parser = argparse.ArgumentParser(description='icm20602 test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--frequency', action='store', type=int, default=None)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
args = parser.parse_args()

log = LLogWriter(args.meta, args.output)

def cleanup(_signo, _stack):
    log.close()
    exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

# format data object to csv string for llog
def format(data):
    return (f'{data.a.x} {data.a.y} {data.a.z} {data.g.x} {data.g.y} {data.g.z} {data.t} '
            f'{data.a_raw.x} {data.a_raw.y} {data.a_raw.z} {data.g_raw.x} {data.g_raw.y} {data.g_raw.z} {data.t_raw}')

icm = ICM20602()

while True:
    try:
        data = icm.read_all()
        log.log(LLOG_DATA, format(data))
    except Exception as e:
        log.log(LLOG_ERROR, e)
    if args.frequency:
        time.sleep(1.0/args.frequency)
