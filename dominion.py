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
	player1 = Player('hold')
	player2 = Player('hold')
	player3 = Player('hold')
	player4 = Player('hold')
	playerWait = [player1, player2, player3, player4]
	boardName = ' '
	def __init__(self):
		pass
	def startGame(self):
		while True:
			x = raw_input("Welcome to Dominion! (J)oin a game or (N)ew game? ")
			if x.lower() == 'j':
				print "There are no current games to join!"
				self.startGame()
				break
			elif x.lower() == 'n':
				roomName = raw_input("What will be the name of your room? ")
				players = raw_input("How many players (2 - 4)? ")
				while True:
					if not players or players not in ['2', '3', '4']:
						players = raw_input(" Invalid number of players, please choose a number between 2 and 4! ")
					elif int(players) > 4 or int(players) < 2:
						players = raw_input(" Invalid number of players, please choose a number between 2 and 4! ")
					else:
						for i in range(int(players)):	
							playerName = raw_input(" Player " + str(i + 1) + " name? ")
							while True:
								if not playerName:
									continue
								else:
									self.playerWait[i].playerName = playerName
									playerRost.append(self.playerWait[i])
									break
						break
				newGame.createGame(roomName, playerRost[0].playerName)
				newDeck = DomDeck()
				newDeck.buildDeck(int(players))
			else:
				print "That is not a valid option!"
				self.startGame()
				break
			for player in playerRost:
				player.deck = newDeck
				player.roster = playerRost
				player.drawToPlayer(0)
				player.drawHand()

			self.playLoop()

	def joinGame(self):
		if roomName not in rooms:
			self.createGame(userName, roomName)
		else:
			pass

	def createGame(self, userName, roomName):
		boardName = [roomName, userName]
		rooms.append(boardName)
		os.system('clear')

	def playLoop(self):
		players = len(playerRost)
		playerTurn = 0
		while True:
			if playerTurn < players:
				playerRost[playerTurn].playTurn(1, 1)
				playerTurn += 1
				continue
			elif playerTurn >= players:
				playerTurn = 0
				continue
			break
			
#Run Dominion Game
os.system('clear')
newGame = DomGame()

#Get a new deck to play the game with
newGame.startGame()

