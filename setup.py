#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
]

test_requirements = []

setup(
    author="Karel Antonio Verdecia Ortiz",
    author_email="kverdecia@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="Create different types of network forwardings (with ssh, kubectl, caddy, etc).",
    entry_points={
        "console_scripts": [
            "netforward=netforward.cli:main",
        ],
    },
    install_requires=["pexpect"],
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="netforward",
    name="netforward",
    packages=find_packages(include=["netforward", "netforward.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/kverdecia/netforward",
    version="0.1.0",
    zip_safe=False,
)
