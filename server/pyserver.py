#!/usr/bin/env python
 
import socket, struct, threading, cgi
 
def recv_data (client, length):
	data = client.recv(length)
	if not data: return data
	return data
 
def send_data (client, data):
	message = str(data)
	return client.send(message)
 
def handle (client, addr, name):
	lock = threading.Lock()
	while 1:
		data = recv_data(client, 1024)
		if not data: break
		if data == '!quit': break
		lock.acquire()
		[send_data(c, "<" + name + "> " + data) for c in (u for u in clients if u != client)]
		lock.release()
	print 'Client closed:', addr
	[send_data(c, "** QUIT: " + name + " has left the server!") for c in (u for u in clients if u != client)]
	lock.acquire()
	clients.remove(client)
	del client_list[name]
	lock.release()
	client.close()

def join_players(conn, game):
	p = conn
	
	
def start_server ():
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('192.168.0.111', 4898))
	s.listen(5)
	while 1:
		conn, addr = s.accept()
		print 'Connection from:', addr
		send_data(conn, "Welcome to the Pyminion server, please select a username:")
		while True:
			client_name = str(recv_data(conn, 1024))
			if client_name.lower() in client_list:
				send_data(conn, "Sorry, that name is in use, please choose another name.")
			else:
				break
		send_data(conn, "Welcome to Dominion, " + client_name + "! Currently connected clients are: ")
		for key in client_list.keys(): send_data(conn, key)
		for client in clients: send_data(client, "** JOIN: " + client_name + " has joined the server!")
		clients.append(conn)
		client_list[client_name.lower()] = conn
		threading.Thread(target = handle, args = (conn, addr, client_name)).start()
#		if recv_data(conn, 1024) == '!start':
#			send_data(conn, "Starting new game... please choose a room name:")
#			while True:
#				room_name = recv_data(conn, 1024)
#				if room_name.lower() in room_list:
#					send_data(conn, "Sorry, that room name is in use, please choose another name.")
#				else:
#					break
#			room_list[room_name] = []
#			send_data(conn, "New room: " + room_name + " started!") 
#		else:
#			for client in clients:
#				send_data(client, recv_data(conn, 1024))			 
clients = []
client_list = {}
room_list = {}
start_server()
