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


import logging
import json
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
    device_number : int
        The unique identifier for the device within the Flespi platform.
    flespi_token : str
        A valid Flespi token for authentication with the Flespi API.

    Attributes
    ----------
    device_number : int
        The device's unique identifier.
    flespi_token : str
        The authentication token for the Flespi API.
    headers : dict
        HTTP headers to include in requests to the Flespi API.
    base_url : str
        The base URL for the Flespi API endpoints related to devices.

    Raises
    ------
    TypeError
        If `device_number` is not an integer or `flespi_token` is not a string.
    ValueError
        If `flespi_token` is not exactly 64 characters long.

    Examples
    --------
    >>> device_number = 123456
    >>> flespi_token = 'your_flespi_token_here'
    >>> device = Device(device_number=device_number, flespi_token=flespi_token)
    >>> print(device.get_logs())
    {'logs': [...]}

    Methods
    -------
    get_logs()
        Fetch and return logs for the specified device.
    get_settings(all=True)
        Retrieve settings for the device, optionally filtered by parameters.
    get_messages(params=None)
        Get messages for the device, optionally filtered by parameters.
    get_telemetry()
        Fetch the latest telemetry data for the device.
    get_devices(all=False)
        Retrieve a list of devices, optionally including all devices on the account.
    get_snapshots()
        List available message snapshots for the device.
    get_snapshot(output)
        Fetch the latest snapshot file for the device and save it to a specified file.
    """

    def __init__(self, device_number, flespi_token):
        """
        Constructs all the necessary attributes for the Device object.

        Parameters
        ----------
        device_number : int
            The unique identifier for the device within the Flespi platform.
        flespi_token : str
            A valid Flespi token for authentication with the Flespi API.

        Raises
        ------
        TypeError
            If `device_number` is not an integer or `flespi_token` is not a string.
        ValueError
            If `flespi_token` is not exactly 64 characters long.
        """
        if not isinstance(device_number, int):
            raise TypeError("Device number must be an integer!")
        if not isinstance(flespi_token, str) or len(flespi_token) != 64:
            raise ValueError("Token must be a 64-character string!")

        self.device_number = device_number
        self.flespi_token = flespi_token
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'FlespiToken {self.flespi_token}'
        }
        self.base_url = "https://flespi.io/gw/devices/"

    def _build_url(self, endpoint):
        return f"{self.base_url}{self.device_number}/{endpoint}"

    def _perform_get_request(self, link, params=None):
        """Perform a GET request to the specified link with optional parameters."""
        try:
            response = requests.get(link, params=params, headers=self.headers)
            return self._process_response(response)
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise

    def _process_response(self, response):
        """Process the HTTP response, logging errors and returning data as needed."""
        if response.status_code == 200:
            logging.info('Success')
            return response
        elif response.status_code in [400, 401, 403]:
            error_info = response.json().get('errors', 'Unknown error')
            logging.error(
                f"Unsuccessful request. Status code: {response.status_code}, Reason: {error_info}")
        else:
            logging.error(
                f"Unexpected status code received: {response.status_code}")
        return None

    def _put_handler(self, link):
        pass

    # Manage
    def get_devices(self, all=False):
        """
        Retrieve a collection of devices available to the user identified by the token.

        This method fetches devices from the Flespi platform. By default, it retrieves only initialized devices. However, by setting the `all` parameter to True, it can be configured to fetch all devices associated with the user's account, regardless of their initialization status.

        Parameters
        ----------
        all : bool, optional
            If set to True, the method retrieves all devices associated with the user's account. If False (default), only initialized devices are retrieved.

        Returns
        -------
        devices : dict or None
            A dictionary containing the devices available to the user. The structure of the dictionary includes device identifiers and possibly other metadata about each device. Returns None if an error occurred during the request.

        Examples
        --------
        >>> device = Device(device_number=123456, flespi_token='your_flespi_token_here')
        >>> all_devices = device.get_devices(all=True)
        >>> print(all_devices)
        {'devices': [{'id': 123, 'name': 'Device 1'}, {'id': 456, 'name': 'Device 2'}]}

        >>> initialized_devices = device.get_devices()
        >>> print(initialized_devices)
        {'devices': [{'id': 123, 'name': 'Device 1'}]}

        Notes
        -----
        The actual structure and content of the returned devices dictionary may vary depending on the data available on the Flespi platform for the user's account. It's important to check the Flespi API documentation for the most current response format.
        """
        link = "https://flespi.io/gw/devices/all" if all else f"https://flespi.io/gw/devices/{self.device_number}"
        return self._perform_get_request(link).json()

    # History and State
    def get_messages(self, params=None):
        """
        Retrieve messages currently accumulated in the device storage.

        This method accesses the device's message storage on the Flespi platform to retrieve messages. By default, without specifying any parameters, it returns all messages currently stored for the device. The storage and retention of messages are governed by the 'messages_ttl' (time to live) and 'messages_rotate' fields in the device configuration, which define the duration and quantity of messages stored, respectively.

        The 'params' argument allows for filtering and customization of the query, supporting operations like searching for specific messages, retrieving all messages, and performing basic generalization mathematics through the 'generalize' API call parameter.

        Parameters
        ----------
        params : dict, optional
            A dictionary containing parameters to filter and customize the message retrieval. Supports a wide range of filtering options, including time ranges, message types, and the 'generalize' parameter for data aggregation and simplification. If None (default), all stored messages for the device are retrieved.

        Returns
        -------
        messages : dict or None
            A dictionary containing the retrieved messages, sorted by timestamp. If messages are requested from multiple devices simultaneously, the output will not have a specific sort order. Returns None if an error occurred during the request.

        Examples
        --------
        >>> params = {'from': 1609581600, 'to': 1609588800, 'fields': 'position,speed', 'generalize': 'avg,60'}
        >>> messages = device.get_messages(params=params)
        >>> print(messages)
        {'messages': [{'timestamp': 1609581700, 'position': {...}, 'speed': 45}, ...]}

        Notes
        -----
        - The structure and content of the returned messages dictionary may vary depending on the data available on the Flespi platform for the user's account and the specified parameters.
        - The 'messages_ttl' and 'messages_rotate' configuration fields of the device determine the longevity and volume of messages stored, impacting the availability of historical data.
        - When retrieving messages from multiple devices simultaneously, consider implementing client-side sorting if a specific order is required.

        See Also
        --------
        get_settings : For retrieving the current configuration of the device, including 'messages_ttl' and 'messages_rotate' fields.
        """
        link = self._build_url('messages')
        messages = self._perform_get_request(link=link)
        return messages.json()

    def get_telemetry(self):
        """
        Retrieve selected telemetry fields for the specified device.

        This method fetches the latest cached values of telemetry fields for the device identified by the device number. Telemetry fields represent the last known value of each message parameter that was received by the device. These values are collected and updated automatically during the registration of device messages and are stored for up to 1 year for each device.

        Parameters
        ----------
        None

        Returns
        -------
        telemetry : dict or None
            A dictionary containing the latest telemetry data for the specified device, including the timestamp and value for each telemetry field. Returns None if an error occurred during the request.

        Examples
        --------
        >>> telemetry = device.get_telemetry()
        >>> print(telemetry)
        {'telemetry': {'battery.level': {'ts': 1610000000, 'value': 95},
                    'temperature': {'ts': 1610000200, 'value': 22},
                    ...}}

        Notes
        -----
        - The actual structure and content of the returned telemetry dictionary may vary depending on the data available on the Flespi platform for the user's account.
        - Telemetry data is useful for monitoring the current state and performance of the device without needing to retrieve and process the entire message history.
        - Since telemetry data is updated with every received message, it provides a near real-time overview of the device's status.

        See Also
        --------
        get_messages : For retrieving the historical messages that contribute to the telemetry data.
        """
        link = self._build_url('telemetry/all')
        return self._perform_get_request(link).json()

    # Connections
    def get_connections(self):
        """
        Retrieve a list of all currently active TCP connections for the specified device.

        This method fetches information about active TCP connections from the Flespi platform for the device identified by the device number. It provides details on each connection, including start times, end times (if applicable), and the current status of the connection. This can be useful for monitoring the device's communication status and diagnosing connectivity issues.

        Parameters
        ----------
        None

        Returns
        -------
        connections : dict or None
            A dictionary containing details of all active TCP connections for the specified device, including timestamps, connection status, and other relevant information. Returns None if an error occurred during the request or if there are no active connections.

        Examples
        --------
        >>> connections = device.get_connections()
        >>> print(connections)
        {'connections': [{'start_ts': 1610000000, 'end_ts': 1610000600, 'status': 'active'},
                        {'start_ts': 1610005000, 'end_ts': 1610005600, 'status': 'closed'},
                        ...]}

        Notes
        -----
        - The actual structure and content of the returned connections dictionary may vary depending on the data available on the Flespi platform for the user's account.
        - Active connections are those that are currently open and transmitting data. Closed connections may also be listed if they were active recently.

        See Also
        --------
        get_messages : For retrieving messages that may have been transmitted during these connections.
        """
        link = self._build_url('connections/all')
        return self._perform_get_request(link).json()

    # Utils
    def get_logs(self, params={'data': '{"from":1702303046,"to":1702317898}'}):
        """
        Fetch and return logs for the specified device.

        This method retrieves logs from the Flespi platform for the device identified by the device number. The logs include various operational and diagnostic information that can be useful for troubleshooting and monitoring the device's performance. Logs are sorted by timestamp for a single device query. However, when requesting logs from multiple devices simultaneously, the logs are not sorted by device.

        Parameters
        ----------
        None

        Returns
        -------
        logs : dict or None
            A dictionary containing the logs for the specified device, sorted by timestamp. Each log entry includes details such as the log level, message, and timestamp. Returns None if an error occurred during the request or if there are no logs available.

        Examples
        --------
        >>> logs = device.get_logs()
        >>> print(logs)
        {'logs': [{'timestamp': 1610000000, 'level': 'info', 'message': 'Device connected'},
                {'timestamp': 1610000020, 'level': 'warning', 'message': 'Low battery'},
                ...]}

        Notes
        -----
        - The structure and content of the returned logs dictionary may vary depending on the data available on the Flespi platform for the user's account.
        - Logs are an essential tool for diagnosing issues and understanding the behavior of the device over time.

        See Also
        --------
        get_messages : For retrieving messages that may have been logged as part of the device's operation.
        """
        link = self._build_url('logs')
        return self._perform_get_request(link=link, params=params).json()

    def get_packets(self, params={'data': '{"from":1702303046,"to":1702317898}'}):
        """
        Fetch and return packets for the specified device.

        This method retrieves packets from the Flespi platform for the device identified by the device number. The packets include various operational and diagnostic information that can be useful for troubleshooting and monitoring the device's performance. Packets are sorted by timestamp for a single device query. However, when requesting packets from multiple devices simultaneously, the packets are not sorted by device.

        Parameters
        ----------
        None

        Returns
        -------
        packets : dict or None
            A dictionary containing the packets for the specified device, sorted by timestamp. Each packet entry includes details such as the packet level, message, and timestamp. Returns None if an error occurred during the request or if there are no packets available.

        Examples
        --------
        >>> packets = device.get_packets()
        >>> print(packets)
        {'packets': [{'timestamp': 1610000000, 'level': 'info', 'message': 'Packet received'},
                {'timestamp': 1610000020, 'level': 'warning', 'message': 'Packet loss'},
                ...]}

        Notes
        -----
        - The structure and content of the returned packets dictionary may vary depending on the data available on the Flespi platform for the user's account.
        - Packets are an essential tool for diagnosing issues and understanding the behavior of the device over time.

        See Also
        --------
        get_messages : For retrieving messages that may have been logged as part of the device's operation.
        """
        link = self._build_url('packets')
        return self._perform_get_request(link=link, params=params).json()

    def get_snapshots(self):
        """
        List of archived messages snapshots available for a device.

        Retrieves a list of available snapshots for the specified device, identified by a 'dev-selector'. Snapshots are generated approximately once per day for all device messages and are stored in the archive for a limited time. This method allows users to identify which snapshots are available for download.

        Parameters
        ----------
        None

        Returns
        -------
        snapshots : dict or None
            The dict object containing information about available snapshots, including their timestamps and identifiers, or None if an error occurred.

        Examples
        --------
        >>> snapshots = device.get_snapshots()
        >>> print(snapshots)
        {'snapshots': [{'timestamp': 1610000000, 'id': 'snapshot1'},
                    {'timestamp': 1610008600, 'id': 'snapshot2'},
                    ...]}

        Notes
        -----
        - The 'dev-selector' is used to specify the device for which to list snapshots, usually by ID, configuration.ident, name, and other criteria.
        - Snapshots are intended for diagnostic purposes only, such as restoring device messages in case of accidental changes or deletion. They should not be relied upon in production environments.
        - The availability of snapshots and their periodic generation are not guaranteed, as this is part of internal functionality provided outside of the standard Flespi platform services.
        - For regular device messages retrieval, always use the GET /gw/devices/{dev-selector}/messages API call instead of snapshots.

        See Also
        --------
        get_snapshot : For downloading a specific snapshot identified by its timestamp.
        get_messages : For retrieving messages from the device, which is the recommended method for regular message access.
        """
        link = self._build_url('snapshots')
        try:
            return self._perform_get_request(link).json()
        except requests.exceptions.HTTPError as http_err:
            # Specific HTTP error
            logging.error(f'HTTP error occurred: {http_err}')
        except requests.exceptions.ConnectionError as conn_err:
            # Network problem
            logging.error(f'Connection error occurred: {conn_err}')
        except requests.exceptions.Timeout as timeout_err:
            # Request timeout
            logging.error(f'Request timed out: {timeout_err}')
        except requests.exceptions.RequestException as req_err:
            # Catch-all for requests exceptions
            logging.error(f'Error during request to {link}: {req_err}')
        except Exception as e:
            # Non-requests exceptions
            logging.error(f'An unexpected error occurred: {e}')
        return None

    def get_snapshot(self, output):
        """
        Download the latest snapshot file available for device messages and saves it to a file.

        This method fetches the most recent snapshot archive for the specified device, identified by a 'dev-selector', and saves it to the specified output file. Snapshots are generated approximately once per day for all device messages and are stored in the archive for a limited time. The 'snapshot-selector' is used to specify the UNIX timestamp of the snapshot to be downloaded, which can be listed using the GET /gw/devices/{dev-selector}/snapshots API call.

        Parameters
        ----------
        output : str
            The file path where the downloaded snapshot will be saved.

        Returns
        -------
        None

        Examples
        --------
        >>> device.get_snapshot(output='device_snapshot.zip')
        Snapshot downloaded and saved to 'device_snapshot.zip'.

        Notes
        -----
        - The 'dev-selector' specifies the device for which to download the snapshot, usually by ID, configuration.ident, name, and other criteria.
        - Snapshots are intended for diagnostic purposes only, such as restoring device messages in case of accidental changes or deletion. They should not be relied upon in production environments.
        - The availability of snapshots and their periodic generation are not guaranteed, as this is part of internal functionality provided outside of the standard Flespi platform services.
        - For regular device messages retrieval, always use the GET /gw/devices/{dev-selector}/messages API call instead of snapshots.

        See Also
        --------
        get_messages : For retrieving messages from the device, which is the recommended method for regular message access.
        """
        snapshots_info = self.get_snapshots()
        if snapshots_info is None or 'result' not in snapshots_info or not snapshots_info['result']:
            logging.error(
                "No snapshots available or failed to retrieve snapshots.")
            return

        # Assuming the structure is {'result': [{'id': device_id, 'snapshots': [snapshot_ids]}]}
        # and you want the latest snapshot from the first device in the list
        latest_snapshot_id = max(snapshots_info['result'][0]['snapshots'])

        # Construct the link for the latest snapshot
        # link = f'https://flespi.io/gw/devices/{self.device_number}/snapshots/{latest_snapshot_id}'
        link = self._build_url(endpoint=f'snapshots/{latest_snapshot_id}')

        try:
            snapshot_data = self._perform_get_request(link)
            if snapshot_data.status_code == 200:
                with open(output, 'wb') as f:
                    for chunk in snapshot_data.iter_content(chunk_size=128):
                        f.write(chunk)
                logging.info(f"Snapshot data saved to {output}.")
        except Exception as e:
            logging.error(f"Failed to fetch or save snapshot data: {e}")

    # Remote control: settings
    def get_settings(self, all=True):
        """
        Get collection of settings matching filter parameters.

        Retrieves specified device settings, including their schemes and values, from the Flespi platform. The method allows for selecting settings from specific devices identified by a 'dev-selector', which can target devices by ID, configuration.ident, name, and other criteria. It also supports selecting which settings to return through a 'sett-selector', allowing for the retrieval of all settings or a subset specified by exact setting names.

        Parameters
        ----------
        all : bool, optional
            Indicates retrieval of all settings. If set to True (default), all available device settings are returned. If False, settings must be specified by exact names in a comma-separated format through the 'sett-selector'.

        Returns
        -------
        settings : dict or None
            A dictionary containing the requested device settings, their schemes, and current values. Each setting is represented as a key-value pair within the dictionary, where the key is the setting name and the value is its current value. Returns None if an error occurred during the request.

        Examples
        --------
        >>> device_settings = device.get_settings(all=True)
        >>> print(device_settings)
        {'settings': {'obd.mileage': {'value': 12345, 'scheme': {...}}, 'backend.server1': {'value': 'http://example.com', 'scheme': {...}}}}

        >>> specific_settings = device.get_settings(all=False)
        >>> print(specific_settings)
        {'settings': {'obd.mileage': {'value': 12345, 'scheme': {...}}}}

        Notes
        -----
        - The 'dev-selector' and 'sett-selector' functionalities are implied by the method's parameters and usage context. The actual implementation of these selectors depends on the method's internal logic and the API's capabilities.
        - Device settings are essentially cached shadows of device configuration options stored within Flespi. The 'current' property of each setting reflects its latest known value.
        - The structure and content of the returned settings dictionary may vary depending on the data available on the Flespi platform for the user's account and the specified selectors.

        See Also
        --------
        get_messages : For retrieving messages that may have been affected by the device settings.
        """
        if all:
            link = self._build_url(endpoint='settings/all')
            # link = f'https://flespi.io/gw/devices/{self.device_number}/settings/all'
            return self._perform_get_request(link).json()
        else:
            # If there's a future implementation planned for when `all` is False, handle it here.
            # For now, raise an error to indicate the method is not yet implemented for this case.
            raise NotImplementedError(
                "Retrieval of filtered settings is not implemented.")
