#Dominion Deck Class

#Import classes
import random
import os
import copy
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
		
		return self.actionCards,self.provinceCards,self.duchyCards,self.estateCards,self.goldCards,self.silverCards,self.copperCards
