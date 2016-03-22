# Our Class Files
from Node import Node
from LocalNode import LocalNode


class NodeDataTable():

    def __init__(self, node_dict={}, node_list=[], freq=0):
        self.node_dict = node_dict
        self.node_list = node_list
        self.freq = freq

    def update(self, Node, msgDat):
        self.__updateNodeTable(Node)
        self.__addACKtoStatusDict(Node)


    def append(self, Node):
        # This may be needed later. The difference being
        # this function will only insert if the node is new.
        pass

    def getTable(self):
        pass

    def getDict(self):
        pass

    def Flush(self):
        for key in slef.node_dict:
            node_dict[key].clear_ack()

    #def printTables():

    def checkIfTableIsFull():
        isfull = True 
        for key in node_dict:
            if node_dict[key].ack == None:
                return not isfull
        return isfull

    def __addACKtoStatusDict(self, Node):
        if self.freq != Node.freq:
            print("Interfering frequency change")
            # need to handle rogue changes in freq
            pass
        else:
            node_dict[NodeName] = "OK"

    def __updateNodeTable(self, newNode):
        if not newNode in node_list:
            node_list.append(newNode)
            print ("Node (" + newNode.name + ") added to table")
        else:
            print ("Node (" + newNode.name + ") already in table")
            