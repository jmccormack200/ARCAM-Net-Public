# Our Class Files
from Node import Node
from LocalNode import LocalNode


class NodeDataTable():

    def __init__(self, node_dict={}, node_list=[], freq=None):
        self.node_dict = node_dict
        self.node_list = node_list
        self.freq = freq

    def set_freq(self, freq):
        if self.freq == None:
            self.freq = freq
        else:
            print "Throw error, frequency already set"

    def update(self, Node, msgDat):
        Node.set_ack(True)
        Node.set_freq(msgDat)
        self.__updateNodeTable(Node)
        self.__updateDict(Node)


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

    def __updateDict(self, node):
        if self.freq == node.freq:
            self.node_dict[node.name] = node
        else:
            print "Frequency Mismatch"
        '''
        if self.freq != Node.freq:
            self.node_dict[Node.name] = Node
        else:
            node_dict[Node.name] = "OK"
        '''

    def __updateNodeTable(self, newNode):
        if not newNode in self.node_list:
            self.node_list.append(newNode)
            print ("Node (" + newNode.name + ") added to table")
        else:
            print ("Node (" + newNode.name + ") already in table")
            