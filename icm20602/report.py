#!/usr/bin/python3

import matplotlib.pyplot as plt

def generate_figures(log):
    an = log.data[['ax', 'ay', 'az']]
    gn = log.data[['gx', 'gy', 'gz']]
    t = log.data.t

    footer = 'icm20602 test report'

    f, spec = log.figure(height_ratios=[1,1], suptitle='icm20602 data statistics', footer=footer)
    plt.subplot(spec[0,:])
    an.stats().ttable(rl=True)

    plt.subplot(spec[1,:])
    gn.stats().ttable(rl=True)

    f, spec = log.figure(height_ratios=[1,1,1], suptitle='icm20602 data plots', footer=footer)

    plt.subplot(spec[0,:])
    an.pplot()

    plt.subplot(spec[1,:])
    gn.pplot()

    plt.subplot(spec[2,:])
    t.pplot()


def main():
    import argparse
    from llog import LLogReader
    from matplotlib.backends.backend_pdf import PdfPages
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

    generate_figures(log)

    if args.output:
        # todo check if it exists!
        with PdfPages(args.output) as pdf:
            [pdf.savefig(n) for n in plt.get_fignums()]

    if args.show:
        plt.show()

if __name__ == '__main__':
    main()
