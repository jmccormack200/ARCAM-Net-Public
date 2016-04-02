# Our Class Files
from Node import Node
from LocalNode import LocalNode
from threading import Lock

import time

class NodeDataTable():

    def __init__(self, node_dict={}, node_list=[], tblfreq=None, tblTime=None, time_out=30):
        self.node_dict = node_dict
        self.tblfreq = tblfreq
        self.tblTime = tblTime
        self.time_out = time_out
        

    def set_freq(self, freq,time):
        if self.tblfreq == None:
            self.tblfreq = freq
            self.tblTime = time
            return True
        else:
            if time == self.tblTime and freq == self.tblFreq:
                return True
            if time < self.tblTime:
                self.Flush
                self.tblfreq = freq
                self.tblTime = time
                print "Current table out of date, flushing"
                return True
            else:
                print "Throw error, sender tbl out of date"
                return False
                


    def ackNode(self, newNode):
        newNode.ack = True
        self.__updateDict(newNode)
       

    def rcvHeartbeat(self, newNode):
        if newNode.name not in self.node_dict:
            print ("Node (" + newNode.name + ") added to table")
            self.node_dict[newNode.name] = newNode
        else:
            self.node_dict[newNode.name].time = newNode.time

    def getDict(self):
        pass

    def printDict(self):
        for key in self.node_dict:
            print({'IP': self.node_dict[key].IP, 'ack': self.node_dict[key].ack, 'freq': self.node_dict[key].freq })
        print 

    def Flush(self):
        self.tblfreq = None
        for key in self.node_dict:
            self.node_dict[key].clear_ack()
        print "Flush"


    def checkIfTableIsFull(self):
        isfull = True 
        for key in self.node_dict:
            tempNode = self.node_dict[key]
            if self.node_dict[key].ack == None:
                if float(time.time()) - float(tempNode.time) >= float(self.time_out):
                    print ("Node (" + self.node_dict[key].name + ") dropped from table")
                    del self.node_dict[key]
                    continue
                else:
                    isfull = False
        return isfull



    def __updateDict(self, newNode):
        if self.tblfreq != newNode.freq:
            print "Frequency mismatch on " + newNode.IP
            #handle rogue node
        elif newNode.name not in self.node_dict:
            self.node_dict[newNode.name] = newNode
            print ("Node (" + newNode.name + ") added to table")
        else:
            self.node_dict[newNode.name] = newNode
             
