#!/usr/bin/python3

from llog import LLogReader
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

DEVICE = 'icm20602'
parser = LLogReader.create_default_parser(__file__, DEVICE)
args = parser.parse_args()

log = LLogReader(args.input, args.meta)

an = log.data[['ax', 'ay', 'az']]
gn = log.data[['gx', 'gy', 'gz']]
t = log.data.t

footer = f'{DEVICE} test report'

f, spec = log.figure(height_ratios=[1,1], suptitle=f'{DEVICE} data statistics', footer=footer)
plt.subplot(spec[0,:])
an.stats().ttable(rl=True)

plt.subplot(spec[1,:])
gn.stats().ttable(rl=True)

f, spec = log.figure(height_ratios=[1,1,1], suptitle=f'{DEVICE} data plots', footer=footer)

plt.subplot(spec[0,:])
an.pplot()

plt.subplot(spec[1,:])
gn.pplot()

plt.subplot(spec[2,:])
t.pplot()

if args.output:
    # todo check if it exists!
    with PdfPages(args.output) as pdf:
        [pdf.savefig(n) for n in plt.get_fignums()]

if args.show:
    plt.show()
