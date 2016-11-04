#!/usr/bin/env python

from setuptools import setup

setup(
    name="kitewrapper",
    version="3.3",
    description="Wrapper around kiteconnect",
    packages=["kitewrapper"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries"
    ],
    install_requires=["requests", "six", "websocket-client", "kiteconnect"]
)
