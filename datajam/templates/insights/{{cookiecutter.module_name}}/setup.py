"""Setup for {{cookiecutter.module_name}} Insights module."""

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
    name='{{cookiecutter.module_name}}',
    version='0.1',
    description='{{cookiecutter.module_name}} Insights',
    packages=[
        '{{cookiecutter.module_name}}',
    ],
    install_requires=[
        'edinsights',
    ],
    package_data=package_data("{{cookiecutter.module_name}}", "static"),
)
