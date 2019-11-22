#!/usr/bin/env python

import os
from setuptools import setup, find_packages

install_requires = [
    line.rstrip() for line in open(os.path.join(os.path.dirname(__file__), "REQUIREMENTS.txt"))
]
print(install_requires)


setup(name='DotBlotr',
      install_requires=install_requires,
      version='0.0.1',
      description='Tools for analyzing dot blots',
      url='https://github.com/czbiohub/dotblotr',
      author='Kevin Yamauchi',
      author_email='kevin.yamauchi@czbiohub.org',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)