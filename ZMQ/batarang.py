

"""Decentralized chat example"""

import argparse
import os
from threading import Thread

from Queue import Queue

from netifaces import interfaces, ifaddresses, AF_INET, AF_LINK # dependency, not in stdlib

from datetime import datetime

import zmq

class Node():
    def __init__(self,IP,tun0,bat0,freq,time):
        self.IP = IP
        self.tun0 = tun0
        self.bat0 = bat0
        self.name = str(self.IP) + "/" + str(self.tun0) + "/" + str(self.bat0)
        self.ack = None
        self.freq = freq
        self.time = time


    def set_freq(self,freq):
        self.freq = freq

    def set_ack(self, ack=True):
        self.ack = ack

    def clear_ack(self):
        self.ack = None



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
            



def listen(masked):
    """listen for messages
    
    masked is the first three parts of an IP address:
    
        192.168.1
    
    The socket will connect to all of X.Y.Z.{1-254}.
    """
    ctx = zmq.Context.instance()
    listener = ctx.socket(zmq.SUB)
    for last in range(99, 110):
        listener.connect("tcp://{0}.{1}:9000".format(masked, last))
    
    listener.setsockopt(zmq.SUBSCRIBE, b'')
    while True:
        try:
            listenerOut = listener.recv_string()
            print(listenerOut)
            handleMsg(listenerOut)
        except (KeyboardInterrupt, zmq.ContextTerminated):
            break


def handleMsg(msg):
    #format    
    #IP/tun0/bat0: freqChange rx/tx
    #IP/tun0/bat0: OK rx/tx
    #IP/tun0/bat0: heartbeat rx/tx time
    
    #parse
    msgParts = msg.split(' ')
    sourceDat = msgParts[0].split('/')
    msgType = msgParts[1]
    msgDat = msgParts[2]
    time = msgParts[3]

    IP = sourceDat[0]
    tun0 = sourceDat[1]
    bat0 = sourceDat[2]

    newNode = Node(IP,tun0,bat0, msgDat, time)
    

    if msgType == 'freqChange':
        # will need to set the freq of the
        # NodeDataTable() here. 
        print "Ip = " + str(IP)
        print "tun0 = " + str(tun0)
        print "bat0 = " + str(bat0)
        print "msgDat = " + str(msgDat)
        print "time = " + str (time)
        freqQue.join()
        freqQue.put({"IP": IP,"msgDat": msgDat})
    elif msgType == 'OK':
        #UpdateNodeTable(newNode) <-
        pass
    elif msgType == 'heartbeat':
        #whatever  heartbeats do
        pass
    else:
        print ("Invalid Message Type")

def freqChangeHandler():
    while True:
        if not freqQue.empty():
            data = freqQue.get()
            freqQue.task_done()
            IP = data['IP']
            msgDat = data['msgDat']
            print "Got Data on Q IP = " + IP + "msg = " + msgDat
            # send OK 
            # Wait for full table
            # Here we would send this data out over SocketIO
            # Connect to socket
            # Send to change,
            # Flush the table
            

def main():
    global freqQue
    freqQue = Queue()

    global nodeStatus
    nodeDict = dict([('frequency change', 'none')])

    global nodeList
    nodeList = []

    parser = argparse.ArgumentParser()
    parser.add_argument("interface", type=str, help="the network interface",
        choices=interfaces(),
    )

    args = parser.parse_args()
    inet = ifaddresses(args.interface)[AF_INET]
    addr = inet[0]['addr']
    masked = addr.rsplit('.', 1)[0]
    
    ctx = zmq.Context.instance()
    
    listen_thread = Thread(target=listen, args=(masked,))
    listen_thread.daemon = True
    listen_thread.start()

    freqQue_thread = Thread(target=freqChangeHandler, args=())
    freqQue_thread.daemon = True
    freqQue_thread.start()
    
    bcast = ctx.socket(zmq.PUB)
    bcast.bind("tcp://%s:9000" % args.interface)
    print("starting chat on %s:9000 (%s.*)" % (args.interface, masked))
    localnode = LocalNode()
    while True:
        try:
            msg = raw_input()
            #IP/tun0/bat0: freqChange rx/tx
            message = localnode.name + " freqChange 915000" + str(datetime.utcnow())
            bcast.send_string(message)
        except KeyboardInterrupt:
            break
    bcast.close(linger=0)
    ctx.term()
    listen_thread.stop()
    freqQue_thread.stop()

if __name__ == '__main__':
    main()

