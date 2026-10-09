import unittest

from safe_config import ConfigurationError, parse_configuration


class SafeConfigurationTests(unittest.TestCase):
    def test_accepts_valid_configuration(self):
        config = parse_configuration("{'theme': 'dark', 'refresh_seconds': 45, 'notifications': False}")
        self.assertEqual(config.theme, "dark")
        self.assertEqual(config.refresh_seconds, 45)
        self.assertFalse(config.notifications)

    def test_uses_defaults_for_omitted_fields(self):
        config = parse_configuration("{'theme': 'system'}")
        self.assertEqual(config.refresh_seconds, 30)
        self.assertTrue(config.notifications)

    def test_rejects_executable_expression(self):
        with self.assertRaises(ConfigurationError):
            parse_configuration("__import__('os').system('echo unsafe')")

    def test_rejects_unknown_setting(self):
        with self.assertRaises(ConfigurationError):
            parse_configuration("{'theme': 'dark', 'admin': True}")

    def test_rejects_invalid_value_type(self):
        with self.assertRaises(ConfigurationError):
            parse_configuration("{'refresh_seconds': 'soon'}")


if __name__ == "__main__":
    unittest.main()
