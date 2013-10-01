#!/usr/bin/env python

import io
import os

from .version import __version__

__author__ = "Gary M. Josack <gary@byoteki.com>"


class Group(object):
    """ Represents a group from a Spelunky index."""
    def __init__(self, name, files=None):
        self.name = name
        self.files = files if files else []

    def __repr__(self):
        return "Group(name=%r, files=%r)" % (self.name, self.files)


class SpelunkyFile(object):
    """ Represents a Spelunky media file."""
    def __init__(self, filename, offset, size):
        self.filename = filename
        self.offset = int(offset)
        self.size = int(size)

    def __repr__(self):
        return "SpelunkyFile(filename=%r, offset=%r, size=%r)" % (self.filename, self.offset, self.size)


def read_index(index_filename):
    """ Reads a wad.wix an returns a structured index."""
    groups = []

    with io.open(index_filename) as index_file:
        group = None
        for line in index_file:
            line = line.strip()
            if not line:
                continue
            if "!group" in line:
                group = Group(line.split()[1])
                groups.append(group)
                continue
            group.files.append(SpelunkyFile(*line.split()))

    return groups


def unpack(index, data_filename, output_dir):
    with io.open(data_filename, "rb") as data_file:
        for idx, group in enumerate(index):
            group_dir = os.path.join(output_dir, "%03d-%s" % (idx, group.name))
            if not os.path.isdir(group_dir):
                os.mkdir(group_dir)
            for spelunky_file in group.files:
                file_path = os.path.join(group_dir, spelunky_file.filename)
                data_file.seek(spelunky_file.offset)
                data = data_file.read(spelunky_file.size)
                write_spelunky_file(file_path, data)


def write_spelunky_file(path, data):
    with io.open(path, "wb") as spelunky_file:
        spelunky_file.write(data)

