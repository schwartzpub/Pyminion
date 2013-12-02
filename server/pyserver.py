#!/usr/bin/env python

#This is the Server component.  I will be slowly injecting the game component into this portion to run the game.
 
import socket, struct, threading, cgi, random, time, errno
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
		self.away = False
		self.event = threading.Event()

	def ingame(self):
		self.game = True

	def resume(self):
		self.game = False

	def run(self):
		lock = threading.Lock()
		while 1:
			while self.game:
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
			if data == '!away' :
				if self.away == True:
					send_data(self.client, "\033[1;31m** You are already set to away, please type !back to return from being away.\033[0m\n")
				elif self.away == False:
					self.away = True
					send_data(self.client, "\033[1;31m** You have been set as away, you cannot join a game until you set yourself back.\033[0m\n")
			if data == '!back' :
				if self.away == False:
					send_data(self.client, "\033[1;31m** You are not currently away.\033[0m\n")
				elif self.away == True:
					self.away = False
					send_data(self.client, "\033[1;31m** You have been set back from away.\033[0m\n")
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

#dominion logo
def display_logo(client):
        send_data(client, "\033[36m        :                                                                       \n")        
        send_data(client, "\033[36m   /:  X#                                                                       \n")        
        send_data(client, "\033[36m  /##/ XX                                                                       \n")        
        send_data(client, "\033[36m  /#########X                                                                   \n")        
        send_data(client, "\033[36m    -#XX#X####                                           -                      \n")        
        send_data(client, "\033[36m    X# /X  /##/                        ##               X#                      \n")        
        send_data(client, "\033[36m   //X /X   X##                   -    X:-  --    -- - -:X            --    :---\n")        
        send_data(client, "\033[36m   -XX-/X   -##:X######XX/X#X   X#/   :#X- -X##   -X#- -X#XXX#######X###X   -XX \n")        
        send_data(client, "\033[36m    #///X  /X##--     -/X###X   ##/    #/   :/##   /X  /X#:-       -/X###X   X/ \n")        
        send_data(client, "\033[36m    #/X/X ##X##           #### X:/#    #/   // X#  /X X#X#            /X###  // \n")        
        send_data(client, "\033[36m    X://X ##X#X          :X##X # -#    #/   /X  X#-:X X##X            XX##/# // \n")        
        send_data(client, "\033[36m    XX /X /###X:        -X##/##-  #/   #/   /X   /#X/  X##X/-       -:XXX  /#X/ \n")        
        send_data(client, "\033[36m    #/ /X   #X############/  /X  -##  -#X-  XX-   -#/   X###########XX#X-   -#: \n")        
        send_data(client, "\033[36m  :##/XX#/-#X           :---     :--- :--- ---:    -/  ----           ---    -: \n")        
        send_data(client, "\033[36m ##########X                                                                    \n")        
        send_data(client, "\033[36m #/:--:XX##                                                                     \n")        
        send_data(client, "\033[36m -/    X:                                                                       \n")        
        send_data(client, "\033[36m  -:   X-                                                                       \n")        
        send_data(client, "\033[36m -:    X                                                                        \n")        
        send_data(client, "\033[36m-      -                                                                        \n")                
        send_data(client, "\033[0m\n")
        time.sleep(2)
        return

#method to receive data, had a bit of decoding whch has been removed.
def recv_data (client, length):
	try:
		data = client.recv(length)

	except socket.error, e:
		if e.errno == errno.EPIPE:
			try:
				clients.remove(client)		
			except:
				pass
			for key in client_list.keys():
				if client == client_list[key][0]:
					print key + " has quit. (Broken Pipe)"
					for client in clients: send_data(client, "\033[32m** QUIT: " + key + " has been disconnected! (Broken Pipe)\033[0m\n")					
					del client_list[key]
		else:
			try:
				clients.remove(client)
			except:
				pass
			for key in client_list.keys():
				if client == client_list[key][0]:
					print key + " has quit. (Connection Reset By peer)"
					for client in clients: send_data(client, "\033[32m** QUIT: " + key + " has been disconnected! (Connection Reset By Peer)\033[0m\n")
					del client_list[key]
	if not data: return data
	return data

#method to send data, had a bit of encoding which has been removed. 
def send_data (client, data):
	message = str(data)
	try:
		return client.send(message)

	except socket.error, e:
		if e.errno == errno.EPIPE:
			try:
				clients.remove(client)
			except:
				pass
			for key in client_list.keys():
				if client == client_list[key][0]:
					print key + " has quit. (Broken Pipe)"
					for client in clients: send_data(client, "\033[32m** QUIT: " + key + " has been disconnected! (Broken Pipe)\033[0m\n")
					del client_list[key]
		else:
			try:
				clients.remove(client)
			except:
				pass
			for key in client_list.keys():
				if client == client_list[key][0]:
					print key + " has quit. (Connection Reset By peer)"
					for client in clients: send_data(client, "\033[32m** QUIT: " + key + " has been disconnected! (Connection Reset By Peer)\033[0m\n")
					del client_list[key]

