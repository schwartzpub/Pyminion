#Dominion Deck Class

#Import classes
import random, os, copy, sys, socket
from dominioncards import *

#Main Deck Class
class DomDeck(object):

	def __init__(self, game):
		self.game = game		
		self.cellarCard = CellarCard(self.game)
		self.chapelCard = ChapelCard(self.game)
		self.moatCard = MoatCard(self.game)
		self.chancellorCard = ChancellorCard(self.game)
		self.villageCard = VillageCard(self.game)
		self.woodcutterCard = WoodcutterCard(self.game)
		self.workshopCard = WorkshopCard(self.game)
		self.bureaucratCard = BureaucratCard(self.game)
		self.feastCard = FeastCard(self.game)
		self.gardensCard = GardensCard(self.game)
		self.militiaCard = MilitiaCard(self.game)
		self.moneylenderCard = MoneylenderCard(self.game)
		self.remodelCard = RemodelCard(self.game)
		self.smithyCard = SmithyCard(self.game)
		self.spyCard = SpyCard(self.game)
		self.thiefCard = ThiefCard(self.game)
		self.throneRoomCard = ThroneRoomCard(self.game)
		self.councilRoomCard = CouncilRoomCard(self.game)
		self.festivalCard = FestivalCard(self.game)
		self.laboratoryCard = LaboratoryCard(self.game)
		self.libraryCard = LibraryCard(self.game)
		self.marketCard = MarketCard(self.game)
		self.mineCard = MineCard(self.game)
		self.witchCard = WitchCard(self.game)
		self.adventurerCard = AdventurerCard(self.game)
		self.embargoCard = EmbargoCard(self.game)
		self.havenCard = HavenCard(self.game)
		self.lighthouseCard = LighthouseCard(self.game)
		self.nativeVillageCard = NativeVillageCard(self.game)
		self.pearlDiverCard = PearlDiverCard(self.game)
		self.ambassadorCard = AmbassadorCard(self.game)
		self.fishingVillageCard = FishingVillageCard(self.game)
		self.lookoutCard = LookoutCard(self.game)
		self.smugglersCard = SmugglersCard(self.game)
		self.warehouseCard = WarehouseCard(self.game)
		self.caravanCard = CaravanCard(self.game)
		self.cutpurseCard = CutpurseCard(self.game)
		self.islandCard = IslandCard(self.game)
		self.navigatorCard = NavigatorCard(self.game)
		self.pirateShipCard = PirateShipCard(self.game)
		self.salvagerCard = SalvagerCard(self.game)
		self.seaHagCard = SeaHagCard(self.game)
		self.treasureMapCard = TreasureMapCard(self.game)
		self.bazaarCard = BazaarCard(self.game)
		self.explorerCard = ExplorerCard(self.game)		
		self.ghostShipCard = GhostShipCard(self.game)
		self.merchantShipCard = MerchantShipCard(self.game)
		self.outpostCard = OutpostCard(self.game)
		self.tacticianCard = TacticianCard(self.game)
		self.treasuryCard = TreasuryCard(self.game)
		self.wharfCard = WharfCard(self.game)

		#Treasure Cards --- [Cost, Value]
		self.goldCard = GoldCard(self.game)
		self.silverCard = SilverCard(self.game)
		self.copperCard = CopperCard(self.game)
		self.goldCards = []
		self.silverCards = []
		self.copperCards = []		
	
		#Victory Cards --- [Cost, Value]
		self.provinceCard = ProvinceCard(self.game)
		self.duchyCard = DuchyCard(self.game)
		self.estateCard = EstateCard(self.game)
		self.provinceCards = []
		self.duchyCards = []
		self.estateCards = []	

		#Curse Cards --- [Cost, Value]
		self.curseCard = CurseCard(self.game)
		self.curseCards = []

		#kingdom Cards --- [Description, Cost, Value]
		self.dominionCards = [
			self.embargoCard,
			self.havenCard,
			self.lighthouseCard,
			self.nativeVillageCard,
			self.pearlDiverCard,
			self.lookoutCard,
			self.smugglersCard,
			self.warehouseCard,
			self.caravanCard,
			self.cutpurseCard,
			self.islandCard,
			self.navigatorCard,
			self.pirateShipCard,
			self.salvagerCard,
			self.seaHagCard,
			self.treasureMapCard,
			self.bazaarCard,
			self.explorerCard,
			self.ghostShipCard,
			self.merchantShipCard,
			self.outpostCard,
			self.tacticianCard,
			self.treasuryCard,
			self.wharfCard,
			self.cellarCard,
			self.moatCard,
			self.chancellorCard,
			self.chapelCard,
			self.villageCard,
			self.woodcutterCard,
			self.workshopCard,
			self.bureaucratCard,
			self.feastCard,
			self.gardensCard,
			self.militiaCard,
			self.moneylenderCard,
			self.remodelCard,
			self.spyCard,
			self.smithyCard,
			self.thiefCard,
			self.throneRoomCard,
			self.councilRoomCard,
			self.festivalCard,
			self.laboratoryCard,
			self.libraryCard,
			self.marketCard,
			self.mineCard,
			self.witchCard,
			self.adventurerCard]

		self.kingdomCardPicks = []
		self.kingdomCards = {}

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
		try:
			return client.sendall(message)
		except:
			pass

	def recv_data(self, client, length):
		try:
			data = client.recv(length)
		except:
			pass
		if not data: return data
		return data

	def printDeckCards(self, roster):
		for user in roster:
