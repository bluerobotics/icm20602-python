#!/usr/bin/python3

def main():
    from icm20602 import ICM20602
    from llog import LLogWriter
    import time

    device = "icm20602"
    parser = LLogWriter.create_default_parser(__file__, device)
    args = parser.parse_args()

    with LLogWriter(args.meta, args.output) as log:
        icm = ICM20602()

        def data_getter():
            data = icm.read_all()
            return (f'{data.a.x} {data.a.y} {data.a.z} {data.g.x} {data.g.y} {data.g.z} {data.t} '
                    f'{data.a_raw.x} {data.a_raw.y} {data.a_raw.z} '
                    f'{data.g_raw.x} {data.g_raw.y} {data.g_raw.z} {data.t_raw}')

        log.log_data_loop(data_getter, parser_args=args)

if __name__ == '__main__':
    main()
