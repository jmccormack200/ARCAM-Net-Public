

"""Decentralized chat example"""

import argparse
import os
from threading import Thread, Lock

from Queue import Queue

from netifaces import interfaces, ifaddresses, AF_INET, AF_LINK # dependency, not in stdlib

import time

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
            #print(listenerOut)
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
    time = msgParts[3]


    IP = sourceDat[0]
    tun0 = sourceDat[1]
    bat0 = sourceDat[2]

    
    newNode = Node(IP,tun0,bat0, msgDat, time)

    lock.acquire()
    try:
        if msgType == 'freqChange':
            '''
            print "Ip = " + str(IP)
            print "tun0 = " + str(tun0)
            print "bat0 = " + str(bat0)
            print "msgDat = " + str(msgDat)
            print "time = " + str (time)
            '''
            print(msg)
            nodeDT.set_freq(msgDat)

            
            freqQue.put({"IP": IP,"msgDat": msgDat})

        elif msgType == 'ACK':
            print
            print(msg)
            print

            nodeDT.ackNode(newNode)
            nodeDT.printDict()

        elif msgType == 'heartbeat':
            nodeDT.rcvHeartbeat(newNode)
            print(IP + ":" time ":" + str(time.time()))
        else:
            print ("Invalid Message Type")
    finally:
        lock.release()

def freqChangeHandler():
    while True:
        if not freqQue.empty():
            data = freqQue.get()
            IP = data['IP']
            msgDat = data['msgDat']
            print "Got request on Q IP = " + IP + "msg = " + msgDat
            message = localnode.name + " ACK " + msgDat + " " + str(time.time())
            bcast.send_string(message)

            
            isfull = False
            while not isfull:
                lock.acquire()
                try:
                    isfull = nodeDT.checkIfTableIsFull()
                finally:
                    lock.release()
            
            # Here we would send this data out over SocketIO
            # Connect to socket
            # Send to change,
            print("Change success. Flushing table")
            # Flush the table
            lock.acquire()
            try:
                nodeDT.Flush()
            finally:       
                lock.release()
           
            #nodeDT.printDict()

            freqQue.task_done()


    

def pacemaker():
    while True:
        lock.acquire()
        try:
            msg =localnode.name + " heartbeat " + localnode.freq + " " + str(time.time())
            bcast.send_string(msg)
        finally:
            lock.release()
            time.sleep(1)



def main():
    global freqQue
    freqQue = Queue()

    global nodeDT
    nodeDT = NodeDataTable()

    global bcast
    global localnode
    localnode = LocalNode()

    global lock
    lock = Lock()

    parser = argparse.ArgumentParser()
    parser.add_argument("interface", type=str, help="the network interface",
        choices=interfaces(),
    )

    args = parser.parse_args()
    inet = ifaddresses(args.interface)[AF_INET]
    addr = inet[0]['addr']
    masked = addr.rsplit('.', 1)[0]
    
    ctx = zmq.Context.instance()
    bcast = ctx.socket(zmq.PUB)
    bcast.bind("tcp://%s:9000" % args.interface)


    listen_thread = Thread(target=listen, args=(masked,))
    listen_thread.daemon = True
    listen_thread.start()

    pacemaker_thread = Thread(target=pacemaker, args=())
    pacemaker_thread.daemon = True
    pacemaker_thread.start()

    freqQue_thread = Thread(target=freqChangeHandler, args=())
    freqQue_thread.daemon = True
    freqQue_thread.start()
    


    print("starting chat on %s:9000 (%s.*)" % (args.interface, masked))

    

    while True:
        try:
            msg = raw_input()

            message = localnode.name + " freqChange 915000 " + str(time.time())
            lock.acquire()
            try:
                bcast.send_string(message)
            finally:
                lock.release()
        except KeyboardInterrupt:
            break

    bcast.close(linger=0)
    ctx.term()

if __name__ == '__main__':
    main()

