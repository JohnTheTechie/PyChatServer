from unittest import TestCase
from src.configuration_managers import ConfigManager


class TestConfigManager(TestCase):
    def test_get_parameter(self):
        manager = ConfigManager()
        self.assertEqual("x:y".split(":"), ['x', 'y'])
        self.assertEqual(manager.get_parameter("maximum_connections"), 5)
        self.assertEqual(manager.get_parameter("socket_address % host_address"), "localhost")
        self.assertEqual(manager.get_parameter("socket_address%port"), 42424)
