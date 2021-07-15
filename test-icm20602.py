#!/usr/bin/python3

import argparse
from icm20602 import ICM20602
from llogger import LLogger
import signal
import time

parser = argparse.ArgumentParser(description='icm20602 test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--frequency', action='store', type=int, default=None)
args = parser.parse_args()


LLOG_ERROR = 0
# read only memory + factory calibration and serialization type information
LLOG_ROM = 1
# application-specific configuration information
LLOG_CONFIG = 2
# measurement data
LLOG_DATA = 4
# calibration data
LLOG_CALIBRATION = 5

def icmFormat(data):
    return (f'{data.a.x} {data.a.y} {data.a.z} {data.g.x} {data.g.y} {data.g.z} {data.t} '
            f'{data.a_raw.x} {data.a_raw.y} {data.a_raw.z} {data.g_raw.x} {data.g_raw.y} {data.g_raw.z} {data.t_raw}')

categories = {
    LLOG_ERROR: {
        'name': 'error',
        'columns': [
            ['error code', '-']
        ]
    },
    LLOG_ROM: {
        'name': 'rom',
        'columns': [
            ['month', '-'],
            ['day', '-'],
            ['year', '-'],
            ['pmin', 'bar'],
            ['pmax', 'bar'],
            ['pmode', '[PA,PR,PAA]']
        ]
    },
    LLOG_DATA: {
        'name': 'measurement',
        'columns': [
            ['ax', 'g'],
            ['ay', 'g'],
            ['az', 'g'],
            ['gx', 'dps'],
            ['gy', 'dps'],
            ['gz', 'dps'],
            ['temperature', 'C'],
            ['ax_raw', 'g'],
            ['ay_raw', 'g'],
            ['az_raw', 'g'],
            ['gx_raw', 'dps'],
            ['gy_raw', 'dps'],
            ['gz_raw', 'dps'],
            ['temperature_raw', 'C'],
        ],
        'format': icmFormat
    },
}

log = LLogger(categories, console=True, logfile=args.output)

def cleanup(_signo, _stack):
    log.close()
    exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)


icm = ICM20602()

while True:
    try:
        data = icm.read_all()
        log.log(LLOG_DATA, data)
    except Exception as e:
        log.log(LLOG_ERROR, e)

    if args.frequency:
        time.sleep(1.0/args.frequency)
