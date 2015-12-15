from setuptools import setup
from setuptools import find_packages

setup(name='yamr',
      version='0.0.1',
      description='Movie recommender',
      install_requires=['flask', 'graphlab', 'tmdbsimple', 'ipyparallel'],
      packages=find_packages())
