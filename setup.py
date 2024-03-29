import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="igql",
    version="1.1.2",
    description="InstagramGraphQL Unofficial API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/FKLC/IGQL",
    author="Fatih Kılıç",
    author_email="***REMOVED***",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["igql"],
    install_requires=["anyapi==1.1.401", "requests"],
)
