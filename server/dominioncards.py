#Dominion card classes
import os
import time

#import dominionsock
from dominioncardsseaside import *

#Treasure Cards
class TreasureCard(object):
	actionCost = 0
	cardType = 'treasure'
	treasure = True
	victory = False
	action = False
	attack = False
	reaction = False
	ruins = False
	duration = False
	looter = False
	victoryPoints = 0
	def __init__(self, cardtype):
		self.cardtype = cardtype

class GoldCard(TreasureCard):
	cardName = "Gold"
	cardPrint = "\033[33mGold\033[0m"
	quantity = 30
	value = 3
	cost = 6
	def __init__(self, game):
		self.game = game
		self.embargoed = False
                self.embargo = 0

class SilverCard(TreasureCard):
	cardName = "Silver"
	cardPrint = "\033[33mSilver\033[0m"
	quantity = 40
	value = 2
	cost = 3
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

class CopperCard(TreasureCard):
	cardName = "Copper"
	cardPrint = "\033[33mCopper\033[0m"
	quantity = 60
	value = 1
	cost = 0
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

#Victory Cards
class VictoryCard(object):
	quantity = 12
	cardType = 'victory'
	victory = True
	action = False
	attack = False
	reaction = False
	ruins = False
	duration = False
	looter = False
	treasure = False
	victoryPonts = 0
	def __init__(self, cardtype):
		self.cardtype = cardtype

class ProvinceCard(VictoryCard):
	cardName = "Province"
	cardPrint = "\033[32mProvince\033[0m"
	victoryPoints = 6
	cost = 8
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

class DuchyCard(VictoryCard):
	cardName = "Duchy"
	cardPrint = "\033[32mDuchy\033[0m"
	victoryPoints = 3
	cost = 5
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

class EstateCard(VictoryCard):
	cardName = "Estate"
	cardPrint = "\033[32mEstate\033[0m"
	victoryPoints = 2
	cost = 2
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

#Curse Cards
class CurseCard(object):
	cardName = "Curse"
	cardPrint = "\033[35mCurse\033[0m"
	cardType = 'curse'
	value = -1
	cost = 0
	action = False
	treasure = False
	victory = True
	ruins = False
	duration = False
	looter = False
	bane = False
	reaction = False
	attack = False
	victoryPoints = -1
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

#Action Cards
class KingdomCard(object):
	cardType = 'action'
	quantity = 10
	cost = 0
	value = 0
	victoryPoints = 0
	reaction = False
	action = True
	attack = False
	reaction = False
	victory = False
	duration = False
	treasure = False
	looter = False
	ruins = False
	bain = False
	def __init__(self, cardtype):
		self.cardtype = cardtype

class CellarCard(KingdomCard):
	cardEval = "CellarCard"
	cardName = "Cellar"
	cardPrint = "\033[37mCellar\033[0m"
	description = "+1 Action.  Discard any number of cards.  +1 Card per card discarded."
	cost = 2
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

	def recv_data (self, client, length):
	        data = client.recv(length)
	        if not data: return data
	        return data

	def send_data (self, client, data):
	        message = str(data)
	        return client.send(message)


	def playCard(self, player, roster, deck):
		self.player = player
		self.player.playerTurnActions += 1
		while True:
			cards = len(self.player.playerHand)
			self.send_data(self.player.playerConn, "How many cards would you like to discard?\n")
			discard = self.recv_data(self.player.playerConn, 1024)
			try:
				discard = int(discard)
			except:
				continue
			if int(discard) == 0:
				break
			elif int(discard) > len(self.player.playerHand):
				self.send_data(self.player.playerConn, "That is not a valid number of cards!\n")
				continue
			else:
				for i in range(int(discard)):
					while True:
						self.send_data(self.player.playerConn, "Choose a card to discard.\n")
						self.player.printHandUpdate()
						choice = self.recv_data(self.player.playerConn, 1024)
						try:
							choice = int(choice)
						except:
							continue
						if (choice - 1) not in range(len(self.player.playerHand)):
							continue					
						self.player.playerDiscard.append(self.player.playerHand[choice - 1])
						del self.player.playerHand[choice - 1]
						break
				for i in range(int(discard)):
					self.player.checkPlayerDeck()
					self.player.drawOneCard()
				break		

