"""Local project information only. Does not access attached devices."""

import argparse
import json

from . import __version__


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="hslink-lp",
        description="HSLink-LP 工具骨架：当前只支持本地工程信息。",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("info", help="显示工程状态，不连接硬件")
    args = parser.parse_args(argv)
    if args.command == "info":
        print(json.dumps({
            "project": "HSLink-LP",
            "version": __version__,
            "phase": "scaffold",
            "hardware_transport_implemented": False,
            "base_hardware": "HSLink Pro 1.2.0 / HPM5301",
            "documentation": "README.md",
        }, ensure_ascii=False, indent=2))
    return 0
