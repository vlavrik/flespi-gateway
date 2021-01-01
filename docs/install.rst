.. _install:

Installation of Flespi Gateway
==============================

This part of the documentation covers the installation of flespi-gateway.
The first step to using any software package is getting it properly installed.


PyPi installation of flespi-gateway
---------------------------------------

To install flespi-gateway, run the following command in your terminal of choice::

    $ python3 -m pip install flespi-gateway

Get the Source Code
-------------------

flespi-gateway is actively developed on GitHub, where the code is
`always available <https://github.com/vlavrik/flespi-gateway>`_.

You can either clone the public repository::

    $ git clone git://github.com/vlavrik/flespi-gateway.git

Or, download the `tarball <https://codeload.github.com/vlavrik/flespi-gateway/legacy.tar.gz/main>`_::

    $ curl -OL https://github.com/vlavrik/flespi-gateway/tarball/master
    # optionally, zipball is also available (for Windows users).

Once you have a copy of the source, you can embed it in your own Python
package, or install it into your site-packages easily::

    $ cd flespi-gateway
    $ python3 -m pip install .