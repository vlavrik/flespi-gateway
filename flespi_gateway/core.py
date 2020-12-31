"""Getting telemetry
"""
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

    def get_telemetry(self):
        #curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/telemetry'
        """Python wrapper on flesp API to get the latest telemetry json.

        Returns:
        --------
        telemetry: dict
            The latest telemetry from the device.
        """
        response = requests.get('https://flespi.io/gw/devices/{}/telemetry'.format(self.device_number),
                                headers=self.headers)
        telemetry = response.json()['result']
        return telemetry

    def get_snapshots(self):
        # curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/snapshots''
        response = requests.get('https://flespi.io/gw/devices/{}/snapshots'.format(self.device_number),
                                headers=self.headers)
        snapshots = response.json()
        return snapshots['result']

    def get_logs(self):
        # curl -X GET  --header 'Accept: application/json' --header 'Authorization: FlespiToken XXXXXXXXX'  'https://flespi.io/gw/devices/{dev-selector}/logs'
        response = requests.get('https://flespi.io/gw/devices/{}/logs'.format(self.device_number),
                                headers=self.headers)
        logs = response.json()
        return logs['result']
    def get_snapshot(self, snapshot, output):
        pass
