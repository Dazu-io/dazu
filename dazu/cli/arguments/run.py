import argparse

from dazu import constants
from dazu.adapters.adapter import MessageAdapter
from dazu.cli.arguments.util import add_argument


def set_run_arguments(parser: argparse.ArgumentParser):
    add_server_arguments(parser)


def add_server_arguments(parser: argparse.ArgumentParser):
    add_argument(
        parser,
        constants.CONFIG_DEFAULT_ADAPTER,
        type=str,
        default=MessageAdapter.name(),
        help="Redefine default adapter",
    )
