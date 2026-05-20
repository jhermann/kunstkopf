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

import pathlib

import click

AUDIO_EXTENSIONS = {'.flac', '.mp3', '.m4a', '.ogg', '.opus', '.wav'}

__app_name__ = 'kunstkopf'
CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-q', '--quiet', is_flag=True, default=False, help='Be quiet (show only errors).')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Create extra verbose output.')
def cli(quiet=False, verbose=False): # pylint: disable=unused-argument
    """'kunstkopf' command line tool."""
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
        root_path = pathlib.Path(entry)
        if root_path.is_dir():
            click.echo(f'📂 Scanning: {root_path}')
            matches = [
                pathlib.Path(dirpath) / filename
                for dirpath, _, filenames in root_path.walk()
                for filename in filenames
                if pathlib.Path(filename).suffix.lower() in AUDIO_EXTENSIONS
            ]
        else:
            matches = [root_path]
        for path in matches:
            short_path = path.relative_to(root_path) if len(matches) > 1 else path
            if dry_run:
                click.echo(f'ℹ️ Would clean: {short_path}')
            else:
                click.echo(f'🧹 Cleaning: {short_path}')


if __name__ == "__main__": # imported via "python -m"?
    cli()
