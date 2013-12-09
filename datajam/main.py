#!/usr/bin/env python
"""
Use cookiecutter to create a new XBlock or Insights project.

"""

import os
import sys

from cookiecutter.main import cookiecutter


HELP = """\
datajam create <project-type>

arguments:
  <project-type>    xblock or insights

"""


def main():
    args = dict(zip(['command', 'project'], sys.argv[1:]))

    command = args.get('command')
    project = args.get('project')

    if command != 'create' or project not in ['xblock', 'insights']:
        print HELP
        return 1

    # Find the prototype for the project
    package_dir = os.path.split(__file__)[0]
    proto_dir = os.path.join(package_dir, "templates/{}".format(project.strip()))

    cookiecutter(proto_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
