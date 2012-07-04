#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="mongomodels",
    version="0.1.2",
    description="A simple ORM for MongoDB",
    author="David Litvak",
    author_email = "david.litvakb@gmail.com",
    license = "GPL v3",
    keywords = "MongoDB ORM Database",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      'pymongo'
    ],
    url='http://github.com/dlitvakb',
)
