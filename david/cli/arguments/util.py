import argparse


def add_argument(parser: argparse.ArgumentParser, name: str, **kwargs):
    arg_name = "--" + name.replace("_", "-")
    parser.add_argument(arg_name, **kwargs)
