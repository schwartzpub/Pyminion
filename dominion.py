#Dominion game....this should go terribly.

#imports
import os
import random
import sys
from dominiondeck import *
from dominioncards import *

#global vars
rooms = []
playerDeck = []
playerDiscard = []
playerHand = []
playerPlay = []
playerName = ""
gameRoom = ""

#Dominion Game Class
class DomGame(object):
	boardName = ' '
	def __init__(self, userName, roomName):
		self.userName = userName
		self.roomName = roomName

	def startGame(self, userName, roomName, players):
		if roomName in rooms:
			joinGame(userName, roomName)
		else:
			self.createGame(userName, roomName)
			newDeck = DomDeck()
			actionPile,provincePile,duchyPile,estatePile,goldPile,silverPile,copperPile = newDeck.buildDeck(int(players))
		return actionPile,provincePile,duchyPile,estatePile,goldPile,silverPile,copperPile

	def joinGame(self):
		if roomName not in rooms:
			self.createGame(userName, roomName)
		else:
			pass

	def createGame(self, userName, roomName):
		boardName = [roomName, userName]
		rooms.append(boardName)
		os.system('clear')

# Card play methods
def drawToPlayer(playerDeck, hand, card):
	if hand == 0:
		for i in range(3):
			playerDeck.append(EstateCard)
		for i in range(7):
			playerDeck.append(CopperCard)
		random.shuffle(playerDeck)
	elif hand > 0:
		pass
	return playerDeck

def drawHand():
	for i in range(5):
		playerHand.append(playerDeck[0])
		del playerDeck[0]
	return playerHand		

def playTurn(actions, buys, treasure):
	playerTurnBuys = buys
	playerTurnActions = actions
	playerTurnTreasure = treasure
	printPlayerHand(actions, buys, treasure)
	playtype = raw_input("\n\n What would you like to do: (P)lay, (B)uy, P(a)ss? ")
	if playerTurnActions == 0 and sum(p.cardType == 'treasure' for p in playerHand) <= 0:
		pass
	if playtype.lower() == 'p':
		i = int(raw_input("  Which would you like to play: (n)umber? "))
		while True:
			if i > (len(playerHand)):
				i = int(raw_input("  Invalid choice, please pick a (n)umber: "))
			elif playerHand[i - 1].cardType == 'treasure':
				playerPlay.append(playerHand[i - 1])
				playerTurnTreasure += playerHand[i - 1].value
				del playerHand[i - 1]
				playerTurnActions = 0
				os.system('clear')
				playTurn(playerTurnBuys, playerTurnActions, playerTurnTreasure)				
			elif playerHand[i - 1].cardType == 'action':
				break
							
	elif playtype.lower() == 'b':
		pass
	elif playtype.lower() == 'a':
		pass				 
	else:
		print "That is not an available choice...."
		playTurn()

