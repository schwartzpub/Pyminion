import socket
from threading import Thread
import SocketServer
import sys
import os
import signal
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('sh.schwartzpub.com', 4898)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
sock.settimeout(10)

def recv():
	dat = ''
	while True:
		try:
			data=sock.recv(1)
		except:
			sock.close()
			sys.exit(0)
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
		data = raw_input("")
		if not data: 
			continue
		elif data == '!quit':
			sock.sendall(data)
			break
		else:
			sock.sendall(data)
			sock.settimeout(None)
			continue

def signal_handler(signal, frame):
	try:
		sock.sendall('!quit')
		sock.close()
		sys.exit(0)
	except:
		pass

signal.signal(signal.SIGINT, signal_handler)

Thread(target=recv).start()
senddata()
sock.close()
