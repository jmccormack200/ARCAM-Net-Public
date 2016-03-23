# Our Class Files
from Node import Node
from LocalNode import LocalNode
from threading import Lock

import time

class NodeDataTable():

    def __init__(self, node_dict={}, node_list=[], freq=None, time_out=30):
        self.node_dict = node_dict
        self.node_list = node_list
        self.freq = freq
        self.time_out = time_out
        

    def set_freq(self, freq):
        if self.freq == None:
            self.freq = freq
        else:
            print "Throw error, frequency already set"


    def ackNode(self, newNode):
        newNode.ack = True
        self.__updateDict(newNode)
        #self.__updateNodeTable(newNode)




    def rcvHeartbeat(self, newNode):
        # This may be needed later. The difference being
        # this function will only insert if the node is new.
        if newNode.name not in self.node_dict:
            self.node_dict[newNode.name] = newNode
            print ("Node (" + newNode.name + ") added to table")
            #self.__updateNodeTable(newNode)
        else:
            self.node_dict[newNode.name].time = newNode.time

        
        

    def getTable(self):
        pass

    def getDict(self):
        pass

    def printDict(self):
        for key in self.node_dict:
            print(self.node_dict.__dict__)

    def Flush(self):
        for key in self.node_dict:
            self.node_dict[key].clear_ack()

    def checkIfTableIsFull(self):
        isfull = True 
        for key in self.node_dict:
            tempNode = self.node_dict[key]
            if tempNode.ack == None:
                isfull = False
                if float(time.time()) - float(tempNode.time) >= float(self.time_out):
                    del self.node_dict[key]
        return isfull



    def __updateDict(self, newNode):
        if self.freq != newNode.freq:
            print "Frequency mismatch on " + newNode.IP
            #handle rogue node
        elif newNode.name not in self.node_dict:
            self.node_dict[newNode.name] = newNode
            print ("Node (" + newNode.name + ") added to table")
        else:
            self.node_dict[newNode.name] = newNode
            

        '''
        if self.freq != node.freq:
            self.node_dict[Node.name] = node
        else:
            node_dict[Node.name] = "OK"
        '''

    '''    
    #does not work
    def __updateNodeTable(self, newNode):
        if newNode not in self.node_list:
            self.node_list.append(newNode)
            print ("Node (" + newNode.name + ") added to table")
        else:
            #print ("Node (" + newNode.name + ") already in table")
            pass
    '''        
