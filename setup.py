from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=['server','library','core'])
)