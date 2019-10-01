import os

import pytest

import hjsonConfig

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_config_files',
    )


def test_main():
    """Tries to run hjsonConfig.main(), which creates and returns an empty and verbose
    hjsonConfig object"""
    config = hjsonConfig.main()
    assert isinstance(config, hjsonConfig.hjsonConfig)


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, 'test.hjson'))
def test_loading_file(datafiles):
    config = hjsonConfig.hjsonConfig(datafiles)
    assert config["test1"] == "Test String 1"
    assert config["test2"] == "Test String 2"
    assert isinstance(config["int1"], int)
    assert config["int1"] == 1
    assert config["int4"] == 4
    assert isinstance(config["float1"], float)
    assert config["float1"] == 0.5
    assert isinstance(config["dict1"], hjsonConfig.hjson.OrderedDict)
    assert config["overrideMe"] == 0.1