class ChapelCard(KingdomCard):
	cardEval = "ChapelCard"
	cardName = "Chapel"
	cardPrint = "\033[37mChapel\033[0m"
	description = "Trash up to 4 cards from your hand."
	cost = 2
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		if len(self.player.playerHand) > 4:
			trash = 4
		else:
			trash = len(self.player.playerHand)
		while True:
			for i in range(trash):
				self.send_data(self.player.playerConn, "Choose a card to trash (0 for none):\n")
				self.player.printHandUpdate()
				choice = self.recv_data(self.player.playerConn, 1024)
				try:
					choice = int(choice)
				except:
					continue
				if choice == 0: break
				elif (choice - 1) not in range(len(self.player.playerHand)):
					self.send_data(self.player.playerConn, "That is not a valid choice!\n")
					continue
				elif (choice - 1 ) == -1:
					break
				else:
					del self.player.playerHand[choice - 1] 				
					for user in roster:
						self.send_data(user.playerConn, self.player.playerName + " has trashed a card.\n")
					continue
			break

class MoatCard(KingdomCard):
	cardEval = "MoatCard"
	cardName = "Moat"
	cardPrint = "\033[36mMoat\033[0m"
	description = "+2 Cards.  When another player plays an Attack card, you may reveal this from your hand. if you do you are unaffected by that Attack."
	cost = 2
	action = True
	reaction = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0
	
        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.draw = 2
		for i in range(self.draw):
			if len(self.player.playerDeck) == 0:
				self.player.playerDiscardToDeck()
				self.player.playerHand.append(self.player.playerDeck[0])
				del self.player.playerDeck[0]
			else:
				self.player.playerHand.append(self.player.playerDeck[0])
				del self.player.playerDeck[0]		
		return

	def reactCard(self, reactor, roster, type):
		self.type = type
		self.reactor = reactor
		self.roster = roster
		if self.type == 'attack':
			while True:
				self.send_data(self.reactor.playerConn, "Would you like to reveal your Moat? (y)es or (no)\n")
				choice = self.recv_data(self.reactor.playerConn, 1024)
				if choice.lower() not in ['y', 'n']:
					continue
				elif choice.lower() == 'y':
					for each in self.roster:
						self.send_data(each.playerConn, self.reactor.playerName + " reveals a Moat!\n")
					self.reactor.reactionImmunity = True
					break
				elif choice.lower() == 'n':
					break
		else:
			return
		return

class ChancellorCard(KingdomCard):
	cardEval = "ChancellorCard"
	cardName = "Chancellor"
	cardPrint = "\033[37mChancellor\033[0m"
	description = "+$2.  You may immediately put your deck into your discard pile."
	cost = 3
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.playerTurnTreasure += 2
		while True:
			self.send_data(self.player.playerConn, "Would you like to place your deck into your discard pile? (y)es or (n)o\n")
			discard = self.recv_data(self.player.playerConn, 1024)
			if discard.lower() not in ['y', 'n']:
				self.send_data(self.player.playerConn, "That is not an available option, please choose (y)es or (n)o!\n")
				continue
			elif discard.lower() == 'n':
				break
			elif discard.lower() == 'y':
				self.player.playerDeckToDiscard()
				break

class VillageCard(KingdomCard):
	cardEval = "VillageCard"
	cardName = "Village"
	cardPrint = "\033[37mVillage\033[0m"
	description = "+1 Card. +2 Actions."
	cost = 3
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		if len(self.player.playerDeck) == 0:
			self.player.playerDiscardToDeck()
			self.player.playerHand.append(self.player.playerDeck[0])
			del self.player.playerDeck[0]
		else:
			self.player.playerHand.append(self.player.playerDeck[0])
			del self.player.playerDeck[0]
		self.player.playerTurnActions += 2
		return

class WoodcutterCard(KingdomCard):
	cardEval = "WoodcutterCard"
	cardName = "Woodcutter"
	cardPrint = "\033[37mWoodcutter\033[0m"
	description = "+1 Buy. +$2."
	cost = 3	
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.playerTurnBuys += 1
		self.player.playerTurnTreasure += 2
		return

class WorkshopCard(KingdomCard):
	cardEval = "WorkshopCard"
	cardName = "Workshop"
	cardPrint = "\033[37mWorkshop\033[0m"
	description = "Gain a card costing up to $4."
	cost = 3
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.player.gainCard(4, 1, 'discard', 'any')		
		return

