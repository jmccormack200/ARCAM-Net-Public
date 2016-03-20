import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 1234
MESSAGE = "Hello SDR World! I'm like hey whats up hello! I just called to say Hello. Hello Hello Hola"

print "UDP target IP: ", UDP_IP
print "UDP target Port: ", UDP_PORT
print "message: ", MESSAGE

#for a in range(0, 10000):
while(1):
	MESSAGE_SENT = MESSAGE
	print "Sent"
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(MESSAGE_SENT, (UDP_IP, UDP_PORT))
