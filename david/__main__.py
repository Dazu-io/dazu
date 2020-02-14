import argparse

import david.config
from david import version
from david.cli import run, train


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="david",
        description="An engine for chatbots. Inspired by Watson Assistant and Rasa.",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Print installed David version",
    )

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parsers = [parent_parser]

    subparsers = parser.add_subparsers(help="David commands")

    run.add_subparser(subparsers, parents=parent_parsers)
    train.add_subparser(subparsers, parents=parent_parsers)

    return parser


def print_version() -> None:
    print("David", version.__version__)


def main() -> None:
    # run(config)

    arg_parser = create_argument_parser()
    cmdline_arguments = arg_parser.parse_args()

    if hasattr(cmdline_arguments, "func"):
        kwargs = cmdline_arguments.__dict__

        config = david.config.load(None, **kwargs)

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
