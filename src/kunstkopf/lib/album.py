""" Music album, possibly multi-disc.

    Mutagen cheat sheet:

    - EasyID3 or generic File(easy=True) interfaces delivers standardized,
      human-readable keys.
    - Tracks: 'title', 'artist', 'tracknumber', 'genre', and 'composer'.
    - Albums: 'album', 'albumartist', 'date' (or 'year'), 'discnumber',
      and 'organization' (the record label).
    - audio.info.length: playback duration (float in seconds).
    - audio.info.bitrate: data stream speed (int in bits per second).
    - audio.info.sample_rate: frequency of the audio (int in Hertz).
    - audio.info.channels: channel count (int, 1 for mono, 2 for stereo).

    All metadata values are returned as Python lists of strings to seamlessly
    support files that contain multi-valued fields, such as a track featuring
    multiple artists.
"""

import re
import logging
import pathlib

from mutagen import File

AUDIO_EXTENSIONS = {'.flac', '.mp3', '.m4a', '.ogg', '.opus', '.wav'}
ALBUM_FOLDER_RE = [
    re.compile(r"(?P<artist>.+?) \((?P<year>[0-9]{4})\) (?P<name>.+?) \{(?P<flags>.+)\}"),
    re.compile(r"(?P<artist>.+?) \((?P<year>[0-9]{4})\) (?P<name>.+?)"),
]
ALBUM_DISC_RE = re.compile(r"(Disc|CD)\s*\d+", re.IGNORECASE)


def is_audio_file(path):
    """ Check if a file is an audio file based on its extension.
    """
    return path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS


def is_album_folder(path):
    """ Check if a folder is an album folder.

        An album folder contains either audio files, follows the
        ALBUM_FOLDER_RE pattern, or has subfolders named "(Disc|CD)\s*\d+"
        with audio files in them.
    """
    if not path.is_dir():
        return False
    names = list(path.iterdir())
    discs = [x for x in names if x.is_dir() and ALBUM_DISC_RE.match(x.name)]
    if discs:
        return True
    for entry in names:
        if entry.name.startswith('.'):
            continue
        if is_audio_file(entry):
            return True
        if entry.is_dir() and ALBUM_DISC_RE.match(entry.name):
            for subentry in entry.iterdir():
                if subentry.name.startswith('.'):
                    continue
                if is_audio_file(subentry):
                    return True
    return False


class Track:
    """ Music track.
    """

    def __init__(self, path):
        self.path = path
        self.audio = File(self.path, easy=True)
        if self.audio is None:
            raise ValueError(f'Unsupported audio format: {self.path}')
        self.title = ""
        self.artist = ""
        self.album = ""
        self.albumartist = ""
        self.disc_number = 0
        self.track_number = 0

        self._read_meta()

    def _read_meta(self):
        """ Read metadata from the audio file using `mutagen`.
        """
        self.title = self.audio.get('title', [self.path.stem])[0]
        self.artist = self.audio.get('artist', [''])[0]
        self.albumartist = self.audio.get('albumartist', [self.artist])[0]
        self.album = self.audio.get('album', [''])[0]
        self.disc_number = int(self.audio.get('discnumber', [0])[0].split('/')[0])
        self.track_number = int(self.audio.get('tracknumber', [0])[0].split('/')[0])
        self.year = int(self.audio.get('date', [0])[0].split('-')[0])
        self.genres = set(self.audio.get('genre', []))

    def __str__(self):
        pos = (f'{self.disc_number:02d}-{self.track_number:02d}' if self.disc_number
               else f'{self.track_number:02d}')
        return f'{pos}. {self.title}'


class Album:
    """ Music album, possibly multi-disc.
    """

    def __init__(self, path):
        if not is_album_folder(path):
            raise ValueError(f'Not an album directory: {path}')
        self.path = path
        self.name = ""
        self.albumartist = ""
        self.year = 0
        self.flags = set()
        for regex in ALBUM_FOLDER_RE:
            groups = regex.match(path.name)
            if groups:
                groups = groups.groupdict()
                logging.debug(f'🎵 Parsed album folder name: {path.name} -> {groups}')
                self.name = groups.get('name', '')
                self.albumartist = groups.get('artist', '')
                self.year = int(groups.get('year', 0))
                flags = [x.strip() for x in groups.get('flags', '').split(',')]
                self.flags = set(flags) - {''}
                break
        self.tracks = [Track(x) for x in path.rglob('*')
                       if is_audio_file(x) and not x.name.startswith('.')]
        if not self.tracks:
            raise ValueError(f'No audio files found: {path}')
        if not (self.name and self.albumartist and self.year):
            self._read_meta()

        logging.info(f'🔎 {self}\n    '
                     + '\n    '.join(f'{k}: {v}' for k, v in vars(self).items() if k not in {'tracks'})
                     + f'\n    tags: {sorted(self.tracks[0].audio.tags)}\n')

    def _read_meta(self):
        """ Read metadata from first track.
        """
        track = self.tracks[0]
        self.name = track.album
        self.albumartist = track.albumartist or track.artist
        self.year = track.year or self.year

    @property
    def genres(self):
        """ Return a set of genres from all tracks.
        """
        genres = set()
        for track in self.tracks:
            genres.update(track.genres)
        return genres

    def __str__(self):
        flags = ', '.join(sorted(self.flags | self.genres))
        return f'{self.albumartist} ({self.year}) {self.name} {{{flags}}} [{len(self.tracks)}]'
