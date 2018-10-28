import os
import io
from setuptools import setup



requirements = [
    'numpy',
    'matplotlib',
    'numpy',
    'PIL',
    'threading',
    'math',
    'pickle'
    ]

setup(
    name='FFT Image Cryptography',
    version='1.0',
    author='Jihoon Lee',
    author_email='anfwkrpdnjs179@gmail.com',
    description='Creates 2 FFT images (contains Real, Imag respectively) with phase scrambling in frequency domain',
    install_requires=requirements
    )
