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
	name = name.lower()
	while 1:
		data = recv_data(client, 1024)
		if not data: break
		if data == '!quit': break
		if data == '!start': start_game(client, addr, name)
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

def start_game(client, addr, name):
	game = {}
	user = name
	send_data(client, '** STARTING GAME:  Please enter the names of the users you want to start a game with, one per line. Enter !go when you are ready to begin.')
	game[name] = client
	while 1:
		player = recv_data(client, 1024)
		player = player.lower()
		if player not in client_list:
			if player == '!go' and len(game.keys()) >= 2:
				[send_data(c, "** GAME STARTING: The following players are entering a new game: ",) for c in clients]
				for p in game:
					del client_list[p]
			elif player == '!go' and len(game.keys()) < 2:
				send_data(client, "You don't have enough players in your game, please add more before starting your game.")
			elif player == '!go' and len(game.keys()) > 4:
				send_data(client, "You have the maximum number of players in your game, please type !go to start your game.")
			elif player == '!cancel':
				send_data(client, "** GAME CREATION CANCELLED **")
				break
			else:
				send_data(client, "Sorry, that player doesn't appear to be connected to the server.  Please try again!") 
		elif player == user:
				send_data(client, "You do not need to add yourself to the game, please add other players!")
		else:
			game[player] = client_list[player]
			[send_data(client_list[player], "** GAME: you have been added to a new game with " + name + "!")]
		
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
		for key in client_list.keys(): send_data(conn, key + " ",)
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
