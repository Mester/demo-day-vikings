# -*- coding: utf-8 -*-

import os
from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name= 'my_app',     #replace later?
    version= '0.0.1',
    description=readme,
    url= 'https://github.com/Mester/demo-day-vikings',
    packages= ['my_app']
)