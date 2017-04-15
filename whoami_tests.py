import unittest
import whoami


class MyTest(unittest.TestCase):
    def test_getip(self):
        ip = whoami.getip()
        print(ip)
        self.assertRegexpMatches(ip, r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    def test_getpubip(self):
        ip = whoami.getpubip()
        print(ip)
        self.assertRegexpMatches(ip, r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    def test_uptime(self):
        uptime = whoami.getuptime()
        print(uptime)
        self.assertGreater(uptime, 0)

    def test_hostname(self):
        hostname = whoami.gethostname()
        print(hostname)
        self.assertIsNotNone(hostname)


if __name__ == '__main__':
    unittest.main()
