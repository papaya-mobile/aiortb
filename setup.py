# -*- coding: utf-8 -*-

import os
import re
import codecs
from setuptools import setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

with codecs.open(
        os.path.join(ROOT, 'aiortb', '__init__.py'), 'r', 'utf-8') as init:
    version = VERSION_RE.search(init.read()).group(1)

desc = 'aiortb - a rtb exchange framework based on asyncio and aiohttp'


setup(name='aiortb',
      version=version,
      packages=['aiortb'],
      entry_points={},
      description=desc,
      author='Papaya Backend',
      author_email='backend@papayamobile.com',
      install_requires=['aiohttp'],
      )
