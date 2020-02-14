import argparse
from typing import List

from david.components.engine import Engine
from david.config import DavidConfig


# noinspection PyProtectedMember
def add_subparser(
    subparsers: argparse._SubParsersAction, parents: List[argparse.ArgumentParser]
):
    train_parser = subparsers.add_parser(
        "train",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Starts train with Training Data with your configured pipeline.",
    )
    train_parser.set_defaults(func=train)

    # arguments.set_run_arguments(run_parser)


def train(config: DavidConfig, args: argparse.Namespace):
    engine = Engine(config)
    engine.train()
