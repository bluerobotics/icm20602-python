#!/usr/bin/python3

import argparse
from icm20602 import ICM20602
import signal
import time

parser = argparse.ArgumentParser(description='ads1115 test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--frequency', action='store', type=int, default=None)
args = parser.parse_args()

icm = ICM20602()

outfile = None

if args.output:
    outfile = open(args.output, "w")

def cleanup(_signo, _stack):
    if outfile:
        outfile.close()
    exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

while True:
    data = icm.read_all()
    output =   ( f'{time.time()} 1 {data.a.x} {data.a.y} {data.a.z} {data.g.x} {data.g.y} {data.g.z} {data.t} '
                 f'{data.a_raw.x} {data.a_raw.y} {data.a_raw.z} {data.g_raw.x} {data.g_raw.y} {data.g_raw.z} {data.t_raw}' )
    print(output)
    if outfile:
        outfile.write(output)
        outfile.write('\n')
    if args.frequency:
        time.sleep(1.0/args.frequency)