class BureaucratCard(KingdomCard):
	cardEval = "BureaucratCard"
	cardName = "Bureaucrat"
	cardPrint = "\033[1;31mBureaucrat\033[0m"
	description = "Gain a silver card; put it on top of your deck. Each other player reveals a Victory card from his hand and puts it on his deck (or reveals a hand with no Victory cards)."
	cost = 4
	action = True
	attack = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.roster = roster
		self.player = player
		self.deck = deck
		self.reveal = []
		self.player.checkReactions('attack')
		if len(self.deck.silverCards) == 0:
			pass
		else:
			self.player.playerDeck.insert(0, self.deck.silverCards[0])
			del self.deck.silverCards[0]
		for each in self.roster:
			if each != self.player and each.reactionImmunity == False and each.durationImmunity == False:
				if any(i.cardType == 'victory' for i in each.playerHand):
					while True:
						each.printPlayerReveal()
						self.send_data(each.playerConn, "Which card would you like to reveal?\n")
						choice = self.recv_data(each.playerConn, 1024)
						try:
							choice = int(choice)
						except:
							continue
						if each.playerHand[int(choice) - 1].cardType != 'victory':
							self_self.send_data(each.playerConn, "Invalid choice, please choose a Victory card.\n")
							continue
						else:
							for player in self.roster:
								self.send_data(player.playerConn, each.playerName + " reveals " + each.playerHand[(int(choice) - 1)].cardPrint + ".\n")
							each.playerDeck.insert(0, each.playerHand[(int(choice) - 1)])
							del each.playerHand[(int(choice) - 1)]
							break
				else:
					for player in self.roster:
						self.send_data(player.playerConn, each.playerName + " reveals " + ' '.join(i.cardPrint for i in each.playerHand) + ".\n")
					break
			else:
				pass
		time.sleep(3)
		for each in self.roster:
			each.reactionImmunity = False
		return

class FeastCard(KingdomCard):
	cardEval = "FeastCard"
	cardName = "Feast"
	cardPrint = "\033[37mFeast\033[0m"
	description = "Trash this card. Gain a card costing up to $5."
	cost = 4
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		while True:
			for card in self.player.playerHand:
				if card.cardName == 'Feast':
					self.player.playerHand.remove(card)
					break
				else:
					continue
			break
		self.player.gainCard(5, 1, 'discard', 'any')
		return

class GardensCard(KingdomCard):
	cardEval = "GardensCard"
	cardName = "Gardens"
	cardPrint = "\033[32mGardens\033[0m"
	description = "Worth 1 Victory for every 10 cards in your deck (rounded down)."
	cost = 4
	victoryPoints = 1
	action = False
	victory = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

class MilitiaCard(KingdomCard):
	cardEval = "MilitiaCard"
	cardName = "Militia"
	cardPrint = "\033[1;31mMilitia\033[0m"
	description = "+$2.  Each other player discards down to 3 cards in his hand."
	cost = 4
	action = True
	attack = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerTurnTreasure += 2
		self.player.checkReactions('attack')
		while True:
			for each in self.roster:
				if each != self.player and each.reactionImmunity == False and each.durationImmunity == False:
					self.send_data(each.playerConn, "You must discard down to three cards in hand.\n")
					each.printPlayerReveal()
					while len(each.playerHand) > 3:
						self.send_data(each.playerConn, "Please choose a card to discard:\n")
						choice = self.recv_data(each.playerConn, 1024)
						try:
							choice = int(choice)
						except:
							continue
						if (int(choice) - 1) not in range(len(each.playerHand)):
							self.send_data(each.playerConn, "Please choose an appropriate card!\n")
						else:
							each.playerDiscard.append(each.playerHand[int(choice) - 1])
							del each.playerHand[int(choice) - 1]
							each.printPlayerReveal()
			break
		for each in self.roster:
			each.reactionImmunity = False
		return
						
class MoneylenderCard(KingdomCard):
	cardEval = "MoneylenderCard"
	cardName = "Moneylender"
	cardPrint = "\033[37mMoneylender\033[0m"
	description = "Trash a Copper from your hand. If you do, +$3."
	cost = 4
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		if any(i.cardName == 'Copper' for i in self.player.playerHand):
			while True:
				self.send_data(self.player.playerConn, "Would you like to trash a copper? (y)es or (n)o\n")
				choice = self.recv_data(self.player.playerConn, 1024)
				if choice.lower() not in ['y', 'n']:
					continue
				elif choice.lower() == 'y':
					for card in self.player.playerHand:
						if card.cardName == 'Copper':
							self.player.playerHand.remove(card)
							for user in roster:
								self.send_data(user.playerConn, self.player.playerName + " has trashed a Copper.\n")
							self.player.playerTurnTreasure += 3
							return
						else:
							pass
				elif choice.lower() == 'n':
					return
		else:
			return				

		return
				
