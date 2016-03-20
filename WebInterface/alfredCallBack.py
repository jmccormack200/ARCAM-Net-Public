

from socketIO_client import SocketIO, BaseNamespace
#import json
import sys
from time import sleep
#import os

class Namespace(BaseNamespace):
    def on_connect(self):
        print('Connected')

def send (lines):
	print(lines)
	
	data = []
	
	for line in lines:
		if line == "\n":
			pass
		else:
			print (line)

			frame = line.strip()[2:-3].split(', ')
			freqandtime = frame[1].split('\\')[0]
			freq,time = freqandtime[1:].split('%')
			mac = frame[0]

			if not data:
				data = [mac,freq,time]
			elif float(data[2]) <= float(time):
				print("HERE")
				data = [mac,freq,time]

	print ("Outputting: " + str(data[1]))
	sleep(4)
	socketIO = SocketIO('127.0.0.1', 5000)
	socketIO.emit('alfred set freq', str(data[1]))
	socketIO.wait(1)

#use this function for testing
def test():
	#Some dummy data if you need to do testing
	#line = '{ "c2:4c:e0:9f:80:07", "918000000%1456077160.77\x0a" },'
	lines = ['{ "6e:28:26:a3:71:dd", "915000000%1456083136.18\\x0a" },\n', '{ "f6:84:ae:73:38:0c", "922000000%1459083275.63\\x0a" },\n']
	send(lines)


if __name__ == '__main__':
	lines = []

	
	for line in sys.stdin:	
		lines.append(line)
	
	send(lines)
	
	#test()


	


