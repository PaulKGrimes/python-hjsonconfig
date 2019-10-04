========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |codecov|
    * - package
      - | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-HjsonConfig/badge/?style=flat
    :target: https://readthedocs.org/projects/python-HjsonConfig
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/paulkgrimes/python-HjsonConfig.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/paulkgrimes/python-HjsonConfig

.. |requires| image:: https://requires.io/github/PaulKGrimes/python-HjsonConfig/requirements.svg?branch=master
     :target: https://requires.io/github/PaulKGrimes/python-HjsonConfig/requirements/?branch=master
     :alt: Requirements Status

.. |codecov| image:: https://codecov.io/gh/PaulKGrimes/python-HjsonConfig/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/PaulKGrimes/python-HjsonConfig
  :alt: Coverage Status

.. |commits-since| image:: https://img.shields.io/github/commits-since/paulkgrimes/python-HjsonConfig/v0.0.3.svg
    :alt: Commits since latest release
    :target: https://github.com/paulkgrimes/python-HjsonConfig/compare/v0.0.3...master


.. end-badges

A package for reading config files written in hjson, with recursive includes of additional files.

* Free software: MIT license

Installation
============

::

    pip install HjsonConfig

Documentation
=============


https://python-HjsonConfig.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
