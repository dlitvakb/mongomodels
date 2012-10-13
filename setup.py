#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="mongomodels",
    version="0.7.3",
    description="A simple ODM for MongoDB",
    author="David Litvak",
    author_email = "david.litvakb@gmail.com",
    license = "GPL v3",
    keywords = "MongoDB ODM Database",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      'pymongo',
      'event_handler'
    ],
    url='http://github.com/dlitvakb',
)
