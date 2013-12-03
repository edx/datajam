"""Setup for Answer Distribution Histogram XBlock."""

import os
from setuptools import setup


def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='answerhisto-xblock',
    version='0.1',
    description='Answer Distribution Histogram XBlock',
    packages=[
        'answerhisto',
    ],
    install_requires=[
        'XBlock',
        'matplotlib',
    ],
    entry_points={
        'xblock.v1': [
            'answerhisto = answerhisto:AnswerDistHistogramBlock',
        ]
    },
    package_data=package_data("answerhisto", "static"),
)
