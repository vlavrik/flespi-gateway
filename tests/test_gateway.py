import unittest
import os

from flespi_gateway.gateway import Device
FLESPI_TOKEN = os.environ.get('FLESPI_TOKEN', None)
FLESPI_DEVICE_NUMBER = os.environ.get('DEVICE', None)

class TestDevice(unittest.TestCase):
    def setUp(self):
        self.dv = Device(device_number=FLESPI_DEVICE_NUMBER, flespi_token=FLESPI_TOKEN)
    
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

    def test_telemetry(self):
        telemetry = self.dv.get_telemetry()

        self.assertIsInstance(telemetry, dict)





if __name__ == '__main__':
    unittest.main()