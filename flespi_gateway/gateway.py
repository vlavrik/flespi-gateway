"""The Gateway API (full-stack API for telematics devices) provides methods
to create and manage the flespi telematics hub that jointly provide the
end-to-end communication between the GPS trackers and your target application.
This module covers an API for a Device instance of flespi platform. 

Devices is a virtual representations of the physical trackers on the flespi platform. 
It allows organizing messages by device (ident), remote device configuration, 
dedicated long-term storage, access to telemetry.

More information on `devices <https://flespi.com/flespi-devices>`_ can be
found on official webpage of a platform.

"""


import sys
#import json
import requests


class Device:
    """Registered device represents an IoT or telematics tracking equipment
    capable of sending messages to the channel (an entry point to the telematics hub.
    The most important attributes of a device are device type and configuration.
    Device type corresponds to the device model. Remember, you must have at least
    one channel in the gateway that works over the same protocol as the given device type.
    If you have several channels working over the same protocol, you can connect the device to any of them.
    Device type defines the schema of the device configuration. Device configuration is a JSON object with fields.
    The full description of the devices API under following `link <https://flespi.io/docs/#/gw/devices>`_

    Parameters
    ----------
    flespi_token : str
        Flespi token generated on the flespi platform.
    device_number : int
        Device number integrated with a flespi platform. Device is a GPS tracker.

    Raises
    ------
    AttributeError
        The ``Raises`` section is a list of all exceptions
        that are relevant to the interface.
    ValueError
        If `param2` is equal to `param1`.

    Examples
    --------
    Example of the device initialization.

    >>> from flespi_gateway.gateway import Device
    >>> device_number = 123456
    >>> flespi_token = 'my_flespi_platform_token'
    >>> dv = Device(device_number=device_number, flespi_token=flespi_token)
    """
    def __init__(self, device_number, flespi_token):
        self.device_number = device_number
        self.flespi_token = flespi_token
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'FlespiToken {}'.format(self.flespi_token)}

    def _get_handler(self, link):
        try:
            response = requests.get(link, headers=self.headers)
            if response.status_code == 200:
                print("Success!")
            elif response.status_code == 401:
                print("Unsuccess, reason:")
                print(response.json()['errors'])
                print("Please check your token!")
            elif response.status_code == 403:
                print("Unsuccess, reason:")
                print(response.json()['errors'])
            elif response.status_code == 400:
                print("Unsuccess, reason:")
                print(response.json()['errors'])

            return response.json()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return None

    def _put_handler(self, link):
        pass

    def get_telemetry(self):
        #curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/telemetry'
        """Python wrapper on flesp API to get the latest telemetry json.

        Returns
        -------
        telemetry : dict
            The latest telemetry from the device.

        Examples
        --------
        >>> telemetry = dv.get_telemetry()
        {'result': [{'id': 123456,
        'telemetry': {'battery.current': {'ts': 1609610197, 'value': 0},
        'battery.voltage': {'ts': 1609610197, 'value': 4.043},
        'can.absolute.load': {'ts': 1609605673, 'value': 17},
        'can.ambient.air.temperature': {'ts': 1609605673, 'value': 3}]}
        """
        link = 'https://flespi.io/gw/devices/{}/telemetry'.format(self.device_number)
        telemetry = self._get_handler(link=link)
        return telemetry

    def get_snapshots(self):
        """Snapshots

        Returns
        -------
        snapshots : dict
            The dict object containing the timestamp when 
            the snapshot was created.
        """
        # curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/snapshots''
        link = 'https://flespi.io/gw/devices/{}/snapshots'.format(self.device_number)
        snapshots = self._get_handler(link=link)
        return snapshots

    def get_logs(self):
        # curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/logs'
        link = 'https://flespi.io/gw/devices/{}/logs'.format(self.device_number)
        logs = self._get_handler(link=link)
        return logs
    def get_snapshot(self, snapshot, output):
        """Fetches snapshot file available for device messages.

        Parameters
        ----------
        snapshot : int
            The timestamp of a snapshot created by flespi platform.
            Available snapshots are fetched vy calling `get_snapshots()`
            class method.
        output : str
            A file name where to save fetched snapshot.

        Examples
        --------
        Fetching one of available snapshots.

        >>> dv.get_snapshot(1609610197, 'latest_dataset.json')
        """
        #curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/snapshots/{snapshot-selector}'
        # link = 'https://flespi.io/gw/devices/{}/snapshots/{}'.format(self.device_number, snapshot)
        # print(link)
        # snapshot = self._get_handler(link=link)
        # print(type(snapshot))
        # print(len(snapshot))

        # with open(output + '.json', 'w') as f:
        #     json.dump(snapshot, f)

        # return None
        #TODO resolve a problem with saving response properly
        pass

    def get_devices(self, all_devices=False):
        #curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/all'
        if all_devices:
            link = "https://flespi.io/gw/devices/all"
        else:
            link = "https://flespi.io/gw/devices/{}".format(self.device_number)

        devices = self._get_handler(link=link)
        return devices
