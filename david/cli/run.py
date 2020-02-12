import argparse
from typing import List

from david.cli.arguments import run as arguments
from david.components.engine import Engine
from david.config import DavidConfig
from david.server import Server


# noinspection PyProtectedMember
def add_subparser(
    subparsers: argparse._SubParsersAction, parents: List[argparse.ArgumentParser]
):
    run_parser = subparsers.add_parser(
        "run",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Starts a David server with your configured "
        "pipeline and your trained model.",
    )
    run_parser.set_defaults(func=run)

    arguments.set_run_arguments(run_parser)


def run(config: DavidConfig, args: argparse.Namespace):

    engine = Engine(config)

    Server.start(config, engine)
