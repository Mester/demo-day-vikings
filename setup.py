# -*- coding: utf-8 -*-

import os
from setuptools import setup

with open('README.md') as f:
    readme = f.read()


with open('LICENSE') as f:
    license = f.read()


setup(
    name= 'my_app',     #replace later?
    version= '0.0.1',
    description='Generate a list of 10 trending songs from r/listentothis',
    long_description=readme,
    authors='Ben Dauer, Adrian Hintermaier, Jason Meeks, Tyler Phillips, Anubhav Yadav',
    url= 'https://github.com/Mester/demo-day-vikings',
    license=license,
    packages= ['my_app'],
    install_requires=[
        'Flask==0.11.1'
    ]
)