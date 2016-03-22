

"""Decentralized chat example"""


class Node():
    def __init__(self,IP,tun0,bat0,freq,datetime):
        self.IP = IP
        self.tun0 = tun0
        self.bat0 = bat0
        self.name = str(self.IP) + "/" + str(self.tun0) + "/" + str(self.bat0)
        self.ack = None
        self.freq = freq
        self.datetime = datetime


    def set_freq(self,freq):
        self.freq = freq

    def set_ack(self, ack=True):
        self.ack = ack

    def clear_ack(self):
        self.ack = None
