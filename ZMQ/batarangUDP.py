

"""Decentralized chat example"""
# http://randalh.blogspot.ie/2012/12/zeromq-true-peer-connectivity-harmony.html

import argparse
import os
from threading import Thread, Lock

from Queue import Queue

from netifaces import interfaces, ifaddresses, AF_INET, AF_LINK # dependency, not in stdlib

import time

import socket
import select

# Our Class Files
from Node import Node
from LocalNode import LocalNode
from NodeDataTable import NodeDataTable

import zmq


def handleMsg(msg):
    #format    
    #IP/tun0/bat0: freqChange rx/tx time
    #IP/tun0/bat0: OK rx/tx time
    #IP/tun0/bat0: heartbeat rx/tx time
    #parse

    msgParts = msg.split(' ')
    IP = msgParts[0]
    msgType = msgParts[1]
    msgDat = msgParts[2]
    nodetime = msgParts[3]


    #IP = sourceDat[0]
    #tun0 = sourceDat[1]
    #bat0 = sourceDat[2]

    
    newNode = Node(IP, msgDat, nodetime)

    lock.acquire()

    try:
        if msgType == 'freqChange':
            
            #print "Ip = " + str(IP)
            #print "tun0 = " + str(tun0)
            #print "bat0 = " + str(bat0)
            #print "msgDat = " + str(msgDat)
            #print "time = " + str (time)
            
            
            nodeDT.set_freq(msgDat)

            
            freqQue.put({"IP": IP,"msgDat": msgDat})

        elif msgType == 'ACK':

            nodeDT.ackNode(newNode)
            nodeDT.printDict()

        elif msgType == 'heartbeat':
            nodeDT.rcvHeartbeat(newNode)
            #print(IP[-3:] + " : " + str(round((float(time.time()) - float(nodetime)),3)))
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
            print "Got request on Q IP = " + IP + " msg = " + msgDat
            message = localnode.name + " ACK " + msgDat + " " + str(time.time())
            
            lock.acquire()
            try:
                broadcastUDP(message,9000)
            finally:
                lock.release()
            
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

def broadcastUDP(msg, port=9000):
    UDP_IP = '<broadcast>'
    UDP_PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print "get lock?"
    #lock.acquire()
    print "yes"
    for a in range(0,10):
        try:
            sock.sendto(msg, (UDP_IP, UDP_PORT))
        finally:
    #        lock.release()
            time.sleep(1)


    

def pacemaker(addr):
    UDP_IP = '<broadcast>'
    UDP_PORT = 9001

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
     
    while True:
        msg =localnode.name + " heartbeat " + localnode.freq + " " + str(time.time())
        #data = repr(str(addr[-3:]) + '\n')
        lock.acquire()
        try:
            sock.sendto(msg, (UDP_IP, UDP_PORT))
        finally:
            lock.release()
            time.sleep(1)

def udprec(addr, port=9000):
    UDP_PORT = port
    bufferSize = 1024

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', UDP_PORT))

    while True:
        print "Check"
        msg, addr = sock.recvfrom(bufferSize)
        print msg
        handleMsg(msg)


def main():
    global freqQue
    freqQue = Queue()

    global nodeDT
    nodeDT = NodeDataTable()

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
    addr = str(inet[0]['addr'])
    masked = addr.rsplit('.', 1)[0]

    ''' 
    move this to udp
    '''

    pacemaker_thread = Thread(target=pacemaker, args=(addr,))
    pacemaker_thread.daemon = True
    pacemaker_thread.start()

    freqQue_thread = Thread(target=freqChangeHandler, args=())
    freqQue_thread.daemon = True
    freqQue_thread.start()
    
    udp_thread = Thread(target=udprec, args=(addr,9000,))
    udp_thread.daemon = True
    udp_thread.start()

    udp_thread_hb = Thread(target=udprec, args=(addr,9001,))
    udp_thread_hb.daemon = True
    udp_thread_hb.start()



    print("starting chat on %s:9000 (%s.*)" % (args.interface, masked))

    

    while True:
        try:
            msg = raw_input()

            message = localnode.name + " freqChange 915000 " + str(time.time())
            lock.acquire()
            try:
                broadcastUDP(message)
            finally:
                lock.release()
        except KeyboardInterrupt:
            break

    ctx.term()

if __name__ == '__main__':
    main()

