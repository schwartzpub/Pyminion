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
		if len(playerDeck) > 0:
			playerHand.append(playerDeck[0])
			del playerDeck[0]
		else:
			playerDiscardToDeck()
			playerHand.append(playerDeck[0])
			del playerDeck[0]
	return playerHand		

def playTurn(actions, buys, treasure, hand):
	playerTurnBuys = buys
	playerTurnActions = actions
	playerTurnTreasure = treasure
	playerHand = hand
	printPlayerHand(actions, buys, treasure)
	playtype = raw_input("\n\n What would you like to do: (P)lay, (B)uy, P(a)ss, (R)ead? ")
	if playerTurnActions == 0 and sum(p.cardType == 'treasure' for p in playerPlay) <= 0 or playtype.lower == 'a':
		pass
	elif playtype.lower() == 'p':
		play(playerTurnActions, playerTurnBuys, playerTurnTreasure, playerHand)
	elif playtype.lower() == 'b':
		buy(playerTurnActions, playerTurnBuys, playerTurnTreasure, playerHand)
	elif playtype.lower() == 'r':
		readCard(raw_input("  Which card would you like to read: (n)umber? "))
		os.system('clear')
		playTurn(playerTurnActions, playerTurnBuys, playerTurnTreasure, playerHand)
	else:
		print " That is not an available choice...."
		playTurn(playerTurnActions, playerTurnBuys, playerTurnTreasure, playerHand)

def play(actions, buys, treasure, hand):
	playerTurnActions = actions
	playerTurnBuys = buys
	playerTurnTreasure = treasure
	playerHand = hand
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
                        break
		elif playerHand[i - 1].cardType == 'action':
                        break
        playTurn(playerTurnActions, playerTurnBuys, playerTurnTreasure, playerHand)

def buy(actions, buys, treasure, hand):
        playerTurnActions = actions
        playerTurnBuys = buys
        playerTurnTreasure = treasure
        playerHand = hand
	i = raw_input("  Which card would you like to buy? ")
        while True:
        	if i not in ['p', 'd', 'e', 'g', 's', 'c', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                	i = raw_input("  Invalid selection!  Which card would you like to buy? ")
		else:
                	if i.lower() in ['p', 'd', 'e', 'g', 's', 'c']:
                        	p = province[0]
                                d = duchy[0]
                                e = estate[0]
                                g = gold[0]
                                s = silver[0]
                                c = copper[0]
                                i = eval(i)
                                playerPlay.append(i)
                                playerTurnTreasure -= i.value
                                del i
                                playerTurnBuys -= 1
                                break
                        elif i in range(1,11):
                                i = 'card' + str(int(i) - 1)
                                playerPlay.append(action[i][0])
                                playerTurnTreasure -= action[i][0].value
                                del action[i][0]
                                playerTurnBuys -= 1
                                break
	if playerTurnBuys < 1:
        	playerHandCleanup(playerPlay, playerHand)
                playerHand = drawHand()
                playTurn(1, 1, 0, playerHand)
        else:
                playTurn(playerTurnActions, playerTurnBuys, playerTurnTreasure, playerHand)

def playerHandCleanup(play, hand):
	playerPlay = play
	playerHand = hand
	x = len(playerPlay)
	y = len(playerHand)
	while x == len(playerPlay) and x > 0:
		playerDiscard.append(playerPlay[0])
		del playerPlay[0]
		x -= 1
	while y == len(playerHand) and y > 0:
		playerDiscard.append(playerHand[0])
		del playerHand[0]
		y -= 1

def playerDiscardToDeck():
	x = len(playerDiscard)
	while x == len(playerDiscard) and x > 0:
		playerDeck.append(playerDiscard[0])
		del playerDiscard[0]
		x -= 1

# Printing methods
def printDeckCards():
	os.system('clear')
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

def readCard(number):
	cardToRead = 'card' + str(int(number) - 1)
	os.system('clear')
	print "\033[36m  Card Name: \033[0m" + action[cardToRead][0].cardColor + action[cardToRead][0].cardName
	print "\033[36m  Description: \033[0m" + action[cardToRead][0].description
	print "\n\033[32m  Cost:\033[0m $" + str(action[cardToRead][0].cost)
	raw_input("\n\n\033[1;31m  Press key...\033[0m")
 
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
playTurn(1, 1, 0, playerHand)

