#! /usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pprint import pprint

import hjson
import jsonmerge


def merge(base, head):
    """Merge two HjsonConfig objects together, using jsonmerge.merge. Keys in
    head overwrite duplicate keys in base.

    Args:
        base: an HjsonConfig or OrderedDict object that represents the
            base of the output.
        head: an HjsonConfig or OrderedDict object to be merged on to the base,
            with duplicated entries overwriting entries in base.

    Returns:
        An HjsonConfig object containing the merged key:value pairs
    """
    try:
        if base is not None:
            verbose = base.verbose or head.verbose
        else:
            verbose = head.verbose
    except AttributeError:
        verbose = False

    merged = jsonmerge.merge(base, head)

    # We copy merged into out, to ensure that the returned value is an
    # HjsonConfig obect rather than an OrderedDict object.
    out = HjsonConfig(verbose=verbose)
    out._copy_in(merged)
    return out


class HjsonConfig(hjson.OrderedDict):
    """A class to handle reading configurations in hjson files, which
    may include references to other hjson files via "config-file" entries.

    On reading the hjson file with readFile, the class looks for "config-file"
    entries and imports their contents as well.  Entries duplicated in the top
    level file override the entries in an included file.

    The key:value pairs read from the config files are made available via the
    standard python dictionary interface.  The order the keys are read from the
    config file is preserved.  See the hjson documentation at
    https://github.com/hjson/hjson-py

    Attributes:
        verbose: A boolean indicating if extra output should be given. Very
                helpful for tracking down errors in the imports.
        filename: The name of the config file last imported. Helps provide a
                basic check for recursive loops of config files
    """
    def __init__(self, *args, **kwds):
        """Inits HjsonConfig class, sets filename and verbosity and
        reads in config key:value pairs from filename if present."""
        # Use try and except to parse **kwds, so that python 2.7 should work like python 3
        try:
            self.verbose = kwds["verbose"]
        except KeyError:
            self.verbose = False
        try:
            self.filename = kwds["filename"]
        except KeyError:
            self.filename = None

        super(hjson.OrderedDict, self).__init__(*args, **kwds)

        if self.filename is not None:
            if self.verbose:
                print("HjsonConfig.__init__: Initializing from {:s}".format(self.filename))
            self.read_file(self.filename)

    def _read_file(self, filename):
        """Reads an .hjson configuration file and returns it as a new
        HjsonConfig object

        Args:
            filename: path to file to be read

        Returns:
            An HjsonConfig object, read from filename.
        """
        # Opens use file and assigns corresponding parameters
        if self.verbose:
            print("HjsonConfig._readFile: Reading file: ", filename)

        f = open(filename, 'r')
        newConfig = HjsonConfig(verbose=self.verbose)
        newConfig._copy_in(hjson.load(f))
        f.close()
        if self.verbose:
            print("HjsonConfig._readFile: Got config:")
            pprint(newConfig)
        newConfig.import_config_files()

        return newConfig

    def _copy_in(self, odict):
        """Deletes all this objects data and copies in data from odict

        Args:
            odict: an OrderedDict or HjsonConfig object"""
        if odict is not None:
            self.clear()
            for k in odict.keys():
                self[k] = odict[k]
        else:
            pass

    def read_file(self, filename):
        """Reads a config file from the specified file

        Args:
            filename: a filename to read the config file from"""
        # Have to delete data from self and then copy data from readFile return value.
        if self.filename is None:
            if self.verbose:
                print("HjsonConfig.readFile: setting filename: ", filename)
            self.filename = filename
        self._copy_in(self._read_file(filename))

    def import_config_files(self):
        """Merges in referenced config files if present.

        Entries in the current config overwrite any entries read from the file.
        This allows this function to be called recursively to build up a complete
        config that refers to default settings stored in default configs.
        """
        # If a config json OrderedDict is passed, merge it with the existing configuration
        # Try and parse a config-file if it is passed to us
        config_file = None
        try:
            if self["config-file"] is not None:
                config_file = self["config-file"]
                if self.verbose:
                    print("HjsonConfig.importConfigFiles: Import from {:s}".format(config_file))

        except KeyError:
            if self.verbose:
                print("HjsonConfig.importConfigFiles: No config-files to import")
            config_file = None

        if config_file is not None:
            # Might be a list of fileNames or a single filename
            if isinstance(config_file, list):
                if self.verbose:
                    print("HjsonConfig.importConfigFiles: Importing config-files {:s}".format(config_file))
                file_config = HjsonConfig(verbose=self.verbose)
                for c in config_file:
                    f = self._read_file(c)
                    file_config._copy_in(jsonmerge.merge(file_config, f))
            else:
                if self.verbose:
                    print("HjsonConfig.importConfigFiles: Importing config-file {:s}".format(config_file))
                file_config = HjsonConfig(filename=config_file, verbose=self.verbose)
            if self.verbose:
                pprint(file_config)

            # We will move imported config-files to "imported-config-file"
            self["config-file"] = None
            try:
                self["imported-config-file"].append(config_file)
            except KeyError:
                self["imported-config-file"] = [config_file]

            # clear self and copy the merged ODict from jsonmerge in
            self._copy_in(jsonmerge.merge(file_config, self))


def main():
    """Creates an empty, verbose HjsonConfig object"""
    config = HjsonConfig(verbose=True)

    return config


if __name__ == "__main__":
    main()