class RemodelCard(KingdomCard):
	cardEval = "RemodelCard"
	cardName = "Remodel"
	cardPrint = "\033[37mRemodel\033[0m"
	description = "Trash a card from your hand. Gain a card costing up to $2 more than the trashed card."
	cost = 4
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		if len(self.player.playerHand) > 0:
			while True:
				self.send_data(self.player.playerConn, "Please choose a card to trash:\n")
				self.player.printHandUpdate()
				choice = self.recv_data(self.player.playerConn, 1024)
				try:
					choice = int(choice)
				except:
					continue
				if (int(choice) - 1) not in range(len(self.player.playerHand)):
					self.send_data(self.player.playerConn, "Please choose an appropriate card!\n")
					continue
				else:
					value = 2 + self.player.playerHand[int(choice) - 1].cost
					for user in roster:
						self.send_data(user.playerConn, self.player.playerName + " has trashed a card.\n")
					del self.player.playerHand[int(choice) - 1]
					self.player.gainCard(value, 1, 'discard', 'any')
					break
		return

class SmithyCard(KingdomCard):
	cardEval = "SmithyCard"
	cardName = "Smithy"
	cardPrint = "\033[37mSmithy\033[0m"
	description = "+3 Cards."
	cost = 4
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		for i in range(3):
			self.player.drawOneCard()
		return
		
class SpyCard(KingdomCard):
	cardEval = "SpyCard"
	cardName = "Spy"
	cardPrint = "\033[1;31mSpy\033[0m"
	description = "+1 Card; +1 Action.  Each player (including you) reveals the top card of his deck and either discards it or puts it back, your choice."
	cost = 4
	action = True
	attack = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.drawOneCard()
		self.player.playerTurnActions += 1
		self.player.checkReactions('attack')
		for each in self.roster:
			if each.reactionImmunity == False and each.durationImmunity == False:
				each.checkPlayerDeck()
				for player in self.roster:
					self.send_data(player.playerConn, each.playerName + " reveals: " + each.playerDeck[0].cardPrint + "...\n")
				while True:
					self.send_data(self.player.playerConn, "Would you like this player to (k)eep or (d)iscard this card?\n")
					choice = self.recv_data(self.player.playerConn, 1024)
					if choice.lower() not in ['d', 'k']:
						continue
					elif choice.lower() == 'd':
						each.playerDiscard.append(each.playerDeck[0])
						for player in self.roster:
							self.send_data(player.playerConn, each.playerName + " discards: " +  each.playerDeck[0].cardPrint + ".\n")
						del each.playerDeck[0]
						break
					elif choice.lower() == 'k':
						for player in self.roster:
							self.send_data(player.playerConn, each.playerName + " keeps: " +  each.playerDeck[0].cardPrint + ".\n")
						break
		for each in self.roster:
			each.reactionImmunity = False
		time.sleep(3)
		return

