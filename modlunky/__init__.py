#!/usr/bin/env python

import io
import os

from .version import __version__

__author__ = "Gary M. Josack <gary@byoteki.com>"


class Error(Exception):
    """ Base class for all modlunky exceptions."""


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


def build_index(unpacked_dir):
    """ Crawls a previous unpacked directory and builds an index file."""
    groups = []
    # Files can be repeated. Keep a dict of what we've seen.
    files = {}
    offset = 0

    for group_dir in sorted(os.listdir(unpacked_dir)):
        group = Group(group_dir.split("-")[1])
        files_dir = os.path.join(unpacked_dir, group_dir)
        for spelunky_file in sorted(os.listdir(files_dir)):
            orig_name = spelunky_file.split("-", 2)[1]
            if orig_name in files:
                group.files.append(files[orig_name])
                continue
            file_path = os.path.join(files_dir, spelunky_file)
            file_stat = os.stat(file_path)
            file_size = file_stat.st_size
            spelunky_file = SpelunkyFile(orig_name, offset, file_size)
            group.files.append(spelunky_file)
            files[orig_name] = spelunky_file
            offset += file_size
        groups.append(group)

    return groups


def write_index(index, output_filename, force=False):
    """ Given an index structure write out a wad.wix file."""
    output = ""
    for group in index:
        output += "!group %s\r\n" % group.name
        for spelunky_file in group.files:
            output += "%s %s %s\r\n" % (spelunky_file.filename,
                                     spelunky_file.offset,
                                     spelunky_file.size)

    if os.path.isfile(output_filename) and not force:
        raise Error("%s already exists and not forced." % output_filename)

    with io.open(output_filename, "wb") as output_file:
        output_file.write(output)


def pack_wad(index, output_filename, unpack_dir, force=False):
    filenames = set()

    if os.path.isfile(output_filename) and not force:
        raise Error("%s already exists and not forced." % output_filename)

    with io.open(output_filename, "wb") as data_file:
        for g_idx, group in enumerate(index):
            group_dir = os.path.join(unpack_dir, "%04d-%s" % (g_idx, group.name))
            for f_idx, spelunky_file in enumerate(group.files):
                file_path = os.path.join(group_dir, "%04d-%s" % (f_idx, spelunky_file.filename))
                if spelunky_file.filename in filenames:
                    continue
                data_file.seek(spelunky_file.offset)
                with io.open(file_path, "rb") as s_file:
                    data_file.write(s_file.read())
                filenames.add(spelunky_file.filename)


def unpack_wad(index, data_filename, unpack_dir):
    with io.open(data_filename, "rb") as data_file:
        for g_idx, group in enumerate(index):
            group_dir = os.path.join(unpack_dir, "%04d-%s" % (g_idx, group.name))
            if not os.path.isdir(group_dir):
                os.mkdir(group_dir)
            for f_idx, spelunky_file in enumerate(group.files):
                file_path = os.path.join(group_dir, "%04d-%s" % (f_idx, spelunky_file.filename))
                data_file.seek(spelunky_file.offset)
                data = data_file.read(spelunky_file.size)
                write_spelunky_file(file_path, data)


def write_spelunky_file(path, data):
    with io.open(path, "wb") as spelunky_file:
        spelunky_file.write(data)

