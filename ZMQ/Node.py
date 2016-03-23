

"""Decentralized chat example"""


class Node():
    def __init__(self,IP,freq,time):
        self.IP = str(IP)
        #self.tun0 = tun0
        #self.bat0 = bat0
        #self.name = str(self.IP) + "/" + str(self.tun0) + "/" + str(self.bat0)
        self.name = self.IP
        self.ack = None
        self.freq = str(freq)
        self.time = time


    def set_freq(self,freq):
        self.freq = int(freq)

    def set_ack(self, ack=True):
        self.ack = ack

    def clear_ack(self):
        self.ack = None