class ThiefCard(KingdomCard):
	cardEval = "ThiefCard"
	cardName = "Thief"
	cardPrint = "\033[1;31mThief\033[0m"
	description = "Each other player reveals the top 2 cards of his deck. if they revealed any Treasure cards, they trash one of them that you choose. You may gain any or all of these trashed cards. They discard the other revealed cards."
	cost = 4
	action = True
	attack = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		self.trash = []
		self.player.checkReactions('attack')
		for each in self.roster:
			if each != self.player and each.reactionImmunity == False and each.durationImmunity == False:
				for i in range(2):
					each.checkPlayerDeck()
					self.trash.append(each.playerDeck[-1])
					del each.playerDeck[-1]
				for player in self.roster:
					self.send_data(player.playerConn, each.playerName + " reveals: [1]" + self.trash[0].cardPrint + " and [2]" + self.trash[1].cardPrint + ".\n")
				if any(i.treasure == True for i in self.trash):
					while True:
						self.send_data(self.player.playerConn, "Which card would you like to trash?\n")
						choice = self.recv_data(self.player.playerConn, 1024)
						try:
							choice = int(choice)
						except:
							continue
						if choice not in [1, 2]:
							continue
						else:
							if choice == 1:
								if self.trash[0].treasure == True:
									each.playerDeck.append(self.trash[1])
									for player in self.roster:
										self.send_data(player.playerConn, each.playerName + " trashes: " + self.trash[0].cardPrint + "\n")
									del self.trash[1]
									break
								else:
									self.send_data(self.player.playerConn, "You may only trash a treasure card.\n")
									continue
							elif choice == 2:
								if self.trash[1].treasure == True:
									each.playerDeck.append(self.trash[0])
									for player in self.roster:
										self.send_data(player.playerConn, each.playerName + " trashes: " + self.trash[1].cardPrint + "\n")
									del self.trash[0]
									break
								else: self.send_data(self.player.playerConn, "You may only trash a treasure card.\n")
					while True:
						self.send_data(self.player.playerConn, "Would you like to (k)eep or (t)rash: " + self.trash[0].cardPrint + "?\n")	
						choice = self.recv_data(self.player.playerConn, 1024)
						if choice.lower() not in ['k', 't']:
							continue
						elif choice.lower() == 'k':
							self.player.playerDiscard.append(self.trash[0])
							for player in self.roster:
								self.send_data(player.playerConn, self.player.playerName + " keeps " + each.player.playerName + "`s " + self.trash[0].cardPrint + ".\n")
							del self.trash[0]
							break
						elif choice.lower() == 't':
							for player in self.roster:
								self.send_data(player.playerConn, self.player.playerName + " trashes " + each.player.playerName + "`s " + self.trash[0].cardPrint + ".\n")
							del self.trash[0]
							break
			else:
				pass
		for each in self.roster:
			each.reactionImmunity = False
		return

class ThroneRoomCard(KingdomCard):
	cardEval = "ThroneRoomCard"
	cardName = "Throne Room"
	cardPrint = "\033[37mThrone Room\033[0m"
	description = "Choose an Action card in your hand. Play it twice."
	cost = 4
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0
	
        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		if not any(i.action == True for i in self.player.playerHand):
			return
		else:
			self.player.printHandUpdate()
			while True:
				self.send_data(self.player.playerConn, self.description + "\n")
				i = self.recv_data(self.player.playerConn, 1024)
				try:
					i = int(i) - 1
				except:
					continue
				if i not in range(len(self.player.playerHand)):
					continue
				elif self.player.playerHand[i].action != True:
					continue
				else:
					self.player.playerPlay.append(self.player.playerHand[i])
					playTwice = self.player.playerPlay[-1]
					del self.player.playerHand[i]
					playTwice.playCard(self.player, self.roster, self.deck)
					playTwice.playCard(self.player, self.roster, self.deck)
					break
		return

class CouncilRoomCard(KingdomCard):
	cardEval = "CouncilRoomCard"
	cardName = "Council Room"
	cardPrint = "\033[37mCouncil Room\033[0m"
	description = "+4 Cards; +1 Buy.  Each other player draws a card."
	cost = 5
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		for i in range(4):
			self.player.drawOneCard()
		self.player.playerTurnBuys += 1
		for each in self.roster:
			if each != self.player:
				each.drawOneCard()
			else:
				pass
		return

class FestivalCard(KingdomCard):
	cardEval = "FestivalCard"
	cardName = "Festival"
	cardPrint = "\033[37mFestival\033[0m"
	description = "+2 Actions; +1 Buy; +$2"
	cost = 5
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.playerTurnActions += 2
		self.player.playerTurnBuys += 1
		self.player.playerTurnTreasure += 2
		return

class LaboratoryCard(KingdomCard):
	cardEval = "LaboratoryCard"
	cardName = "Laboratory"
	cardPrint = "\033[37mLaboratory\033[0m"
	description = "+2 Cards; +1 Action"
	cost = 5
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
	
        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		for i in range(2):
			self.player.drawOneCard()
		self.player.playerTurnActions += 1
		return

class LibraryCard(KingdomCard):
	cardEval = "LibraryCard"
	cardName = "Library"
	cardPrint = "\033[37mLibrary\033[0m"
	description = "Draw until you have 7 cards in hand. You may set aside any Action cards drawn this way, as you draw them; discard the set aside cards after you finish drawing."
	cost = 5
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.setAside = False
		self.setAsideNum = 0
		while len(self.player.playerHand) < 7:
			i = self.player.playerDeck[0]
			self.send_data(self.player.playerConn, "You have drawn: " + i.cardPrint + "\n")
			if i.action != True:
				self.player.playerHand.append(i)
				del i
			else:
				while True:
					self.send_data(self.player.playerConn, "Would you like to (k)eep or (s)et this card aside?\n")
					choice = self.recv_data(self.player.playerConn, 1024)
					if choice.lower() not in ['k', 's']:
						continue
					elif choice.lower() == 'k':
						self.player.playerHand.append(i)
						del i
						break
					elif choice.lower() == 's':
						self.setAside = True
						self.setAsideNum += 1
						self.player.playerSetAside.append(i)
						del i
						break
		for i in range(self.setAsideNum):
			self.player.playerDiscard.append(self.player.playerSetAside[-1])
			del self.player.playerSetAside[-1]
		return

