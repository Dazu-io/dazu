import argparse

import grpc

import dazu.config
from dazu import version
from dazu.cli import run, train

import dazu.components.proto.component_pb2 as component__pb2
import dazu.components.proto.component_pb2_grpc as component_pb2_grpc

from google.protobuf.struct_pb2 import Struct


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dazu",
        description="An engine for chatbots. Inspired by Watson Assistant and Rasa.",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Print installed Dazu version",
    )

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parsers = [parent_parser]

    subparsers = parser.add_subparsers(help="Dazu commands")

    run.add_subparser(subparsers, parents=parent_parsers)
    train.add_subparser(subparsers, parents=parent_parsers)

    return parser


def print_version() -> None:
    print("Dazu", version.__version__)


def main() -> None:
    channel = grpc.insecure_channel("localhost:9898")
    stub = component_pb2_grpc.ComponentServiceStub(channel)

    s = Struct()
    s.update({"text": "value"})
    response = stub.Process(component__pb2.DazuMessage(input=s))
    print("Greeter client received: " + response.output["text"][0])

    arg_parser = create_argument_parser()
    cmdline_arguments = arg_parser.parse_args()

    if hasattr(cmdline_arguments, "func"):
        kwargs = cmdline_arguments.__dict__

        config = dazu.config.load(None, **kwargs)

        cmdline_arguments.func(config, cmdline_arguments)
    elif hasattr(cmdline_arguments, "version"):
        print_version()
    else:
        # user has not provided a subcommand, let's print the help
        print("No command specified.")
        arg_parser.print_help()
        exit(1)


if __name__ == "__main__":
    main()
