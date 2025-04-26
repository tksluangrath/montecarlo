from setuptools import setup, find_packages

setup(
    name='montecarlo',
    version='1.1',
    description='A Python module for Monte Carlo simulations using Die, Game, and Analyzer classes.',
    url='https://github.com/tksluangrath/m09-homework-2025',
    long_description = open('README.md').read(),
    author='Terrance Luangrath',
    author_email='vwy4sa@virginia.com',
    license='MIT',
    packages=find_packages(),
    install_requires = [
        'numpy',
        'pandas',
        'pytest'
    ]
)