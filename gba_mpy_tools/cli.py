import sys
# the real import begin
from argparse import ArgumentParser
from os import chdir
from gba_mpy_tools.config import Config
import gba_mpy_tools.action as m_action

def parse_args():
    parser = ArgumentParser(
        description="GBA MicroPython Tools"
    )
    parser.add_argument(
        "-c", "--config",
        dest="config_path",
        default=".",
        help="Config file path, or workspace which contains the config file (.gbampy.toml)",
    )
    subparser = parser.add_subparsers()

    cmd_build = subparser.add_parser(
        "list",
        help="List all the files that will be write into the ROM"
    )
    cmd_build.set_defaults(action="list")

    cmd_build = subparser.add_parser(
        "build",
        help="Build GBA ROM"
    )
    cmd_build.set_defaults(action="build")
    
    cmd_run = subparser.add_parser(
        "run",
        help="Build GBA ROM and run with emulator",
    )
    cmd_run.set_defaults(action="run")

    args = parser.parse_args()
    if not hasattr(args, "action"):
        parser.print_help()
        sys.exit(-1)
    return args

def main():
    args = parse_args()
    cfg = Config(args.config_path)
    chdir(cfg.config_file_dir)
    if args.action == "list":
        file_list = m_action.list_files(cfg)
        for item in file_list:
            print(item.target, "    -> is_dir:", item.is_dir, "compile:", item.compile)
    elif args.action == "build":
        m_action.build(cfg)
    elif args.action == "run":
        m_action.run(cfg)

def _start_():
    main()

if __name__ == "__main__":
    _start_()
