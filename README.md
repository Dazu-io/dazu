# David

[![Documentation Status](https://readthedocs.org/projects/david-ausubel/badge/?version=latest)](https://david-ausubel.readthedocs.io/en/latest/?badge=latest)


**David** is a powerfull engine dialogue engine with two main parts: `NLU` and `dialogue`. The main objetive of this project is too use existing chatbots projects and uses it to develop your solution.

The name was inspired by [David Ausubel](https://novaescola.org.br/conteudo/262/david-ausubel-e-a-aprendizagem-significativa) because the main objective of this project was to build a collaborative platform to maintain Bots for learning.

Inspired by Watson Assistant and Rasa.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

* Docker:

```bash
docker-compose up --build
```

* Editable mode:

```bash
pip install -e .
cd examples/my-first-bot
david train
david run
```

* After that you should see this output:

```bash
david run
 * Serving Flask app "david.__main__" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

## Prerequisites

* To build, first install all necessary dependencies:

All the dependencies can be find in `requirements.txt` and development in `requirements-dev.txt`.

## Installing Development Environment

* A step by step installation guide:

1. Run these commands to install `david` in your python virtual env:

```bash
pip install -r requirements-dev.txt
pip install -e .
```

1. Go to examples folder and start the project:

```bash
cd examples/my-first-bot
david train
david run
```

1. Have fun :rocket:

## Code Style

To ensure a standardized code style we use the formatter [black](https://github.com/ambv/black).
To ensure our type annotations are correct we use the type checker [pytype](https://github.com/google/pytype). 
If your code is not formatted properly or doesn't type check, travis will fail to build.

### Formatting

If you want to automatically format your code on every commit, you can use [pre-commit](https://pre-commit.com/).
Just install it via `pip install pre-commit` and execute `pre-commit install` in the root folder.
This will add a hook to the repository, which reformats files on every commit.

If you want to set it up manually, install black via `pip install -r requirements-dev.txt`.
To reformat files execute
```
make formatter
```

### Type Checking

If you want to check types on the codebase, install `pytype` using `pip install -r requirements-dev.txt`.
To check the types execute
```
make types
```

## Running the tests

`Still needed`

## Deployment

`Still needed`

## Built With

* [Python](https://www.python.org/) - The main programing language used

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Raphael Pinto** - *Creator* - [ralphg6](https://github.com/ralphg6)

See also the list of [contributors](https://github.com/ralphg6/david/graphs/contributors) who participated in this project.

## License

This project is licensed under the Apache-2.0 - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* **Arthur Temporim** - [arthurTemporim](https://github.com/arthurTemporim)

