#!/usr/bin/env python
"""
This module will get various bit of info about the running system
and populate a row in a google doc with it.
"""
from __future__ import print_function
import time
import socket
import http.client as httplib
import platform
import urllib.request as urllib2
from urllib.error import URLError
import logging

import uptime
import sheets


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info('Starting')
# this is the url i am using to get the public IP
IP_WEBSITE = "myip.xname.org:80"

# Find this value in the spreadsheet url with 'key=XXX' and copy XXX below
SPREADSHEET_KEY = '1Ewy2qo98asjDiZoSJtwkZX5oQQPuR5ka91BNkfGaWSA'


def getip():
    """  Gets the local IP """

    return [l for l in
            (
                [ip for ip in socket.gethostbyname_ex(socket.gethostname())[
                    2] if not ip.startswith("127.")][:1],
                [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close())
                  for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]
            ) if l][0][0]


def getpubip():
    """ Gets the public IP by doing a get of the IP_WEBSITE """
    conn = httplib.HTTPConnection(IP_WEBSITE)
    conn.request("GET", "/")
    response = conn.getresponse()
    ip_address = response.read().decode('utf-8')
    ip_address = ip_address.replace("\n", "")
    return ip_address


def getuptime():
    """ gets uptime """
    output = uptime.uptime()
    return output


def gethostname():
    """ gets current hostname """
    if socket.gethostname().find('.') >= 0:
        return socket.gethostname()
    return socket.gethostbyaddr(socket.gethostname())[0]


def write_to_sheet(results):

    try:
        entry = sheets.append_row(SPREADSHEET_KEY, results)
    except Exception as err:
        logging.error("Insert row failed. {0}".format(results))
        raise err

    if entry and entry['updates']['updatedRows'] > 0:
        logging.info("Insert row succeeded.")
    else:
        return 0


def wait_for_internet_connection():
    start = time.time()
    while True and time.time() - start < 10:
        try:
            response = urllib2.urlopen('http://216.58.213.110', timeout=1)
            return True
        except URLError:
            pass
    return False


def main():
    """ Get various bits of system info and publish to google sheet """
    platform_info = platform.platform()
    hostname = gethostname()
    publip = getpubip()
    loclip = getip()
    uptim = getuptime()

    results = [platform_info, hostname, time.strftime('%H:%M:%S'), time.strftime(
        '%d/%m/%Y'), loclip, publip, str(uptim)]
    return write_to_sheet(results)


if __name__ == '__main__':
    try:
        if wait_for_internet_connection():
            main()
        else:
            logging.error("No internet connection")
    except Exception as err:
        logging.error("Insert row failed. {0}".format(err))
