import socket
from threading import Thread
import SocketServer
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.0.111', 4898)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

def recv():
	while True:
		data = sock.recv(1024)
		if not data:
			sys.exit(0)
		print data

def senddata():
	while True:
		data = raw_input("")
		if not data: 
			continue
		elif data == '!quit':
			sock.sendall(data)
			break
		else:
			sock.sendall(data)

Thread(target=recv).start()
senddata()
sock.close()
