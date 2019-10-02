#! /usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pprint import pprint

import hjson
import jsonmerge
from pkg_resources import resource_filename


def merge(base, head):
    """Merge two hjsonconfig objects together, using jsonmerge.merge. Keys in
    head overwrite duplicate keys in base.

    Args:
        base: an hjsonconfig or OrderedDict object that represents the
            base of the output.
        head: an hjsonconfig or OrderedDict object to be merged on to the base,
            with duplicated entries overwriting entries in base.

    Returns:
        An hjsonconfig object containing the merged key:value pairs
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
    # hjsonconfig obect rather than an OrderedDict object.
    out = hjsonconfig(verbose=verbose)
    out._copyIn(merged)
    return out


class hjsonconfig(hjson.OrderedDict):
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
    def __init__(self, *args, filename=None, verbose=False, **kwds):
        """Inits hjsonconfig class, sets filename and verbosity and
        reads in config key:value pairs from filename if present."""
        super(hjson.OrderedDict, self).__init__(*args, **kwds)
        self.verbose = verbose
        self.filename = filename
        if filename is not None:
            if self.verbose:
                print("hjsonconfig.__init__: Initializing from {:s}".format(filename))
            self.readFile(filename)

    def _readFile(self, filename):
        """Reads an .hjson configuration file and returns it as a new
        hjsonconfig object

        Args:
            filename: path to file to be read

        Returns:
            An hjsonconfig object, read from filename.
        """
        # Opens use file and assigns corresponding parameters
        if self.verbose:
            print("hjsonconfig._readFile: Reading file: ", filename)
        try:
            f = open(filename, 'r')
            newConfig = hjsonconfig(verbose=self.verbose)
            newConfig._copyIn(hjson.load(f))
            f.close()
            if self.verbose:
                print("hjsonconfig._readFile: Got config:")
                pprint(newConfig)
            newConfig.importConfigFiles()
        except OSError:
            if self.verbose:
                print("hjsonconfig._readFile: OS Error received")
            try:
                # File not found in pwd
                # Look in same directory as current file
                if self.verbose:
                    print("hjsonconfig._readFile: Couldn't find config file: ", filename)
                if self.filename is not None:
                    if self.verbose:
                        print("hjsonconfig._readFile: looking in LabEqupiment/config")
                    newFileName = resource_filename("LabEquipment", "/config/{:s}".format(filename))
                    if self.verbose:
                        print("hjsonconfig._readFile: New filename:", newFileName)
                else:
                    return None

                # check we aren't setting up an infinite loop
                if newFileName != filename:
                    if self.verbose:
                        print("hjsonconfig._readFile: Trying config file: ", newFileName)
                    newConfig = hjsonconfig(filename=newFileName, verbose=self.verbose)
                else:
                    return None
            except OSError:
                if self.verbose:
                    print("hjsonconfig._readFile: File {:s} not found.".format(filename))
                return None
        return newConfig

    def _copyIn(self, odict):
        """Deletes all this objects data and copies in data from odict

        Args:
            odict: an OrderedDict or hjsonconfig object"""
        if odict is not None:
            self.clear()
            for k in odict.keys():
                self[k] = odict[k]
        else:
            pass

    def readFile(self, filename):
        """Reads a config file from the specified file

        Args:
            filename: a filename to read the config file from"""
        # Have to delete data from self and then copy data from readFile return value.
        if self.filename is None:
            if self.verbose:
                print("hjsonconfig.readFile: setting filename: ", filename)
            self.filename = filename
        self._copyIn(self._readFile(filename))

    def importConfigFiles(self):
        """Merges in referenced config files if present.

        Entries in the current config overwrite any entries read from the file.
        This allows this function to be called recursively to build up a complete
        config that refers to default settings stored in default configs.
        """
        # If a config json OrderedDict is passed, merge it with the existing configuration
        # Try and parse a config-file if it is passed to us
        configFile = None
        try:
            if self["config-file"] is not None:
                configFile = self["config-file"]
                if self.verbose:
                    print("hjsonconfig.importConfigFiles: Import from {:s}".format(configFile))

        except KeyError:
            if self.verbose:
                print("hjsonconfig.importConfigFiles: No config-files to import")
            configFile = None

        if configFile is not None:
            # Might be a list of fileNames or a single filename
            if isinstance(configFile, list):
                if self.verbose:
                    print("hjsonconfig.importConfigFiles: Importing config-files {:s}".format(configFile))
                fileConfig = hjsonconfig(verbose=self.verbose)
                for c in configFile:
                    f = self._readFile(c)
                    fileConfig._copyIn(jsonmerge.merge(fileConfig, f))
            else:
                if self.verbose:
                    print("hjsonconfig.importConfigFiles: Importing config-file {:s}".format(configFile))
                fileConfig = hjsonconfig(filename=configFile, verbose=self.verbose)
            if self.verbose:
                pprint(fileConfig)

            # We will move imported config-files to "imported-config-file"
            self["config-file"] = None
            try:
                self["imported-config-file"].append(configFile)
            except KeyError:
                self["imported-config-file"] = [configFile]

            # clear self and copy the merged ODict from jsonmerge in
            self._copyIn(jsonmerge.merge(fileConfig, self))


def main():
    """Creates an empty, verbose hjsonconfig object"""
    config = hjsonconfig(verbose=True)

    return config


if __name__ == "__main__":
    main()
