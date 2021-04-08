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
import json
import requests
from flespi_gateway.logger import logger



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
    TypeError
        Device number must be integer!

    TypeError
        Flespi token must be string!

    ValueError
        The length of token must be 64 characters!

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
        if type(self.device_number) is not int:
            raise TypeError("Device number must be integer!")
        self.flespi_token = flespi_token
        if type(self.flespi_token) is not str:
            raise TypeError("Token must be string!")
        elif (type(self.flespi_token) is str) and (len(self.flespi_token) != 64):
            raise ValueError("The length of token must be 64 characters!")
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'FlespiToken {}'.format(self.flespi_token)}

    def _get_handler(self, link, params=None):
        try:
            response = requests.get(link, params, headers=self.headers)
            if response.status_code == 200:
                logger.info('Success!')
            elif response.status_code == 401:
                status_message = response.json()['errors'][0]['reason']
                logger.error(f"Unsuccess! Reason: {status_message}")
                logger.info("Please check your token!")
            elif response.status_code == 403:
                print("Unsuccess, reason:")
                print(response.json()['errors'])
            elif response.status_code == 400:
                print("Unsuccess, reason:")
                logger.warning('test warning')
                print(response.json()['errors'])

            return response.json()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        return None

    def _put_handler(self, link):
        pass

    def get_logs(self):
        """Get logs for specified device.
        The request without parameters will return all logs records.
        By default retreieves all logs. Filtering by parameters
        is not imlemented

        Returns
        -------
        logs : dict
            Logs for a specific device.
        """
        # curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/logs'
        link = 'https://flespi.io/gw/devices/{}/logs'.format(self.device_number)
        logs = self._get_handler(link=link)
        return logs

    def get_settings(self, all=True):
        """Get collection of settings matching filter parameters.
        By default retreieves all settings. Filtering by parameters
        is not implemented.

        Parameters
        ----------
        all : bool
            Indicates of all settings retreival.

        Returns
        -------
        settings : dict
            Setting of a cpecified device.
        """
        # curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/settings/{sett-selector}'
        if all:
            link = 'https://flespi.io/gw/devices/{}/settings/all'.format(self.device_number)
            settings = self._get_handler(link=link)
            return settings
        else:
            raise NotImplementedError

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
        # curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/snapshots/{snapshot-selector}'
        # link = 'https://flespi.io/gw/devices/{}/snapshots/{}'.format(self.device_number, snapshot)
        # print(link)
        # snapshot = self._get_handler(link=link)
        # print(type(snapshot))
        # print(len(snapshot))

        # with open(output + '.json', 'w') as f:
        #     json.dump(snapshot, f)

        # return None
        # TODO resolve a problem with saving response properly

    def get_messages(self, params=None):
        # curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/messages'
        """Get specified device messages. The request without
        parameters will return all device messages.
        Reply contains sorted by time messages, in case
        you request messages from multiple devices simulateniously
        they are not sorted by device.

        Parameters
        ----------
        params : dict
            Dictionary with filter parameters.

        Returns
        -------
        messages : dict
            Messages with telemetry and gps data.

        Examples
        --------
        Example of a data retrieveng within a certain time
        period. The data are sorted according to timestamp.
        The full description of parameters can be found `here <https://flespi.io/docs/#/gw/devices/get_devices_dev_selector_messages>`_

        >>> params = {'from': 1609581600 , 'to': 1609588800, 'reverse': True}
        >>> messages = get_messages(params=params)
        >>> print(messages['result'][100])
        {'battery.current': 0, 'battery.voltage': 4.044, 'can.absolute.load': 70,
        'can.ambient.air.temperature': 3 ... }
        """
        link = "https://flespi.io/gw/devices/{}/messages".format(self.device_number)
        if params:
            params = (('data', '{}'.format(json.dumps(params))),)
            messages = self._get_handler(link=link, params=params)
        else:
            messages = self._get_handler(link=link, params=None)
        return messages

    def get_telemetry(self):
        # curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/telemetry'
        """Get specified device telemetry - e.g. latest values of parameters
        from registered messages. Telemetry is updated
        automatically during new messages reception for a device.

        Returns
        -------
        telemetry : dict
            The latest telemetry from the device.

        Examples
        --------
        >>> telemetry = dv.get_telemetry()
        >>> print(telemetry)
        {'result': [{'id': 123456,
        'telemetry': {'battery.current': {'ts': 1609610197, 'value': 0},
        'battery.voltage': {'ts': 1609610197, 'value': 4.043},
        'can.absolute.load': {'ts': 1609605673, 'value': 17},
        'can.ambient.air.temperature': {'ts': 1609605673, 'value': 3}]}
        """
        link = 'https://flespi.io/gw/devices/{}/telemetry'.format(self.device_number)
        telemetry = self._get_handler(link=link)
        return telemetry

    def get_devices(self, all=False):
        """Fetches a collection of devices matching filter parameters.
        By defaults retreieves all devices.

        Parameters
        ----------
        all : bool
            Defaults to `False`. In this case
            only initialized device will be returned.

        Returns
        -------
        devices : dict
            Fetched devices.
        """
        # curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/all'
        if all:
            link = "https://flespi.io/gw/devices/all"
        else:
            link = "https://flespi.io/gw/devices/{}".format(self.device_number)

        devices = self._get_handler(link=link)
        return devices

    def get_snapshots(self):
        """List of archived messages snapshots available for a device.

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
