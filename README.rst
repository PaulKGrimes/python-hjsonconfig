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
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-hjsonconfig/badge/?style=flat
    :target: https://readthedocs.org/projects/python-hjsonconfig
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/paulkgrimes/python-hjsonconfig.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/paulkgrimes/python-hjsonconfig

.. |requires| image:: https://requires.io/github/PaulKGrimes/python-hjsonconfig/requirements.svg?branch=master
     :target: https://requires.io/github/PaulKGrimes/python-hjsonconfig/requirements/?branch=master
     :alt: Requirements Status

.. |codecov| .. image:: https://codecov.io/gh/PaulKGrimes/python-hjsonconfig/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/PaulKGrimes/python-hjsonconfig
  :alt: Coverage Status

.. |commits-since| image:: https://img.shields.io/github/commits-since/paulkgrimes/python-hjsonconfig/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/paulkgrimes/python-hjsonconfig/compare/v0.0.0...master


.. end-badges

A package for reading config files written in hjson, with recursive includes of additional files.

* Free software: MIT license

Installation
============

::

    pip install hjsonconfig

Documentation
=============


https://python-hjsonconfig.readthedocs.io/


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
