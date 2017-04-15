"""This module tests the whoami module"""
from __future__ import print_function
import unittest
import whoami


class WhoAmITests(unittest.TestCase):
    """ Tests for whoami """

    ip_address_regex = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"

    def test_getip(self):
        """Test getip method returns valid IP address"""
        ip_address = whoami.getip()
        print(ip_address)
        self.assertRegexpMatches(ip_address, self.ip_address_regex)

    def test_getpubip(self):
        """Test getpubip method returns valid IP address"""
        ip_address = whoami.getpubip()
        print(ip_address)
        self.assertRegexpMatches(ip_address, self.ip_address_regex)

    def test_uptime(self):
        """Test uptime method returns number greater than 0"""
        uptime = whoami.getuptime()
        print(uptime)
        self.assertGreater(uptime, 0)

    def test_hostname(self):
        """Test hostname is not None"""
        hostname = whoami.gethostname()
        print(hostname)
        self.assertIsNotNone(hostname)


if __name__ == '__main__':
    unittest.main()
