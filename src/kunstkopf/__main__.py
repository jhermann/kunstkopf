# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Command line interface.
"""
# Copyright ©  2015, 2026 Jürgen Hermann <jh@web.de>
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

import logging
import pathlib

import click

from .lib.scan import MusicFolder
from .lib.album import Album, is_album_folder

__app_name__ = 'kunstkopf'
CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-q', '--quiet', is_flag=True, default=False, help='Be quiet (show only errors).')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Create extra verbose output.')
def cli(quiet=False, verbose=False): # pylint: disable=unused-argument
    """'kunstkopf' command line tool."""
    if verbose:
        log_level = logging.DEBUG
    elif quiet:
        log_level = logging.ERROR
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level)
    appdir = click.get_app_dir(__app_name__)
    #click.secho(f'appdir = {appdir}', fg='yellow')


@cli.command()
def help():
    """Print some helpful message."""
    click.echo('Helpful message.')


@cli.group(context_settings=CONTEXT_SETTINGS)
def meta():
    """Commands for audio metadata handling."""


@meta.command()
@click.argument('paths', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('-n', '--dry-run', is_flag=True, default=False, help='Show what would be done without making changes.')
def clean(paths, dry_run):
    """Remove non-standard tags from audio PATHS (files or directories)."""
    for entry in paths:
        entry = pathlib.Path(entry).resolve()
        click.echo(f'📂 Scanning: {entry}')
        if is_album_folder(entry):
            albums = [Album(entry)]
        else:
            root_path = MusicFolder(entry)
            albums = root_path.scan()
        for album in albums:
            short_path = album.path.relative_to(entry)
            if dry_run:
                click.echo(f'ℹ️ Would clean: {album} @ {short_path}')
            else:
                click.echo(f'🧹 Cleaning: {album} @ {short_path}')


if __name__ == "__main__": # imported via "python -m"?
    cli()
