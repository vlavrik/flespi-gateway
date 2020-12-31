"""Getting telemetry
"""


import sys
import json
import requests


class Gateway:
    """Flespi gateway methods.

    Parameters:
    -----------
    flespi_token: str
        Flespi token generated on the flespi platform.
    device_number : int
        Device number integrated with a flespi platform. Device is a GPS tracker.
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

        Returns:
        --------
        telemetry: dict
            The latest telemetry from the device.
        """
        link = 'https://flespi.io/gw/devices/{}/telemetry'.format(self.device_number)
        telemetry = self._get_handler(link=link)
        return telemetry

    def get_snapshots(self):
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
