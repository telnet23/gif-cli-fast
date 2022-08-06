from pathlib import Path
from setuptools import setup, find_packages

with open(Path(__file__).parent.joinpath("README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="gif-cli-fast",
    description="Watch GIF animations in your terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/telnet23/gif-cli-fast",
    license="Apache License 2.0",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
    install_requires=["Pillow", "py256color @ git+https://github.com/telnet23/py256color"],
    entry_points={"console_scripts": ["gif = gif_cli_fast.__main__:main"]},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
)
