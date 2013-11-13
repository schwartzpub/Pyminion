#Dominion Deck Class

#Import classes
import random
import os
import copy
import sys
import socket
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
	smithyCard = SmithyCard()
	spyCard = SpyCard()
	thiefCard = ThiefCard()
	throneRoomCard = ThroneRoomCard()
	councilRoomCard = CouncilRoomCard()
	festivalCard = FestivalCard()
	laboratoryCard = LaboratoryCard()
	libraryCard = LibraryCard()
	marketCard = MarketCard()
	mineCard = MineCard()
	witchCard = WitchCard()
	adventurerCard = AdventurerCard()
		
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
	curseCard = CurseCard()
	curseCards = []

	#kingdom Cards --- [Description, Cost, Value]
	dominionCards = [
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
		remodelCard,
		spyCard,
		smithyCard,
		thiefCard,
		throneRoomCard,
		councilRoomCard,
		festivalCard,
		laboratoryCard,
		libraryCard,
		marketCard,
		mineCard,
		adventurerCard]
		
	intrigueCards = []

	kingdomCardPicks = []
	kingdomCards = {}

	def __init__(self):
		pass

# Method to build the starting deck, inculding treasure, victory, and kingdom cards
# Makes a "pile" for each card type, saved as lists and dictionaries
	def buildDeck(self, players):
		self.kingdomCardPicks = random.sample(self.dominionCards, 10)
		self.kingdomCardPicks.sort(key=lambda x: x.cost, reverse=True)		
		for i in range(len(self.kingdomCardPicks)):
			if self.kingdomCardPicks[i].victory == True:
				if players == 2:
					x = 8
				else:
					x = 12
				for y in range(x):
					if y == 0:
						self.kingdomCards['card' + str(i)] = [self.kingdomCardPicks[i]]
					else:
						self.kingdomCards['card' + str(i)].append(self.kingdomCardPicks[i])
			else:
				for x in range(10):
					if x == 0:
						self.kingdomCards['card' + str(i)] = [self.kingdomCardPicks[i]]
					else:
						self.kingdomCards['card' + str(i)].append(self.kingdomCardPicks[i])
		if players == 2:
			x = 8
		else:
			x = 12
		for i in range(x):
			self.provinceCards.append(self.provinceCard)
			self.duchyCards.append(self.duchyCard)
			self.estateCards.append(self.estateCard)
		for i in range(30):
			self.goldCards.append(self.goldCard)
		for i in range(40):
			self.silverCards.append(self.silverCard)
		for i in range(60):
			self.copperCards.append(self.copperCard)
		for i in range((players * 10) - 10):
			self.curseCards.append(self.curseCard)
