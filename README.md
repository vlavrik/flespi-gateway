# Flespi gateway python library

[![Build Status](https://travis-ci.com/vlavrik/flespi-gateway.svg?branch=main)](https://travis-ci.com/vlavrik/flespi-gateway)
![Read the Docs](https://img.shields.io/readthedocs/flespi-gateway)
![PyPI](https://img.shields.io/pypi/v/flespi-gateway?label=flespi-gateway)

**flespy-gateway** is a python library.

```python
>>> from flespi_gateway.gateway import Device
>>> dv = Device(device_number=device_number, flespi_token=flespi_token)
>>> telemetry = dv.get_telemetry()
>>> print(telemetry)
{'result': [{'id': xxxxxx,
   'telemetry': {'battery.current': {'ts': 1609521935, 'value': 0},
    'battery.voltage': {'ts': 1609521935, 'value': 4.049},
    'can.absolute.load': {'ts': 1609327396, 'value': 23}]
}
```

Flespi gateway allows you to send http requests easily.

## Installing Flespi gateway and Supported Versions

Flespi gateway is available on PyPI:

```console
$ python3 -m pip install flespi-gateway
```

Flespi gateway supports Python 3.8+.

## API Reference and User Guide available on [Read the Docs](https://flespi-gateway.readthedocs.io)