# Printing methods
def printDeckCards():
	print "\n"
	print "  " + ProvinceCard.cardColor + ProvinceCard.cardName + "\033[0m  (" + str(len(province)) + "): $" + str(ProvinceCard.cost) + "   " + GoldCard.cardColor + GoldCard.cardName + "\033[0m    (" + str(len(gold)) + "): $" + str(GoldCard.cost),
	print "   " + action['card0'][0].cardColor +  action['card0'][0].cardName + "\033[0m  " + (" " * (12 - len(action['card0'][0].cardName))) + " (" + str(len(action['card0'])) + "): $" + str(action['card0'][0].cost),
	print "   " + action['card1'][0].cardColor +  action['card1'][0].cardName + "\033[0m  " + (" " * (12 - len(action['card1'][0].cardName))) + " (" + str(len(action['card1'])) + "): $" + str(action['card1'][0].cost)
	print "  " + DuchyCard.cardColor + DuchyCard.cardName + "\033[0m     (" + str(len(duchy)) + "): $" + str(DuchyCard.cost) + "   " + SilverCard.cardColor + SilverCard.cardName + "\033[0m  (" + str(len(silver)) + "): $" + str(SilverCard.cost),
        print "   " + action['card2'][0].cardColor +  action['card2'][0].cardName + "\033[0m  " + (" " * (12 - len(action['card2'][0].cardName))) + " (" + str(len(action['card2'])) + "): $" + str(action['card2'][0].cost), 
        print "   " + action['card3'][0].cardColor +  action['card3'][0].cardName + "\033[0m  " + (" " * (12 - len(action['card3'][0].cardName))) + " (" + str(len(action['card3'])) + "): $" + str(action['card3'][0].cost)
	print "  " + EstateCard.cardColor + EstateCard.cardName + "\033[0m    (" + str(len(estate)) + "): $" + str(EstateCard.cost) + "   " + CopperCard.cardColor + CopperCard.cardName + "\033[0m  (" + str(len(copper)) + "): $" + str(CopperCard.cost),
        print "   " + action['card4'][0].cardColor +  action['card4'][0].cardName + "\033[0m  " + (" " * (12 - len(action['card4'][0].cardName))) + " (" + str(len(action['card4'])) + "): $" + str(action['card4'][0].cost), 
        print "   " + action['card5'][0].cardColor +  action['card5'][0].cardName + "\033[0m  " + (" " * (12 - len(action['card5'][0].cardName))) + " (" + str(len(action['card5'])) + "): $" + str(action['card5'][0].cost)
	print "                                      ",
        print "   " + action['card6'][0].cardColor +  action['card6'][0].cardName + "\033[0m  " + (" " * (12 - len(action['card6'][0].cardName))) + " (" + str(len(action['card6'])) + "): $" + str(action['card6'][0].cost), 
        print "   " + action['card7'][0].cardColor +  action['card7'][0].cardName + "\033[0m  " + (" " * (12 - len(action['card7'][0].cardName))) + " (" + str(len(action['card7'])) + "): $" + str(action['card7'][0].cost)
	print "                                      ",
        print "   " + action['card8'][0].cardColor +  action['card8'][0].cardName + "\033[0m  " + (" " * (12 - len(action['card8'][0].cardName))) + " (" + str(len(action['card8'])) + "): $" + str(action['card8'][0].cost), 
        print "   " + action['card9'][0].cardColor +  action['card9'][0].cardName + "\033[0m  " + (" " * (12 - len(action['card9'][0].cardName))) + " (" + str(len(action['card9'])) + "): $" + str(action['card9'][0].cost)

def printPlayerHand(actions, buys, treasures):
	playerTurnActions = actions
	playerTurnBuys = buys
	playerTurnTreasure = treasures
	printDeckCards()
	printPlayerCount()
	printTurnCount(playerTurnActions, playerTurnBuys, playerTurnTreasure)
	print "\n  Current Hand (" + playerName + "):\n ",
	for i in range(len(playerHand)):
		print playerHand[i].cardColor + playerHand[i].cardName + " \033[0m",

def printPlayerCount():
	sys.stdout.write("\n\n  Deck [")
	for i in range(len(playerDeck)):
		sys.stdout.write("|")
	sys.stdout.write("] -- Discard [")
	for i in range(len(playerDiscard)):
		sys.stdout.write("|")
	sys.stdout.write("]\n\n")

def printTurnCount(actions, buys, treasure):
	playerTurnActions = actions
	playerTurnBuys = buys
	playerTurnTreasure = treasure
	print "  Actions: " + str(playerTurnActions) + "    Buys ($" + str(playerTurnTreasure) + "): " + str(playerTurnBuys)  
 
#Run Dominion Game
os.system('clear')
playerName = raw_input("What is your username? ")
gameRoom = raw_input("What is the room name? ")
gameName = DomGame(playerName, gameRoom)

#Get a new deck to play the game with
action,province,duchy,estate,gold,silver,copper = gameName.startGame(gameName.userName, gameName.roomName, raw_input("How many players? "))

playerDeck = drawToPlayer(playerDeck, 0, 0)

#play turn
playerHand = drawHand()
playTurn(1, 1, 0)

