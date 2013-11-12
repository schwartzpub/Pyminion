import socket
from threading import Thread
import SocketServer
import sys
import os
import signal
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.0.111', 4898)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

def recv():
	dat = ''
	while True:
        	data=sock.recv(1)
       		if data == "\n":
			if dat == 'CLRSCRN_FULL':
				os.system('clear')
				dat = ''
				continue
			else:
				print dat
				dat = ''
		else: dat += data
				

#def recv():
#	while True:
#		data = sock.recv(8192)
#		if data == 'CLRSCRN_FULL':
#			os.system('clear')
#			continue
#		if not data:
#			sys.exit(0)
#		print data

def senddata():
	while True:
		print '>>'
		data = raw_input("")
		if not data: 
			continue
		elif data == '!quit':
			sock.sendall(data)
			break
		else:
			sock.sendall(data)
			continue

def signal_handler(signal, frame):
	sock.sendall('!quit')
	sock.close()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

Thread(target=recv).start()
senddata()
sock.close()
