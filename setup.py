# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from setuptools import setup


if __name__ == '__main__':
    print('Sopel does not correctly load modules installed with setup.py '
          'directly. Please use "pip install .".',
          file=sys.stderr)


setup()
