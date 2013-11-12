#!/usr/bin/env python

#This is the Server component.  I will be slowly injecting the game component into this portion to run the game.
 
import socket, struct, threading, cgi, random
from dominiondeck import *
from dominioncards import *
from dominionplayer import *

#Client class for users in the lobby waiting for a game to start.  A bit tricky, need to make some adjustments.
class Lobby_Client(threading.Thread):
	def __init__(self, conn, addr, name, clients):
		threading.Thread.__init__(self)
		self.client = conn
		self.addr = addr
		self.name = name.lower()
		self.clients = clients
		self.game = False
		self.event = threading.Event()

	def ingame(self):
		self.game = True

	def resume(self):
		self.game = False

	def run(self):
		lock = threading.Lock()
	        while 1:
			while self.game:
				self.clients.remove(self.client)
				continue
	                data = recv_data(self.client, 1024)
	                if not data: break
	                if data == '!quit': break
	                if data == '!start':
	                        while 1:
	                                build_game(self.client, self.addr, self.name)
	                                break
	                if data == '!help' : help_commands(self.client)
	                if data == '!list' : list_users(self.client)
	                if data == '!clear' : send_data(self.client, 'CLRSCRN_FULL\n')
	                lock.acquire()
	                [send_data(c, "<" + self.name + "> " + data + "\n") for c in (u for u in self.clients if u != self.client)]
	                lock.release()
        	print 'Client closed:', self.addr
	        [send_data(c, "\033[1;31m** QUIT: " + self.name + " has left the server!\033[0m\n") for c in (u for u in self.clients if u != self.client)]
	        lock.acquire()
	        self.clients.remove(self.client)
	        del client_list[self.name]
	        lock.release()
	        self.client.close()

#method to receive data, had a bit of decoding whch has been removed.
def recv_data (client, length):
	data = client.recv(length)
	if not data: return data
	return data

#method to send data, had a bit of encoding which has been removed. 
def send_data (client, data):
	message = str(data)
	return client.send(message)

#method that prints the commands to the user in the lobby
def help_commands(client):
	send_data(client, "\033[1;31m** HELP: The commands for this server are: \n")
	send_data(client, "**   !help -- displays this message\n")
	send_data(client, "**   !start -- starts a new game.  You will add users until you have 2-4 players\n")
	send_data(client, "**      !cancel -- cancels game creation once you have entered the !start command.\n")
	send_data(client, "**      !go -- begins the game once you have run !start and added your players.\n")
	send_data(client, "**   !quit -- quits the server.  You will not be asked to confirm.  This works from the lobby\n")
	send_data(client, "**   !clear -- clears the screen.  This works in the lobby\n")
	send_data(client, "**   !list -- lists the users currently in the lobby.\033[0m\n")

#method that prints a user list to the client in the lobby
def list_users(client):
	send_data(client, "\033[1;31m** Currently connected clients are:\n")
	for key in client_list.keys(): send_data(client,"\033[1;31m" + key + " \033[0m",)
	send_data(client, "\n")

#handles game starting
def start_handle(user_dict, user):
        newGame = DomGame()
        newGame.startGame(user_dict, user)

#handles game building
def build_game(client, addr, name):
	game = {}
	user = name.lower()
	send_data(client, "\033[1;32m** STARTING GAME:  Please enter the names of the users you want to start a game with, one per line. Enter !go when you are ready to begin.\033[0m\n")
	game[name] = client
	while 1:
		player = recv_data(client, 1024)
		player = player.lower()
		if player not in client_list:
			if player == '!go' and len(game.keys()) >= 2:
				[send_data(c, "\033[1;32m** GAME STARTING: The following players are entering a new game: \033[0m\n") for c in clients]
				for p in game:
					clients.remove(client_list[p][0])
					client_list[p][1].ingame()
					print "client " + p + " joined game"
				start_handle(game, user)
				break
			elif player == '!go' and len(game.keys()) < 2:
				send_data(client, "\033[1;31m** You don't have enough players in your game, please add more before starting your game.\033[0m\n")
				continue
			elif player == '!go' and len(game.keys()) > 4:
				send_data(client, "\033[1;31m** You have the maximum number of players in your game, please type !go to start your game.\033[0m\n")
				continue
			elif player == '!cancel':
				send_data(client, "\033[1;31m** GAME CREATION CANCELLED **\033[0m\n")
				break
			else:
				send_data(client, "\033[1;31m** Sorry, that player doesn't appear to be connected to the server.  Please try again!\033[0m\n") 
				continue
		elif player == user:
				send_data(client, "\033[1;31m** You do not need to add yourself to the game, please add other players!\033[0m\n")
				continue
		else:
			game[player] = client_list[player][0]
			[send_data(client_list[player][0], "\033[1;32m** GAME: you have been added to a new game with " + name + "!\033[0m\n")]
			send_data(client, "\033[1;32m" + player + " has been added to the game. Current players: ",)
			for key in game.keys():
				send_data(client, str(key) + ",",)
			send_data(client, "\033[0m\n")

#starts the server up indefinitely
def start_server ():
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('192.168.0.111', 4898))
	s.listen(5)
	while 1:
		conn, addr = s.accept()
		print 'Connection from:', addr
		send_data(conn, "Welcome to the Pyminion server, please select a username:\n")
		while True:
			client_name = str(recv_data(conn, 1024))
			if client_name.lower() in client_list:
				send_data(conn, "** Sorry, that name is in use, please choose another name.\n")
			else:
				break
		send_data(conn, "Welcome to Dominion, " + client_name + "! Currently connected clients are:\n")
		for key in client_list.keys(): send_data(conn, key + " ",)
		send_data(conn, "\n")
		for client in clients: send_data(client, "** JOIN: " + client_name + " has joined the server!\n")
		clients.append(conn)
		newClient = Lobby_Client(conn, addr, client_name, clients)
		client_list[client_name.lower()] = []
		client_list[client_name.lower()].append(conn)
		client_list[client_name.lower()].append(newClient)
		client_list[client_name.lower()][1].start()

#game class, this is used to group players and start a new game
class DomGame(object):
        player1 = Player('hold')
        player2 = Player('hold')
        player3 = Player('hold')
        player4 = Player('hold')
        playerWait = [player1, player2, player3, player4]
        playerRost = []
        playerTurn = 0
        def __init__(self):
                pass

        def startGame(self, user_dict, user):
                for user, conn in user_dict.iteritems():
                        self.playerWait[0].playerName = user
                        self.playerWait[0].playerConn = conn
                        self.playerRost.append(self.playerWait[0])
                        del self.playerWait[0]
                newDeck = DomDeck()
                newDeck.buildDeck(len(self.playerRost))
                for player in self.playerRost:
                        player.deck = newDeck
                        player.roster = self.playerRost
                        player.drawToPlayer(0)
                        player.drawHand()
                        player.game = self
                self.playLoop()

        def playLoop(self):
                players = len(self.playerRost)
                while True:
                        if self.playerTurn < players:
				self.playerRost[self.playerTurn].playerTurn = True
                                self.playerRost[self.playerTurn].playTurn()
				self.playerRost[self.playerTurn].playerTurn = False
                                self.playerTurn += 1
                                continue
                        elif self.playerTurn >= players:
                                self.playerTurn = 0
                                continue
                        break

clients = []
client_list = {}
room_list = {}
start_server()
