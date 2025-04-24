from setuptools import setup

setup(
    name='montecarlo',
    version='0.1',
    description='A Python module for Monte Carlo simulations using Die, Game, and Analyzer classes.',
    url='https://github.com/tksluangrath/m09-homework-2025',
    long_description = open('README.md').read(),
    author='Terrance Luangrath',
    author_email='vwy4sa@virginia.com',
    license='MIT',
    packages=['montecarlo'],
    install_requires = [
        'numpy',
        'pandas',
        'pytest'
    ]
)