# David
An engine for chatbots. 

Inspired by Watson Assistant and Rasa.

## How to RUN

```bash
docker-compose up --build
```

or in editable mode:

```bash
pip3 install -r requirements-dev.txt
pip3 install -e .
cd examples/my-first-bot
david
```

## How can you contribute?

- [ ] Improve code documentation
- [ ] Improve README.md
- [ ] Improve condition evaluation engine
  - [ ] Context Variables
  - [ ] Entities
  - [ ] Other expressions in SPEL
- [ ] Modularize the code
- [ ] Implement support for multiples NLU engines
- [ ] Implement support for RASA NLU Engine

## Name of Project

The name was inspired by [David Ausubel](https://novaescola.org.br/conteudo/262/david-ausubel-e-a-aprendizagem-significativa) because the main objective of this project was to build a collaborative platform to maintain Bots for learning.

## Development Internals
### Running and changing the documentation
To build <!--& edit the docs-->, first install all necessary dependencies:

```
pip3 install -r requirements-dev.txt
```
<!--
After the installation has finished, you can run and view the documentation
locally using:
```
make livedocs
```

Visit the local version of the docs at http://localhost:8000 in your browser.
You can now change the docs locally and the web page will automatically reload
and apply your changes.

### Running the Tests
In order to run the tests, make sure that you have the development requirements installed:
```bash
export PIP_USE_PEP517=false
pip3 install -r requirements-dev.txt
pip3 install -e .
make prepare-tests-ubuntu # Only on Ubuntu and Debian based systems
make prepare-tests-macos  # Only on macOS
```

Then, run the tests:
```bash
make test
```

They can also be run at multiple jobs to save some time:
```bash
JOBS=[n] make test
```

Where `[n]` is the number of jobs desired. If omitted, `[n]` will be automatically chosen by pytest.

### Steps to release a new version
Releasing a new version is quite simple, as the packages are build and distributed by travis.

*Terminology*:
* patch release (third version part increases): 1.1.2 -> 1.1.3
* minor release (second version part increases): 1.1.3 -> 1.2.0
* major release (first version part increases): 1.2.0 -> 2.0.0

*Release steps*:
1. Make sure all dependencies are up to date (**especially Rasa SDK**)
2. Switch to the branch you want to cut the release from (`master` in case of a major / minor, the current feature branch for patch releases) 
3. Run `make release`
4. Create a PR against master or the release branch (e.g. `1.2.x`)
5. Once your PR is merged, tag a new release (this SHOULD always happen on master or release branches), e.g. using
    ```bash
    git tag 1.2.0 -m "next release"
    git push origin 1.2.0
    ```
    travis will build this tag and push a package to [pypi](https://pypi.python.org/pypi/rasa)
6. **If this is a minor release**, a new release branch should be created pointing to the same commit as the tag to allow for future patch releases, e.g.
    ```bash
    git checkout -b 1.2.x
    git push origin 1.2.x
    ```
-->
### Code Style

To ensure a standardized code style we use the formatter [black](https://github.com/ambv/black).
To ensure our type annotations are correct we use the type checker [pytype](https://github.com/google/pytype). 
If your code is not formatted properly or doesn't type check, travis will fail to build.

#### Formatting

If you want to automatically format your code on every commit, you can use [pre-commit](https://pre-commit.com/).
Just install it via `pip install pre-commit` and execute `pre-commit install` in the root folder.
This will add a hook to the repository, which reformats files on every commit.

If you want to set it up manually, install black via `pip install -r requirements-dev.txt`.
To reformat files execute
```
make formatter
```

#### Type Checking

If you want to check types on the codebase, install `pytype` using `pip install -r requirements-dev.txt`.
To check the types execute
```
make types
```
<!--
### Deploying documentation updates

We use `sphinx-versioning` to build docs for tagged versions and for the master branch.
The static site that gets built is pushed to the `docs` branch of this repo, which doesn't contain
any code, only the site.

We host the site on netlify. When there is a reason to update the docs (e.g. master has changed or we have
tagged a new version) we trigger a webhook on netlify (see `.travis.yml`). 
-->
