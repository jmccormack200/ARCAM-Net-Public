

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


class Batarang():

    def __init__(self):
        self.freqQue = Queue()

        self.nodeDT = NodeDataTable()

        self.localnode = LocalNode()

        self.lock = Lock()

        parser = argparse.ArgumentParser()
        parser.add_argument("interface", type=str, help="the network interface",
            choices=interfaces(),
        )

        self.args = parser.parse_args()
        inet = ifaddresses(self.args.interface)[AF_INET]
        addr = str(inet[0]['addr'])
        self.masked = addr.rsplit('.', 1)[0]


        pacemaker_thread = Thread(target=self.pacemaker, args=(addr,))
        pacemaker_thread.daemon = True
        pacemaker_thread.start()

        self.freqQue_thread = Thread(target=self.freqChangeHandler, args=())
        self.freqQue_thread.daemon = True
        self.freqQue_thread.start()
        
        udp_thread = Thread(target=self.udprec, args=(addr,9000,))
        udp_thread.daemon = True
        udp_thread.start()

        udp_thread_hb = Thread(target=self.udprec, args=(addr,9001,))
        udp_thread_hb.daemon = True
        udp_thread_hb.start()

    def handleMsg(self, msg):
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

        self.lock.acquire()

        try:
            if msgType == 'freqChange':
                
                #print "Ip = " + str(IP)
                #print "tun0 = " + str(tun0)
                #print "bat0 = " + str(bat0)
                #print "msgDat = " + str(msgDat)
                #print "time = " + str (time)
                
                
                if(self.nodeDT.set_freq(msgDat,time)):
                    self.freqQue.put({"IP": IP,"msgDat": msgDat, "time" : time})
                self.nodeDT.ackNode(newNode)

            elif msgType == 'ACK':
                self.nodeDT.ackNode(newNode)
                self.nodeDT.printDict()

            elif msgType == 'heartbeat':
                self.nodeDT.rcvHeartbeat(newNode)
                #print(IP[-3:] + " : " + str(round((float(time.time()) - float(nodetime)),3)))
            else:
                print ("Invalid Message Type")
        finally:
            self.lock.release()

    def freqChangeHandler(self):
        while True:
            if not self.freqQue.empty():
                data = self.freqQue.get()
                IP = data['IP']
                msgDat = data['msgDat']
                time = data['time']
                print "Got request on Q IP = " + IP + " msg = " + msgDat
                message = self.localnode.name + " freqChange " + msgDat + " " + str(time)


                isfull = False
                while not isfull:
                    self.lock.acquire()
                    try:
                        self.broadcastUDP(message,9000)
                        #self.distributeMsg(message,9000)
                        isfull = self.nodeDT.checkIfTableIsFull()
                        self.nodeDT.printDict()
                    finally:
                        self.lock.release()
                
                # Here we would send this data out over SocketIO
                # Connect to socket
                # Send to change,
                print("Change success. Flushing table")
                # Flush the table
                self.lock.acquire()
                try:
                    self.nodeDT.Flush()
                finally:       
                    self.lock.release()

                self.freqQue.task_done()

    def distributeMsg(self, msg,port):
        for k,node in nodeDT.node_dict:
            if node.ACK == False:
                sendUdpMsg(msg,node.IP,port)


    def sendUdpMsg(self, msg, IP,port=9000):
        UDP_IP = str(IP)
        UDP_PORT = port

        host= str(IP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host,0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #lock.acquire()
        try:
            sock.sendto(msg, (host, UDP_PORT))
        finally:
            pass
        #        lock.release()  

    def broadcastUDP(self, msg, port=9000, numPackets=1):
        UDP_PORT = port

        host='192.168.200.255'
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host,0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #lock.acquire()
        for a in range(0,numPackets):
            try:
                sock.sendto(msg, (host, UDP_PORT))
            finally:
                pass
        #        lock.release()  

    def pacemaker(self, addr):
        UDP_PORT = 9001

        host='192.168.200.255'
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host,0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
         
        while True:
            msg =self.localnode.name + " heartbeat " + self.localnode.freq + " " + str(time.time())
            #data = repr(str(addr[-3:]) + '\n')
         #   lock.acquire()
            try:
                sock.sendto(msg, (host, UDP_PORT))
            finally:
          #      lock.release()
                time.sleep(1)

    def udprec(self, addr, port=9000):
        UDP_PORT = port
        bufferSize = 1024

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('', UDP_PORT))

        while True:
            msg, addr = sock.recvfrom(bufferSize)
            print addr
            self.handleMsg(msg)

    def start(self):

        print("starting chat on %s:9000 (%s.*)" % (self.args.interface, self.masked))

        

        while True:
            try:
                msg = raw_input()

                message = self.localnode.name + " freqChange 915000 " + str(time.time())
                self.lock.acquire()
                try:
                    self.broadcastUDP(message)
                finally:
                    self.lock.release()
            except KeyboardInterrupt:
                break

if __name__ == '__main__':
    batarang = Batarang()
    batarang.start()

