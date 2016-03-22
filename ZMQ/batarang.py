

"""Decentralized chat example"""

import argparse
import os
from threading import Thread

from Queue import Queue

from netifaces import interfaces, ifaddresses, AF_INET, AF_LINK # dependency, not in stdlib

from datetime import datetime

# Our Class Files
from Node import Node
from LocalNode import LocalNode
from NodeDataTable import NodeDataTable

import zmq


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
    #IP/tun0/bat0: freqChange rx/tx time
    #IP/tun0/bat0: OK rx/tx time
    #IP/tun0/bat0: heartbeat rx/tx time
    
    #parse
    msgParts = msg.split(' ')
    sourceDat = msgParts[0].split('/')
    msgType = msgParts[1]
    msgDat = msgParts[2]
    datetime = msgParts[3]


    IP = sourceDat[0]
    tun0 = sourceDat[1]
    bat0 = sourceDat[2]

    newNode = Node(IP,tun0,bat0, msgDat, datetime)
    

    if msgType == 'freqChange':
        # will need to set the freq of the
        # NodeDataTable() here. 
        print "Ip = " + str(IP)
        print "tun0 = " + str(tun0)
        print "bat0 = " + str(bat0)
        print "msgDat = " + str(msgDat)
        print "time = " + str (datetime)
        nodeDT.set_freq(msgDat)
        print "Frequency of Table is now: " + nodeDT.freq
        freqQue.join()
        freqQue.put({"IP": IP,"msgDat": msgDat})

    elif msgType == 'ACK':
        nodeDT.update(newNode, msgDat)
        print nodeDT.node_dict
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
            message = message = localnode.name + " ACK " + "915000 " + str(datetime.utcnow())
            bcast.send_string(message)

            # send OK 
            # Wait for full table
            # Here we would send this data out over SocketIO
            # Connect to socket
            # Send to change,
            # Flush the table
            

def main():
    global freqQue
    freqQue = Queue()

    global nodeDT
    nodeDT = NodeDataTable()

    global bcast
    global localnode

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
            message = localnode.name + " freqChange 915000 " + str(datetime.utcnow())
            bcast.send_string(message)
        except KeyboardInterrupt:
            break
            
    bcast.close(linger=0)
    ctx.term()
    listen_thread.stop()
    freqQue_thread.stop()

if __name__ == '__main__':
    main()