class MarketCard(KingdomCard):
	cardEval = "MarketCard"
	cardName = "Market"
	cardPrint = "\033[37mMarket\033[0m"
	description = "+1 Card; +1 Action; +1 Buy, +$1"
	cost = 5
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.drawOneCard()
		self.player.playerTurnActions += 1
		self.player.playerTurnBuys += 1
		self.player.playerTurnTreasure += 1
		return

class MineCard(KingdomCard):
	cardEval = "MineCard"
	cardName = "Mine"
	cardPrint = "\033[37mMine\033[0m"
	description = "Trash a tresure card from your hand. gain a Treasure card costing up to $3 more; put it into your hand."
	cost = 5
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		while True:
			self.send_data(self.player.playerConn, "Trash a treasure card from your hand.\n")
			self.player.printHandUpdate()
			i = self.recv_data(self.player.playerConn, 1024)
			try:
				i = int(i) - 1
			except:
				continue
			if self.player.playerHand[i].treasure != True or i not in range(len(self.player.playerHand)):
				continue
			else:
				value = self.player.playerHand[i].cost + 3
				for user in roster:
					self.send_data(user.playerConn, self.player.playerName + " has trashed a card.\n")
				del self.player.playerHand[i]
				self.player.gainCard(value, 1, 'hand', 'treasure')
				break
		return

class WitchCard(KingdomCard):
	cardEval = "WitchCard"
	cardName = "Witch"
	cardPrint = "\033[1;31mWitch\033[0m"
	description = "+2 Cards.  Each other player gains a Curse card."
	cost = 5
	action = True
	attack = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
                self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		self.player.drawOneCard()
		self.player.drawOneCard()
		self.player.checkReactions('attack')
		for each in self.roster:
			if each != self.player and each.reactionImmunity == False and each.durationImmunity == False and len(self.deck.curseCards) > 0:
				each.playerDiscard.append(self.deck.curseCards[0])
				del self.deck.curseCards[0]
				for player in self.roster:
					self.send_data(player.playerConn, each.playerName + " has gained a " + self.deck.curseCards[0].cardPrint + ".\n")
			else:
				pass
		for each in self.roster:
			each.reactionImmunity = False
		return

class AdventurerCard(KingdomCard):
	cardEval = "AdventurerCard"
	cardName = "Adventurer"
	cardPrint = "\033[37mAdventurer\033[0m"
	description = "Reveal cards from your deck until you reveal 2 Treasure cards. Put those Treasure cards in your hand and discard the other revealed cards."
	cost = 6
	action = True
	def __init__(self, game):
		self.game = game
                self.embargoed = False
		self.embargo = 0

        def recv_data (self, client, length):
                data = client.recv(length)
                if not data: return data
                return data

        def send_data (self, client, data):
                message = str(data)
                return client.send(message)

	def playCard(self, player, roster, deck):
		self.player = player
		self.treasureCount = 0
		self.revealCount = 0
		self.roster = roster
		while self.treasureCount < 2:
			if len(self.player.playerDeck) > 0:
				for each in self.roster:
					self.send_data(each.playerConn, self.player.playerName + " reveals a: " + self.player.playerDeck[0].cardPrint + ".\n")
			if len(self.player.playerDeck) == 0:
				self.player.playerDiscardToDeck()
			if self.player.playerDeck[0].treasure != True:
				self.player.playerSetAside.append(self.player.playerDeck[0])
				del self.player.playerDeck[0]
				self.revealCount += 1
			else:
				self.player.playerSetAside.append(self.player.playerDeck[0])
				del self.player.playerDeck[0]
				self.revealCount += 1
				self.treasureCount += 1
		for i in range(self.revealCount):
			if self.player.playerSetAside[-1].treasure != True:
				self.player.playerDiscard.append(self.player.playerSetAside[-1])
				del self.player.playerSetAside[-1]
			else:
				self.player.playerHand.append(self.player.playerSetAside[-1])
				del self.player.playerSetAside[-1]
		return
