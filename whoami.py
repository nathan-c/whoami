#!/usr/bin/env python
"""
This module will get various bit of info about the running system
and populate a row in a google doc with it.
"""
from __future__ import print_function
import time
import socket
import httplib
import platform
import uptime
import sheets

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
    message = response.status, response.reason
    message = str(message)
    # print message #print http responce for debugging
    ip_address = response.read()
    # get rid of new line character (may not be necessary)
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


def main():
    """ Get various bits of system info and publish to google sheet """
    platform_info = platform.platform()
    hostname = gethostname()
    publip = getpubip()
    loclip = getip()
    uptim = getuptime()

    results = [platform_info, hostname, time.strftime('%H:%M:%S'), time.strftime(
        '%d/%m/%Y'), loclip, publip, str(uptim)]

    entry = sheets.append_row(SPREADSHEET_KEY, results)
    if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
        print("Insert row succeeded.")
    else:
        return 0


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print("Insert row failed. {0}".format(err))
