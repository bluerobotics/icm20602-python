#!/usr/bin/python3

import argparse
from icm20602 import ICM20602
from pathlib import Path
import llog
import time

device = "icm20602"
defaultMeta = Path(__file__).resolve().parent / f"{device}.meta"

parser = argparse.ArgumentParser(description=f'{device} test')
parser.add_argument('--output', action='store', type=str, default=None)
parser.add_argument('--meta', action='store', type=str, default=defaultMeta)
parser.add_argument('--frequency', action='store', type=int, default=None)
args = parser.parse_args()

with llog.LLogWriter(args.meta, args.output) as log:
    icm = ICM20602()

    while True:
        data = icm.read_all()
        log.log(llog.LLOG_DATA, (f'{data.a.x} {data.a.y} {data.a.z} {data.g.x} {data.g.y} {data.g.z} {data.t} '
                f'{data.a_raw.x} {data.a_raw.y} {data.a_raw.z} {data.g_raw.x} {data.g_raw.y} {data.g_raw.z} {data.t_raw}'))
        if args.frequency:
            time.sleep(1.0/args.frequency)
