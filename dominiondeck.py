#Dominion Deck Class

#Import classes
import random
import os
import copy
import sys
from dominioncards import *

#Main Deck Class
class DomDeck(object):
	cellarCard = CellarCard()
	chapelCard = ChapelCard()
	moatCard = MoatCard()
	chancellorCard = ChancellorCard()
	villageCard = VillageCard()
	woodcutterCard = WoodcutterCard()
	workshopCard = WorkshopCard()
	bureaucratCard = BureaucratCard()
	feastCard = FeastCard()
	gardensCard = GardensCard()
	militiaCard = MilitiaCard()
	moneylenderCard = MoneylenderCard()
	remodelCard = RemodelCard()
		
	#Treasure Cards --- [Cost, Value]
	goldCard = GoldCard()
	silverCard = SilverCard()
	copperCard = CopperCard()
	goldCards = []
	silverCards = []
	copperCards = []

	#Victory Cards --- [Cost, Value]
	provinceCard = ProvinceCard()
	duchyCard = DuchyCard()
	estateCard = EstateCard()
	provinceCards = []
	duchyCards = []
	estateCards = []

	#Curse Cards --- [Cost, Value]
	curseCards = ["curseCard"]

	#Action Cards --- [Description, Cost, Value]
	actionTypes = [
		cellarCard,
		moatCard,
		chancellorCard,
		chapelCard,
		villageCard,
		woodcutterCard,
		workshopCard,
		bureaucratCard,
		feastCard,
		gardensCard,
		militiaCard,
		moneylenderCard,
		remodelCard]
	actionCardPicks = []
	actionCards = {}

	def __init__(self):
		pass

# Method to build the starting deck, inculding treasure, victory, and action cards
# Makes a "pile" for each card type, saved as lists and dictionaries
	def buildDeck(self, players):
		self.actionCardPicks = random.sample(self.actionTypes, 10)
		self.actionCardPicks.sort(key=lambda x: x.cost, reverse=True)		
		for i in range(len(self.actionCardPicks)):
			for x in range(10):
				if x == 0:
					self.actionCards['card' + str(i)] = [self.actionCardPicks[i]]
				else:
					self.actionCards['card' + str(i)].append(self.actionCardPicks[i])
		if players == 2:
			for i in range(8):
				self.provinceCards.append(self.provinceCard)
				self.duchyCards.append(self.duchyCard)
				self.estateCards.append(self.estateCard)
			for i in range(30):
				self.goldCards.append(self.goldCard)
			for i in range(40):
				self.silverCards.append(self.silverCard)
			for i in range(60):
				self.copperCards.append(self.copperCard)
		else:
			return

	def printDeckCards(self):
		os.system('clear')
		print "\n"
		print "  [P]" + ProvinceCard.cardColor + ProvinceCard.cardName + "\033[0m  (" + str(len(self.provinceCards)) + "): $" + str(ProvinceCard.cost) + "   [G]" + GoldCard.cardColor + GoldCard.cardName + "\033[0m    (" + str(len(self.goldCards)) + "): $" + str(GoldCard.cost),
		print "   [0]" + self.actionCards['card0'][0].cardColor +  self.actionCards['card0'][0].cardName + "\033[0m  " + (" " * (12 - len(self.actionCards['card0'][0].cardName))) + " (" + str(len(self.actionCards['card0'])) + "): $" + str(self.actionCards['card0'][0].cost),
		print "   [5]" + self.actionCards['card5'][0].cardColor +  self.actionCards['card5'][0].cardName + "\033[0m  " + (" " * (12 - len(self.actionCards['card5'][0].cardName))) + " (" + str(len(self.actionCards['card5'])) + "): $" + str(self.actionCards['card5'][0].cost)
		print "  [D]" + DuchyCard.cardColor + DuchyCard.cardName + "\033[0m     (" + str(len(self.duchyCards)) + "): $" + str(DuchyCard.cost) + "   [S]" + SilverCard.cardColor + SilverCard.cardName + "\033[0m  (" + str(len(self.silverCards)) + "): $" + str(SilverCard.cost),
		print "   [1]" + self.actionCards['card1'][0].cardColor +  self.actionCards['card1'][0].cardName + "\033[0m  " + (" " * (12 - len(self.actionCards['card1'][0].cardName))) + " (" + str(len(self.actionCards['card1'])) + "): $" + str(self.actionCards['card1'][0].cost),
		print "   [6]" + self.actionCards['card6'][0].cardColor +  self.actionCards['card6'][0].cardName + "\033[0m  " + (" " * (12 - len(self.actionCards['card6'][0].cardName))) + " (" + str(len(self.actionCards['card6'])) + "): $" + str(self.actionCards['card6'][0].cost)
		print "  [E]" + EstateCard.cardColor + EstateCard.cardName + "\033[0m    (" + str(len(self.estateCards)) + "): $" + str(EstateCard.cost) + "   [C]" + CopperCard.cardColor + CopperCard.cardName + "\033[0m  (" + str(len(self.copperCards)) + "): $" + str(CopperCard.cost),
		print "   [2]" + self.actionCards['card2'][0].cardColor +  self.actionCards['card2'][0].cardName + "\033[0m  " + (" " * (12 - len(self.actionCards['card2'][0].cardName))) + " (" + str(len(self.actionCards['card2'])) + "): $" + str(self.actionCards['card2'][0].cost),
		print "   [7]" + self.actionCards['card7'][0].cardColor +  self.actionCards['card7'][0].cardName + "\033[0m  " + (" " * (12 - len(self.actionCards['card7'][0].cardName))) + " (" + str(len(self.actionCards['card7'])) + "): $" + str(self.actionCards['card7'][0].cost)
		print "					    ",
		print "   [3]" + self.actionCards['card3'][0].cardColor +  self.actionCards['card3'][0].cardName + "\033[0m  " + (" " * (12 - len(self.actionCards['card3'][0].cardName))) + " (" + str(len(self.actionCards['card3'])) + "): $" + str(self.actionCards['card3'][0].cost),
		print "   [8]" + self.actionCards['card8'][0].cardColor +  self.actionCards['card8'][0].cardName + "\033[0m  " + (" " * (12 - len(self.actionCards['card8'][0].cardName))) + " (" + str(len(self.actionCards['card8'])) + "): $" + str(self.actionCards['card8'][0].cost)
		print "					    ",
		print "   [4]" + self.actionCards['card4'][0].cardColor +  self.actionCards['card4'][0].cardName + "\033[0m  " + (" " * (12 - len(self.actionCards['card4'][0].cardName))) + " (" + str(len(self.actionCards['card4'])) + "): $" + str(self.actionCards['card4'][0].cost),
		print "   [9]" + self.actionCards['card9'][0].cardColor +  self.actionCards['card9'][0].cardName + "\033[0m  " + (" " * (12 - len(self.actionCards['card9'][0].cardName))) + " (" + str(len(self.actionCards['card9'])) + "): $" + str(self.actionCards['card9'][0].cost)

	def readCard(self, number):
		cardToRead = 'card' + str(int(number))
		os.system('clear')
		print "\033[36m  Card Name: \033[0m" + self.actionCards[cardToRead][0].cardColor + self.actionCards[cardToRead][0].cardName
		print "\033[36m  Description: \033[0m" + self.actionCards[cardToRead][0].description
		print "\n\033[32m  Cost:\033[0m $" + str(self.actionCards[cardToRead][0].cost)
		raw_input("\n\n\033[1;31m  Press key...\033[0m")
