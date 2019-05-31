
import os
import pytest

import hjsonConfig
import hjson


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_config_files',
    )

def test_main():
    """Tries to run hjsonConfig.main(), which creates and returns an empty and verbose
    HjsonConfig object"""
    config = hjsonConfig.main()

@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, 'test.hjson'))
def test_loading_file(datafiles):
    config = hjsonConfig.HjsonConfig(datafiles)
    assert config["test1"] == "Test String 1"
    assert config["test2"] == "Test String 2"
    assert config["int1"] is type(1)
    assert config["int1"] == 1
    assert config["int4"] == 4
    assert config["float1"] is type (0.5)
    assert config["float1"] == 0.5
    assert config["dict1"] is type(hjson.OrderedDict())
    assert config["overrideMe"] == 0.1
