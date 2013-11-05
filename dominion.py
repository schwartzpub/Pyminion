#Dominion game....this should go terribly.

#imports
import os
import random
import sys
from dominiondeck import *
from dominioncards import *
from dominionplayer import *

#global vars
rooms = []
playerRost = []
playerName = ""
gameRoom = ""

#Dominion Game Class
class DomGame(object):
	player1 = Player()
	player2 = Player()
	player3 = Player()
	player4 = Player()
	playerWait = [player1, player2, player3, player4]
	boardName = ' '
	def __init__(self):
		pass
	def startGame(self):
		x = raw_input("Welcome to Dominion! (J)oin a game or (N)ew game? ")
		if x.lower() == 'j':
			pass
		elif x.lower() == 'n':
			roomName = raw_input("What will be the name of your room? ")
			players = int(raw_input("How many players (2 - 4)? "))
			while True:
				if players > 4 or players < 2:
					players = int(raw_input(" Invalid number of players, please choose a number between 2 and 4! "))
				else:
					for i in range(int(players)):
						playerName = raw_input(" Player " + str(i + 1) + " name? ")
						self.playerWait[i].playerName = playerName
						playerRost.append(self.playerWait[i])
						print playerRost[i].playerName
				break
			for i in range(len(playerRost)):
                                playerRost[i].drawToPlayer(0)
	                        playerRost[i].drawHand()
			newGame.createGame(roomName, playerRost[0].playerName)
			newDeck = DomDeck()
			newDeck.buildDeck(int(players))
		playerRost[0].playTurn(newDeck, 1, 1)

	def joinGame(self):
		if roomName not in rooms:
			self.createGame(userName, roomName)
		else:
			pass

	def createGame(self, userName, roomName):
		boardName = [roomName, userName]
		rooms.append(boardName)
		os.system('clear')

#Run Dominion Game
os.system('clear')
newGame = DomGame()

#Get a new deck to play the game with
newGame.startGame()