#method that prints the commands to the user in the lobby
def help_commands(client):
	send_data(client, "\033[1;31m** HELP: The commands for this server are: \n")
	send_data(client, "\033[1;31m**   !help -- displays this message\n")
	send_data(client, "\033[1;31m**   !start -- starts a new game.  You will add users until you have 2-4 players\n")
	send_data(client, "\033[1;31m**      !cancel -- cancels game creation once you have entered the !start command.\n")
	send_data(client, "\033[1;31m**      !go -- begins the game once you have run !start and added your players.\n")
	send_data(client, "\033[1;31m**   !away -- sets your client to away, you will not be able to join a game if you are away.\n")
	send_data(client, "\033[1;31m**   !back -- sets your client back from away.\n")
	send_data(client, "\033[1;31m**   !quit -- quits the server.  You will not be asked to confirm.  This works from the lobby\n")
	send_data(client, "\033[1;31m**   !clear -- clears the screen.  This works in the lobby\n")
	send_data(client, "\033[1;31m**   !list -- lists the users currently in the lobby.\033[0m\n")

#method that prints a user list to the client in the lobby
def list_users(client):
	send_data(client, "\033[1;31m** Currently connected clients are:",)
	for key in client_list.keys():
		if client_list[key][1].game:
			send_data(client,"\033[34m [ " + key + " (in game) ]",)
		elif client_list[key][1].away:
			send_data(client,"\033[35m [ " + key + " (away) ]",)
		else:
			send_data(client,"\033[1;31m [ " + key + " ]",)
	send_data(client, "\033[0m\n")

#handles game starting
def start_handle(user_dict, user):
	newGame[user] = DomGame()
	newGame[user].startGame(user_dict, user)
	del newGame[user]
	return

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
				[send_data(c, "\033[1;32m** GAME STARTING: The following players are entering a new game:\n") for c in clients]
				for p in game:
					clients.remove(client_list[p][0])
					client_list[p][1].ingame()
#					[send_data(c, "[ " + p + " ]",) for c in clients]
					print "client " + p + " joined game"
#				[send_data(c, "\033[0m\n") for c in clients]
				start_handle(game, user)
				for p in game:
					try:
						send_data(client_list[p][0], '\nCLRSCRN_FULL\n')
						clients.append(client_list[p][0])
						client_list[p][1].resume()
						print "client " + p + " finished game"
					except:
						pass
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
		elif client_list[player][1].game == True or client_list[player][1].away == True:
				send_data(client, "\033[1;31m** Sorry, that user is already in a game, or is set to away.\033[0m\n")
				continue
		else:
			game[player] = client_list[player][0]
			[send_data(client_list[player][0], "\033[1;32m** GAME: you have been added to a new game with " + name + "!\033[0m\n")]
			send_data(client, "\033[1;32m" + player + " has been added to the game. Current players: ",)
			for key in game.keys():
				send_data(client, "( " + str(key) + " ) ",)
			send_data(client, "\033[0m\n")
	return

#starts the server up indefinitely
def start_server ():
	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('192.168.0.111', 4898))
	s.listen(5)
	while 1:
		conn, addr = s.accept()
		print 'Connection from:', addr
		display_logo(conn)
		send_data(conn, 'CLRSCRN_FULL\n')
		send_data(conn, "\033[36mWelcome to the Pyminion server, please select a username:\n")
		while True:
			client_name = str(recv_data(conn, 1024))
			if client_name.lower() in client_list:
				send_data(conn, "\033[1;31m** Sorry, that name is in use, please choose another name.\033[0m\n")
			else:
				break
		send_data(conn, "\033[36mWelcome to Dominion, \033[33m" + client_name + "\033[36m!  Type !help for commands. Currently connected clients are: ",)
	        for key in client_list.keys():
	                if client_list[key][1].game:
        	                send_data(conn,"\033[34m [ " + key + " (in game) ]",)
			elif client_list[key][1].away:
				send_data(conn,"\033[35m [ " + key + " (away) ]",)
                	else:
                        	send_data(conn,"\033[37m [ " + key + " ]",)
		send_data(conn, "\033[0m\n")
		for client in clients: send_data(client, "\033[32m** JOIN: " + client_name + " has joined the server!\033[0m\n")
		clients.append(conn)
		newClient = Lobby_Client(conn, addr, client_name, clients)
		client_list[client_name.lower()] = []
		client_list[client_name.lower()].append(conn)
		client_list[client_name.lower()].append(newClient)
		client_list[client_name.lower()][1].start()

#game class, this is used to group players and start a new game
class DomGame(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.player1 = Player('hold')
		self.player2 = Player('hold')
		self.player3 = Player('hold')
		self.player4 = Player('hold')
		self.playerWait = [self.player1, self.player2, self.player3, self.player4]
		self.playerRost = []
		self.playerTurn = 0
		pass

	def startGame(self, user_dict, user):
		for user, conn in user_dict.iteritems():
			self.playerWait[0].playerName = user
			self.playerWait[0].playerConn = conn
			self.playerRost.append(self.playerWait[0])
			del self.playerWait[0]
		newDeck = DomDeck(self)
		newDeck.buildDeck(len(self.playerRost))
		for player in self.playerRost:
			player.deck = newDeck
			player.roster = self.playerRost
			player.drawToPlayer(0)
			player.drawHand()
			player.game = self
		self.playLoop()
		return

	def playLoop(self):
		while True:
			players = len(self.playerRost)
			if len(self.playerRost) == 1:
				break
			try:
				self.playerTurn = int(self.playerTurn)
			except:
				break
			if self.playerTurn < players:
				self.playerRost[self.playerTurn].playerTurn = True
				self.playerRost[self.playerTurn].playTurn()
				if self.playerTurn == 'gameover':
					break
				self.playerRost[self.playerTurn].playerTurn = False
				self.playerTurn += 1
				continue
			elif self.playerTurn >= players:
				self.playerTurn = 0
				continue
			break
		return
newGame = {}
clients = []
client_list = {}
room_list = {}
start_server()
