import david.config
from david.adapters.adapter import MessageAdapter
from david.cli.run import run
from david.constants import CONFIG_DEFAULT_ADAPTER

# [TODO] This kwargs must from CLI args
kwargs = {CONFIG_DEFAULT_ADAPTER: MessageAdapter.name()}

config = david.config.load(None, **kwargs)


def main() -> None:
    run(config)


if __name__ == "__main__":
    main()
