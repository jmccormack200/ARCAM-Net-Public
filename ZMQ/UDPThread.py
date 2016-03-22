
import os
import sys
import time

import zmq
from udplib import UDP

#From http://zguide.zeromq.org/py:udpping2

#include <czmq.h>
PING_PORT_NUMBER = 9999
PING_MSG_SIZE    = 1
PING_INTERVAL    = 1  # Once per second

def UDPThread():

    udp = UDP(PING_PORT_NUMBER)

    poller = zmq.Poller()
    poller.register(udp.handle, zmq.POLLIN)

    # Send first ping right away
    ping_at = time.time()

    while True:
        timeout = ping_at - time.time()
        if timeout < 0:
            timeout = 0
        try:
            events = dict(poller.poll(1000* timeout))
        except KeyboardInterrupt:
            print("interrupted")
            break

        # Someone answered our ping
        if udp.handle.fileno() in events:
            udp.recv(PING_MSG_SIZE)

        if time.time() >= ping_at:
            # Broadcast our beacon
            print ("Pinging peers…")
            udp.send('!')
            ping_at = time.time() + PING_INTERVAL

if __name__ == '__main__':
    UDPThread()