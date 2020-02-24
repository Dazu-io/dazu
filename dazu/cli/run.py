import argparse
from typing import List

from dazu.cli.arguments import run as arguments
from dazu.components.engine import Engine
from dazu.config import DazuConfig
from dazu.server import Server


# noinspection PyProtectedMember
def add_subparser(
    subparsers: argparse._SubParsersAction, parents: List[argparse.ArgumentParser]
):
    run_parser = subparsers.add_parser(
        "run",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Starts a Dazu server with your configured "
        "pipeline and your trained model.",
    )
    run_parser.set_defaults(func=run)

    arguments.set_run_arguments(run_parser)


def run(config: DazuConfig, args: argparse.Namespace):

    engine = Engine(config)

    Server.start(config, engine)
