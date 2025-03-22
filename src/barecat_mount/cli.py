import argparse
import barecat
from barecat_mount.barecat_mount import BarecatFuse, BarecatFuseMmap, PyFuse


def mount():
    parser = argparse.ArgumentParser(description='Mount a Barecat archive as a FUSE filesystem.')
    parser.add_argument('barecat_file', type=str, help='path to the barecat file')
    parser.add_argument('mount_point', type=str, help='path to the mount point')
    parser.add_argument('--writable', action='store_true', help='mount the filesystem writeable')
    parser.add_argument('--overwrite', action='store_true', help='delete existing barecat')
    parser.add_argument('--append-only', action='store_true', help='append-only mode')
    parser.add_argument(
        '--mmap',
        action='store_true',
        help='Use memory-mapped files to read data. Ignored if --writable is specified.',
    )
    parser.add_argument(
        '--enable-defrag',
        action='store_true',
        help='enables periodic defragmentation of the data shards after '
        'significant amount of '
        'deleted space. Has no effect in readonly or append-only mode.',
    )
    parser.add_argument(
        '--shard-size-limit',
        type=str,
        default=None,
        help='maximum size of a shard in bytes (if not specified, '
        'it is left at the previous setting stored in the index database if '
        'mounting an existing Barecat, or it created as unlimited)',
    )
    parser.add_argument(
        '--foreground', action='store_true', help='run in the foreground, don\'t daemonize'
    )
    args = parser.parse_args()
    readonly = not args.writable
    with barecat.Barecat(
        args.barecat_file,
        readonly=readonly,
        append_only=args.append_only,
        overwrite=args.overwrite,
        shard_size_limit=args.shard_size_limit,
    ) as bc:
        barecat_fuse = (
            BarecatFuseMmap(bc)
            if readonly and args.mmap
            else BarecatFuse(bc, enable_defrag=args.enable_defrag)
        )
        barecat_fuse.mount(
            args.mount_point,
            readonly=readonly,
            single_threaded=True,
            foreground=args.foreground,
        )
