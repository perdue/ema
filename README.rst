===========
EMA Analyze
===========


.. image:: https://img.shields.io/pypi/v/ema.svg
        :target: https://pypi.python.org/pypi/ema

.. image:: https://img.shields.io/travis/perdue/ema.svg
        :target: https://travis-ci.org/perdue/ema

.. image:: https://readthedocs.org/projects/ema/badge/?version=latest
        :target: https://ema.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Package to download my solar panel production data.


* Free software: MIT license
* Documentation: https://ema.readthedocs.io.

===========
Set Up
===========
clone

pipenv

===========
Configuration
===========

A configuration file (``config.yaml``) is included that contains default parameters.
The EMA connection-specific parameters are supplied through
environment variables.  Google Drive credentials file locations are
also provided through environment variables.

Encryption of EMA Paramaters
-------

The EMA parameters are assumed to be encrypted.
A command line utility (``encrypt.py``) is provided to create files that
contain the encrypted environment variables.

To generate new files:

::



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