#		if any(i.potion == True for i,value in self.kingdomCardPicks[value]):
#			pass

	def send_data(self, client, data):
        	message = str(data)
	        return client.sendall(message)

	def printDeckCards(self, roster):
		for user in roster:
			self.send_data(user.playerConn, "CLRSCRN_FULL\n")
			self.send_data(user.playerConn, "\n")
			self.send_data(user.playerConn, "[P]" + ProvinceCard.cardColor + ProvinceCard.cardName + "\033[0m  (" + str(len(self.provinceCards)) + "): $" + str(ProvinceCard.cost) + "   [G]" + GoldCard.cardColor + GoldCard.cardName + "\033[0m    (" + str(len(self.goldCards)) + "): $" + str(GoldCard.cost))
			self.send_data(user.playerConn, "   [0]" + self.kingdomCards['card0'][0].cardColor +  self.kingdomCards['card0'][0].cardName + "\033[0m  " + (" " * (12 - len(self.kingdomCards['card0'][0].cardName))) + " (" + str(len(self.kingdomCards['card0'])).zfill(2) + "): $" + str(self.kingdomCards['card0'][0].cost))
			self.send_data(user.playerConn, "   [5]" + self.kingdomCards['card5'][0].cardColor +  self.kingdomCards['card5'][0].cardName + "\033[0m  " + (" " * (12 - len(self.kingdomCards['card5'][0].cardName))) + " (" + str(len(self.kingdomCards['card5'])).zfill(2) + "): $" + str(self.kingdomCards['card5'][0].cost) + "\n")
			self.send_data(user.playerConn, "[D]" + DuchyCard.cardColor + DuchyCard.cardName + "\033[0m     (" + str(len(self.duchyCards)) + "): $" + str(DuchyCard.cost) + "   [S]" + SilverCard.cardColor + SilverCard.cardName + "\033[0m  (" + str(len(self.silverCards)) + "): $" + str(SilverCard.cost))
			self.send_data(user.playerConn, "   [1]" + self.kingdomCards['card1'][0].cardColor +  self.kingdomCards['card1'][0].cardName + "\033[0m  " + (" " * (12 - len(self.kingdomCards['card1'][0].cardName))) + " (" + str(len(self.kingdomCards['card1'])).zfill(2) + "): $" + str(self.kingdomCards['card1'][0].cost))
			self.send_data(user.playerConn, "   [6]" + self.kingdomCards['card6'][0].cardColor +  self.kingdomCards['card6'][0].cardName + "\033[0m  " + (" " * (12 - len(self.kingdomCards['card6'][0].cardName))) + " (" + str(len(self.kingdomCards['card6'])).zfill(2) + "): $" + str(self.kingdomCards['card6'][0].cost) + "\n")
			self.send_data(user.playerConn, "[E]" + EstateCard.cardColor + EstateCard.cardName + "\033[0m    (" + str(len(self.estateCards)) + "): $" + str(EstateCard.cost) + "   [C]" + CopperCard.cardColor + CopperCard.cardName + "\033[0m  (" + str(len(self.copperCards)) + "): $" + str(CopperCard.cost))
			self.send_data(user.playerConn, "   [2]" + self.kingdomCards['card2'][0].cardColor +  self.kingdomCards['card2'][0].cardName + "\033[0m  " + (" " * (12 - len(self.kingdomCards['card2'][0].cardName))) + " (" + str(len(self.kingdomCards['card2'])).zfill(2) + "): $" + str(self.kingdomCards['card2'][0].cost))
			self.send_data(user.playerConn, "   [7]" + self.kingdomCards['card7'][0].cardColor +  self.kingdomCards['card7'][0].cardName + "\033[0m  " + (" " * (12 - len(self.kingdomCards['card7'][0].cardName))) + " (" + str(len(self.kingdomCards['card7'])).zfill(2) + "): $" + str(self.kingdomCards['card7'][0].cost) + "\n")
			self.send_data(user.playerConn, "					  ")
			self.send_data(user.playerConn, "   [3]" + self.kingdomCards['card3'][0].cardColor +  self.kingdomCards['card3'][0].cardName + "\033[0m  " + (" " * (12 - len(self.kingdomCards['card3'][0].cardName))) + " (" + str(len(self.kingdomCards['card3'])).zfill(2) + "): $" + str(self.kingdomCards['card3'][0].cost))
			self.send_data(user.playerConn, "   [8]" + self.kingdomCards['card8'][0].cardColor +  self.kingdomCards['card8'][0].cardName + "\033[0m  " + (" " * (12 - len(self.kingdomCards['card8'][0].cardName))) + " (" + str(len(self.kingdomCards['card8'])).zfill(2) + "): $" + str(self.kingdomCards['card8'][0].cost) + "\n")
			self.send_data(user.playerConn, "[U]" + CurseCard.cardColor + CurseCard.cardName + "\033[0m    (" + str(len(self.curseCards)).zfill(2) + "): $" + str(CurseCard.cost) + "                      ")
			self.send_data(user.playerConn, "   [4]" + self.kingdomCards['card4'][0].cardColor +  self.kingdomCards['card4'][0].cardName + "\033[0m  " + (" " * (12 - len(self.kingdomCards['card4'][0].cardName))) + " (" + str(len(self.kingdomCards['card4'])).zfill(2) + "): $" + str(self.kingdomCards['card4'][0].cost))
			self.send_data(user.playerConn, "   [9]" + self.kingdomCards['card9'][0].cardColor +  self.kingdomCards['card9'][0].cardName + "\033[0m  " + (" " * (12 - len(self.kingdomCards['card9'][0].cardName))) + " (" + str(len(self.kingdomCards['card9'])).zfill(2) + "): $" + str(self.kingdomCards['card9'][0].cost) + "\n")

	def readCard(self, number, conn):
		cardToRead = 'card' + str(int(number))
		self.send_data(conn, 'CLRSCRN_FULL\n')
		self.send_data(conn, "\033[36m  Card Name: \033[0m" + self.kingdomCards[cardToRead][0].cardColor + self.kingdomCards[cardToRead][0].cardName + "\n")
		self.send_data(conn, "\033[36m  Description: \033[0m" + self.kingdomCards[cardToRead][0].description + "\n")
		self.send_data(conn, "\n\033[32m  Cost:\033[0m $" + str(self.kingdomCards[cardToRead][0].cost) + "\n")
		self.send_data(conn, ("\n\n\033[1;31m  Press (y) when finished...\033[0m\n"))
		while True:
			done_reading = self.recv_data(conn, 1024)
			if done_reading != 'y':
				self.send_data(conn, "\n\n\033[1;31m  Press (y) when finished...\033[0m\n")
				continue
			else:
				return
