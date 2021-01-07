import unittest
import os

from flespi_gateway.gateway import Device

class TestDevice(unittest.TestCase):
    def setUp(self):
        FLESPI_TOKEN = os.environ.get('FLESPI_TOKEN', None)
        FLESPI_DEVICE_NUMBER = int(os.environ.get('DEVICE', None))
        self.dv = Device(device_number=FLESPI_DEVICE_NUMBER, flespi_token=FLESPI_TOKEN)

    def test_telemetry(self):
        telemetry = self.dv.get_telemetry()

        self.assertIsInstance(telemetry, dict)

if __name__ == '__main__':
    unittest.main()