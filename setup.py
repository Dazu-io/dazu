import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
with open("david/version.py") as f:
    exec(f.read())

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


# Get requirements from files.
# Solution from https://stackoverflow.com/a/25193001/12704331
def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


dev_requires = parse_requirements("requirements-dev.txt")
docs_requires = parse_requirements("requirements-docs.txt")
install_requires = parse_requirements("requirements.txt")

extras_requires = {
    "dev": dev_requires,
    # "spacy": ["spacy>=2.1,<2.2"],
    # "convert": ["tensorflow_text~=1.15.1", "tensorflow_hub~=0.6.0"],
    # "mitie": ["mitie"],
    # "sql": ["psycopg2~=2.8.2", "SQLAlchemy~=1.3"],
    # "kafka": ["kafka-python~=1.4"],
}

setup(
    name="david",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        # supported python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests", "tools", "docs", "contrib"]),
    entry_points={"console_scripts": ["david=david.__main__:main"]},
    version=__version__,
    install_requires=install_requires,
    extras_requires=extras_requires,
    include_package_data=True,
    description="An engine for chatbots. Inspired by Watson Assistant and Rasa.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Raphael Pinto",
    author_email="raphaelcpinto@gmail.com",
    maintainer="Raphael Pinto",
    maintainer_email="raphaelcpinto@gmail.com",
    license="Apache 2.0",
    keywords="nlp machine-learning machine-learning-library bot bots "
    "botkit rasa conversational-agents conversational-ai chatbot"
    "chatbot-framework bot-framework watson nlu",
    url="https://github.com/ralphg6/david",
    download_url="https://github.com/ralphg6/david/archive/{}.tar.gz"
    "".format(__version__),
    project_urls={
        "Bug Reports": "https://github.com/ralphg6/david/issues",
        "Source": "https://github.com/ralphg6/david",
    },
)

print("\nWelcome to David!")
print(
    "If you have any questions, please visit our documentation page: https://github.com/ralphg6/david/"
)
print("or join the community discussions on https://github.com/ralphg6/david/issues/")
