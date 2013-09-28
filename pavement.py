# -*- coding: utf-8 -*-
# pylint: disable=wildcard-import, unused-wildcard-import, invalid-name, unused-import
""" A  set of tools that handle audio (meta-)data and control hi-fi gear.

    This is the main build script for Paver.
"""
# Copyright © 2013 Jürgen Hermann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see {http://www.gnu.org/licenses/}.
import os
import re
import sys

from paver.easy import *
from paver.setuputils import setup
from cobblestones import tools
from setuptools import find_packages


#
# Project Description
#
projectdir = path(__file__).dirname().abspath()
try:
    import kunstkopf
except ImportError:
    # Special bootstrap in our own project, in absence of an initialized virtualenv
    sys.path.insert(0, projectdir / "src")
    import kunstkopf

changelog = (projectdir / "debian" / "changelog").text("UTF-8")
project = tools.bunchify(kunstkopf.pkg_info())
project.update(
    # TODO: find ways to get at these during runtime, within "kunstkopf.pkg_info"
    version = re.search(r"(?<=\()[^)]+(?=\))", changelog).group(), # DRY principle
    packages = find_packages(projectdir / "src", exclude=["tests"]),
)


#
# Tasks
#

@task
@needs(["setuptools.command.develop"])
def init():
    """initial project setup"""


#
# Continuous Integration
#

@task
@needs(["build", "doc"])
def travis_ci():
    """continuous integration tasks for Travis"""


#
# Register with Paver
#
setup(**project)
