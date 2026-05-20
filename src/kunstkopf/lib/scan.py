""" Scan file system for audio files.
"""
import re
import pathlib

from .album import Album, is_album_folder


class MusicFolder:
    """ A nested music folder, with albums as the leaves.
    """

    def __init__(self, path: str|pathlib.Path):
        self.path = pathlib.Path(path)

    def scan(self):
        """ Recursively scan the folder for audio files and yield Album objects.

            Folders can be nested, album directories are recognized using the
            is_album_folder() function.
        """
        for entry in sorted(self.path.iterdir()):
            if entry.name.startswith('.'):
                continue
            if entry.is_dir():
                if is_album_folder(entry):
                    album = Album(entry)
                    yield album
                else:
                    subfolder = MusicFolder(entry)
                    yield from subfolder.scan()
