# -*- coding: utf-8 -*-
""" kunstkopf [ˈkʊnstkɔp͜f] is a set of tools that handle audio (meta-)data and control hi-fi gear.

    Copyright © 2013 Jürgen Hermann

    Licensed under the GNU General Public License, Version 3.0
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

def pkg_info():
    """Return project information for setuptools."""
    try:
        doc = __doc__.decode("UTF-8")
    except (AttributeError, UnicodeError):
        doc = __doc__ # Python3, or some strangeness

    return dict(
        # project data & layout
        name = __name__.split('.')[0],
        ## TODO: version = re.search(r"(?<=\()[^)]+(?=\))", changelog).group(),
        package_dir = {"": "src"},
        ## TODO: packages = find_packages(projectdir / "src", exclude=["tests"]),
        test_suite = "nose.collector",
        zip_safe = True,
        include_package_data = True,
        data_files = [
            ("EGG-INFO", [
                "README.md", "LICENSE", "debian/changelog",
            ]),
        ],

        # dependency management
        install_requires = [
            "mutagen",
        ],
        setup_requires = [
            "docutils",
            "Sphinx",
        ],
        extras_require = {
        },

        # PyPI
        url = "https://github.com/jhermann/kunstkopf",
        license = "GNU General Public License Version 3.0",
        keywords = "python audio tool tagging indexing searching syncing",
        author = u"Jürgen Hermann",
        author_email = "jh@web.de",
        description = doc.split('.')[0].strip(),
        long_description = doc.split('.', 1)[1].strip(),
        classifiers = [
            # values at http://pypi.python.org/pypi?:action=list_classifiers
            "Development Status :: 3 - Alpha",
            #"Development Status :: 4 - Beta",
            #"Development Status :: 5 - Production/Stable",
            "Operating System :: OS Independent",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.7",
            "Topic :: Multimedia :: Sound/Audio",
            "Topic :: Multimedia :: Sound/Audio :: Players",
            "Topic :: Text Processing :: Indexing",
            "Topic :: Utilities",
        ],
    )
