from netifaces import interfaces, ifaddresses, AF_INET, AF_LINK # dependency, not in stdlib

# Our Class Files
from Node import Node



class LocalNode(Node):

    def __init__(self):
        self.parseIP()
        self.parseTun0()
        self.parseBat0()
        self.name = str(self.IP) + "/" + str(self.tun0) + "/" + str(self.bat0)
        # add frequency?

        # Possibly have a method to check current freq and see if the new freq command
        # is the same frequency.  

    def parseIP(self):
        addr = ifaddresses('bat0')
        self.IP = addr[AF_INET][0]['addr']

    def parseTun0(self):
        addr = ifaddresses('tun0')
        self.tun0 = addr[AF_LINK][0]['addr']

    def parseBat0(self):
        addr = ifaddresses('bat0')
        self.bat0 = addr[AF_LINK][0]['addr']