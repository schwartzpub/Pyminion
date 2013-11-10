#!/usr/bin/env python

#This is the Server component.  I will be slowly injecting the game component into this portion to run the game.
 
import socket, struct, threading, cgi, random
from dominiondeck import *
from dominioncards import *
from dominionplayer import *
 
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
		if data == '!start': build_game(client, addr, name)
		if data == '!help' : help_commands(client)
		if data == '!list' : list_users(client)
		if data == '!clear' : send_data(client, 'CLRSCRN_FULL')
		lock.acquire()
		[send_data(c, "<" + name + "> " + data) for c in (u for u in clients if u != client)]
		lock.release()
	print 'Client closed:', addr
	[send_data(c, "\033[1;31m** QUIT: " + name + " has left the server!\033[0m") for c in (u for u in clients if u != client)]
	lock.acquire()
	clients.remove(client)
	del client_list[name]
	lock.release()
	client.close()

def help_commands(client):
	send_data(client, "\033[1;31m** HELP: The commands for this server are: ")
	send_data(client, "**   !help -- displays this message")
	send_data(client, "\n**   !start -- starts a new game.  You will add users until you have 2-4 players.")
	send_data(client, "\n**      !cancel -- cancels game creation once you have entered the !start command.")
	send_data(client, "\n**      !go -- begins the game once you have run !start and added your players.")
	send_data(client, "\n**   !quit -- quits the server.  You will not be asked to confirm.  This works from the lobby.")
	send_data(client, "\n**   !clear -- clears the screen.  This works in the lobby.")
	send_data(client, "\n**   !list -- lists the users currently in the lobby.\033[0m")

def list_users(client):
	send_data(client, "\033[1;31m** Currently connected clients are: ",)
	for key in client_list.keys(): send_data(client,"\033[1;31m" + key + " \033[0m",)

def start_handle(user_dict, user):
        newGame = DomGame()
        newGame.startGame(user_dict, user)

def build_game(client, addr, name):
	game = {}
	user = name.lower()
	send_data(client, '\033[1;32m** STARTING GAME:  Please enter the names of the users you want to start a game with, one per line. Enter !go when you are ready to begin.\033[0m')
	game[name] = client
	while 1:
		player = recv_data(client, 1024)
		player = player.lower()
		if player not in client_list:
			if player == '!go' and len(game.keys()) >= 2:
				[send_data(c, "\033[1;32m** GAME STARTING: The following players are entering a new game: \033[0m",) for c in clients]
				for p in game:
					del client_list[p]
				threading.Thread(target = start_handle, args = (game, user)).start()
			elif player == '!go' and len(game.keys()) < 2:
				send_data(client, "\033[1;31m** You don't have enough players in your game, please add more before starting your game.\033[0m")
				continue
			elif player == '!go' and len(game.keys()) > 4:
				send_data(client, "\033[1;31m** You have the maximum number of players in your game, please type !go to start your game.\033[0m")
				continue
			elif player == '!cancel':
				send_data(client, "\033[1;31m** GAME CREATION CANCELLED **\033[0m")
				break
			else:
				send_data(client, "\033[1;31m** Sorry, that player doesn't appear to be connected to the server.  Please try again!\033[0m") 
				continue
		elif player == user:
				send_data(client, "\033[1;31m** You do not need to add yourself to the game, please add other players!\033[0m")
				continue
		else:
			game[player] = client_list[player]
			[send_data(client_list[player], "\033[1;32m** GAME: you have been added to a new game with " + name + "!\033[0m")]

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
				send_data(conn, "** Sorry, that name is in use, please choose another name.")
			else:
				break
		send_data(conn, "Welcome to Dominion, " + client_name + "! Currently connected clients are: ")
		for key in client_list.keys(): send_data(conn, key + " ",)
		for client in clients: send_data(client, "** JOIN: " + client_name + " has joined the server!")
		clients.append(conn)
		client_list[client_name.lower()] = conn
		threading.Thread(target = handle, args = (conn, addr, client_name)).start()

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
                                self.playerRost[self.playerTurn].playTurn()
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