#			self.send_data(user.playerConn, "CLRSCRN_FULL\n")
			self.send_data(user.playerConn, "\n")
			self.send_data(user.playerConn, (" " if not self.provinceCard.embargoed else "\033[1;31m" + str(self.provinceCard.embargo) + "\033[0m") + "[P]" + ProvinceCard.cardPrint + "\033[0m  (" + str(len(self.provinceCards)) + "): $" + str(ProvinceCard.cost) + "  " + (" " if not self.goldCard.embargoed else "\033[1;31m" + str(self.goldCard.embargo) + "\033[0m") + "[G]" + GoldCard.cardPrint + "\033[0m    (" + str(len(self.goldCards)) + "): $" + str(GoldCard.cost))
			self.send_data(user.playerConn, "  " + (" " if not self.kingdomCardPicks[0].embargoed else "\033[1;31m" + str(self.kingdomCardPicks[0].embargo) + "\033[0m") + "[0]" + self.kingdomCardPicks[0].cardPrint + "\033[0m  " + (" " * (14 - len(self.kingdomCardPicks[0].cardName))) + " (" + str(len(self.kingdomCards['card0'])).zfill(2) + "): $" + str(self.kingdomCardPicks[0].cost))
			self.send_data(user.playerConn, "  " + (" " if not self.kingdomCardPicks[5].embargoed else "\033[1;31m" + str(self.kingdomCardPicks[5].embargo) + "\033[0m") + "[5]" + self.kingdomCardPicks[5].cardPrint + "\033[0m  " + (" " * (14 - len(self.kingdomCardPicks[5].cardName))) + " (" + str(len(self.kingdomCards['card5'])).zfill(2) + "): $" + str(self.kingdomCardPicks[5].cost) + "\n")
			self.send_data(user.playerConn, (" " if not self.duchyCard.embargoed else "\033[1;31m" + str(self.duchyCard.embargo) + "\033[0m") + "[D]" + DuchyCard.cardPrint + "\033[0m     (" + str(len(self.duchyCards)) + "): $" + str(DuchyCard.cost) + "  " + (" " if not self.silverCard.embargoed else "\033[1;31m" + str(self.silverCard.embargo) + "\033[0m") + "[S]" + SilverCard.cardPrint + "\033[0m  (" + str(len(self.silverCards)) + "): $" + str(SilverCard.cost))
			self.send_data(user.playerConn, "  " + (" " if not self.kingdomCardPicks[1].embargoed else "\033[1;31m" + str(self.kingdomCardPicks[1].embargo) + "\033[0m") + "[1]" + self.kingdomCardPicks[1].cardPrint + "\033[0m  " + (" " * (14 - len(self.kingdomCardPicks[1].cardName))) + " (" + str(len(self.kingdomCards['card1'])).zfill(2) + "): $" + str(self.kingdomCardPicks[1].cost))
			self.send_data(user.playerConn, "  " + (" " if not self.kingdomCardPicks[6].embargoed else "\033[1;31m" + str(self.kingdomCardPicks[6].embargo) + "\033[0m") + "[6]" + self.kingdomCardPicks[6].cardPrint + "\033[0m  " + (" " * (14 - len(self.kingdomCardPicks[6].cardName))) + " (" + str(len(self.kingdomCards['card6'])).zfill(2) + "): $" + str(self.kingdomCardPicks[6].cost) + "\n")
			self.send_data(user.playerConn, (" " if not self.estateCard.embargoed else "\033[1;31m" + str(self.estateCard.embargo) + "\033[0m") + "[E]" + EstateCard.cardPrint + "\033[0m    (" + str(len(self.estateCards)) + "): $" + str(EstateCard.cost) + "  " + (" " if not self.copperCard.embargoed else "\033[1;31m" + str(self.copperCard.embargo) + "\033[0m") + "[C]" + CopperCard.cardPrint + "\033[0m  (" + str(len(self.copperCards)) + "): $" + str(CopperCard.cost))
			self.send_data(user.playerConn, "  " + (" " if not self.kingdomCardPicks[2].embargoed else "\033[1;31m" + str(self.kingdomCardPicks[2].embargo) + "\033[0m") + "[2]" + self.kingdomCardPicks[2].cardPrint + "\033[0m  " + (" " * (14 - len(self.kingdomCardPicks[2].cardName))) + " (" + str(len(self.kingdomCards['card2'])).zfill(2) + "): $" + str(self.kingdomCardPicks[2].cost))
			self.send_data(user.playerConn, "  " + (" " if not self.kingdomCardPicks[7].embargoed else "\033[1;31m" + str(self.kingdomCardPicks[7].embargo) + "\033[0m") + "[7]" + self.kingdomCardPicks[7].cardPrint + "\033[0m  " + (" " * (14 - len(self.kingdomCardPicks[7].cardName))) + " (" + str(len(self.kingdomCards['card7'])).zfill(2) + "): $" + str(self.kingdomCardPicks[7].cost) + "\n")
			self.send_data(user.playerConn, "					  ")
			self.send_data(user.playerConn, "  " + (" " if not self.kingdomCardPicks[3].embargoed else "\033[1;31m" + str(self.kingdomCardPicks[3].embargo) + "\033[0m") + "[3]" + self.kingdomCardPicks[3].cardPrint + "\033[0m  " + (" " * (14 - len(self.kingdomCardPicks[3].cardName))) + " (" + str(len(self.kingdomCards['card3'])).zfill(2) + "): $" + str(self.kingdomCardPicks[3].cost))
			self.send_data(user.playerConn, "  " + (" " if not self.kingdomCardPicks[8].embargoed else "\033[1;31m" + str(self.kingdomCardPicks[8].embargo) + "\033[0m") + "[8]" + self.kingdomCardPicks[8].cardPrint + "\033[0m  " + (" " * (14 - len(self.kingdomCardPicks[8].cardName))) + " (" + str(len(self.kingdomCards['card8'])).zfill(2) + "): $" + str(self.kingdomCardPicks[8].cost) + "\n")
			self.send_data(user.playerConn, (" " if not self.curseCard.embargoed else "\033[1;31m" + str(self.curseCard.embargo) + "\033[0m") + "[U]" + CurseCard.cardPrint + "\033[0m    (" + str(len(self.curseCards)).zfill(2) + "): $" + str(CurseCard.cost) + "		      ")
			self.send_data(user.playerConn, "  " + (" " if not self.kingdomCardPicks[4].embargoed else "\033[1;31m" + str(self.kingdomCardPicks[4].embargo) + "\033[0m") + "[4]" + self.kingdomCardPicks[4].cardPrint + "\033[0m  " + (" " * (14 - len(self.kingdomCardPicks[4].cardName))) + " (" + str(len(self.kingdomCards['card4'])).zfill(2) + "): $" + str(self.kingdomCardPicks[4].cost))
			self.send_data(user.playerConn, "  " + (" " if not self.kingdomCardPicks[9].embargoed else "\033[1;31m" + str(self.kingdomCardPicks[9].embargo) + "\033[0m") + "[9]" + self.kingdomCardPicks[9].cardPrint + "\033[0m  " + (" " * (14 - len(self.kingdomCardPicks[9].cardName))) + " (" + str(len(self.kingdomCards['card9'])).zfill(2) + "): $" + str(self.kingdomCardPicks[9].cost) + "\n")

	def readCard(self, number, conn):
		try:
			cardToRead = 'card' + str(int(number))
		except:
			return
		self.send_data(conn, 'CLRSCRN_FULL\n')
		self.send_data(conn, "\033[36m  Card Name: \033[0m" + self.kingdomCards[cardToRead][0].cardPrint + "\n")
		self.send_data(conn, "\033[36m  Description: \033[0m" + self.kingdomCards[cardToRead][0].description + "\n")
		self.send_data(conn, "\n\033[32m  Cost:\033[0m $" + str(self.kingdomCards[cardToRead][0].cost) + "\n")
		self.send_data(conn, ("\n\n\033[1;31m  Press (y) when finished...\033[0m\n"))
		while True:
			done_reading = self.recv_data(conn, 1024)
			if done_reading != 'y':
				self.send_data(conn, "\n\n\033[1;31m  Press (y) when finished...\033[0m\n")
				return
			else:
				return

	def intrigueCards(self):
		pass
