#Dominion card classes
import os

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
	def __init__(self, cardtype):
		self.cardtype = cardtype

class GoldCard(TreasureCard):
	cardName = "Gold"
	cardColor = "\033[33m"
	quantity = 30
	value = 3
	cost = 6
	def __init__(self):
		pass

class SilverCard(TreasureCard):
	cardName = "Silver"
	cardColor = "\033[33m"
	quantity = 40
	value = 2
	cost = 3
	def __init__(self):
		pass

class CopperCard(TreasureCard):
	cardName = "Copper"
	cardColor = "\033[33m"
	quantity = 60
	value = 1
	cost = 0
	def __init__(self):
		pass

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
	def __init__(self, cardtype):
		self.cardtype = cardtype

class ProvinceCard(VictoryCard):
	cardName = "Province"
	cardColor = "\033[32m"
	value = 6
	cost = 8
	def __init__(self):
		pass

class DuchyCard(VictoryCard):
	cardName = "Duchy"
	cardColor = "\033[32m"
	value = 3
	cost = 5
	def __init__(self):
		pass

class EstateCard(VictoryCard):
	cardName = "Estate"
	cardColor = "\033[32m"
	value = 2
	cost = 2
	def __init__(self):
		pass

#Curse Cards
class CurseCard(object):
	cardName = "Curse"
	cardColor = "\033[35m"
	cardType = 'curse'
	value = -1
	cost = 0
	def __init__(self):
		pass

#Action Cards
class KingdomCard(object):
	cardType = 'action'
	quantity = 10
	cost = 0
	value = 0
	reaction = False
	action = True
	attack = False
	reaction = False
	victory = False
	duration = False
	treasure = False
	looter = False
	ruins = False
	def __init__(self, cardtype):
		self.cardtype = cardtype

class CellarCard(KingdomCard):
	cardEval = "CellarCard"
	cardName = "Cellar"
	cardColor = "\033[0m"
	description = "+1 Action.  Discard any number of cards.  +1 Card per card discarded."
	cost = 2
	action = True
	def __init__(self):
		pass
	
	def playCard(self, player, roster, deck):
		self.player = player
		self.player.playerTurnActions += 1
		while True:
			cards = len(self.player.playerHand)
			discard = raw_input("    How many cards would you like to discard? ")
			if int(discard) == 0:
				break
			elif int(discard) > len(self.player.playerHand):
				print "    That is not a valid number of cards!"
				continue
			else:
				for i in range(int(discard)):
					choice = int(raw_input("      Choose a card to discard: "))
					self.player.playerDiscard.append(self.player.playerHand[choice - 1])
					del self.player.playerHand[choice - 1]
				for i in range(int(discard)):
					self.player.drawOneCard()
				break		

class ChapelCard(KingdomCard):
	cardEval = "ChapelCard"
	cardName = "Chapel"
	cardColor = "\033[0m"
	description = "Trash up to 4 cards from your hand."
	cost = 2
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		if len(self.player.playerHand) > 4:
			trash = 4
		else:
			trash = len(self.player.playerHand)
		while True:
			for i in range(trash):
				choice = int(raw_input("    Choose a card to trash ([0] for none): "))
				if (choice - 1) not in range(len(self.player.playerHand)):
					print "    That is not a valid choice!"
					continue
				elif (choice - 1 ) == -1:
					break
				else:
					del self.player.playerHand[choice - 1] 				
					break
			break

class MoatCard(KingdomCard):
	cardEval = "MoatCard"
	cardName = "Moat"
	cardColor = "\033[36m"
	description = "+2 Cards.  When another player plays an Attack card, you may reveal this from your hand. if you do you are unaffected by that Attack."
	cost = 2
	action = True
	reaction = True
	def __init__(self):
		pass
	
	def playCard(self, player, roster, deck):
		self.player = player
		self.draw = 2
		for i in draw:
			if len(self.player.playerDeck) == 0:
				self.player.playerDiscardToDeck()
				self.player.playerHand.append(self.player.playerDeck[0])
				del self.player.playerDeck[0]
			else:
				self.player.playerHand.append(self.player.playerDeck[0])
				del self.player.playerDeck[0]		

class ChancellorCard(KingdomCard):
	cardEval = "ChancellorCard"
	cardName = "Chancellor"
	cardColor = "\033[0m"
	description = "+$2.  You may immediately put your deck into your discard pile."
	cost = 3
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.playerTurnTreasure += 2
		while True:
			discard = raw_input("Would you like to place your deck into your discard pile (y/n)? ")
			if discard.lower() not in ['y', 'n']:
				raw_input("That is not an available option, please choose (y)es or (n)o! ")
			elif discard.lower() == 'n':
				break
			elif discard.lower() == 'y':
				self.player.playerDeckToDiscard()
				break

class VillageCard(KingdomCard):
	cardEval = "VillageCard"
	cardName = "Village"
	cardColor = "\033[0m"
	description = "+1 Card. +2 Actions."
	cost = 3
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		if len(self.player.playerDeck) == 0:
			self.player.playerDiscardToDeck()
			self.player.playerHand.append(self.player.playerDeck[0])
			del self.player.playerDeck[0]
		else:
			self.player.playerHand.append(self.player.playerDeck[0])
			del self.player.playerDeck[0]
		self.player.playerTurnActions += 1

class WoodcutterCard(KingdomCard):
	cardEval = "WoodcutterCard"
	cardName = "Woodcutter"
	cardColor = "\033[0m"
	description = "+1 Buy. +$2."
	cost = 3	
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.playerTurnBuys += 1
		self.player.playerTurnTreasure += 2

class WorkshopCard(KingdomCard):
	cardEval = "WorkshopCard"
	cardName = "Workshop"
	cardColor = "\033[0m"
	description = "Gain a card costing up to $4."
	cost = 3
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.player.gainCard(4, 1)		

class BureaucratCard(KingdomCard):
	cardEval = "BureaucratCard"
	cardName = "Bureaucrat"
	cardColor = "\033[1;31m"
	description = "Gain a silver card; put it on top of your deck. Each other player reveals a Victory card from his hand and puts it on his deck (or reveals a hand with no Victory cards)."
	cost = 4
	action = True
	attack = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.roster = roster
		self.player = player
		self.deck = deck
		self.reveal = []
		if len(self.deck.silverCards) == 0:
			pass
		else:
			self.player.playerDeck.insert(0, self.deck.silverCards[0])
			del self.deck.silverCards[0]
		for each in self.roster:
			while True:
				if each != self.player:
					raw_input("    " + each.playerName + "`s reaction... Press any key when ready.")
					os.system('clear')
					if any(i.cardType == 'victory' for i in each.playerHand):
						while True:
							print " ",
							each.printPlayerReveal()
							choice = raw_input("\n Which card would you like to reveal? ")
							if each.playerHand[int(choice) - 1].cardType != 'victory':
								print "\n Invalid choice, please choose a Victory card."
								continue
							else:
								self.reveal.append("\n " + each.playerName + " reveals " + each.playerHand[(int(choice) - 1)].cardName + ".")
								break
					else:
						self.reveal.append("\n" + each.playerName + " reveals " + ' '.join(i.cardName for i in each.playerHand) + ".")
					break
				else:
					break
		raw_input(" Press any key to return to " + self.player.playerName + "`s hand...")
		os.system('clear')
		print "\n " + ' '.join(self.reveal)
		raw_input(" Press any key when done viewing reveal. ")

class FeastCard(KingdomCard):
	cardEval = "FeastCard"
	cardName = "Feast"
	cardColor = "\033[0m"
	description = "Trash this card. Gain a card costing up to $5."
	cost = 4
	action = True
	def __init__(self):
		pass

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
		self.player.gainCard(5, 1)

class GardensCard(KingdomCard):
	cardEval = "GardensCard"
	cardName = "Gardens"
	cardColor = "\033[32m"
	description = "Worth 1 Victory for every 10 cards in your deck (rounded down)."
	cost = 4
	value = 1
	action = False
	victory = True
	def __init__(self):
		pass

class MilitiaCard(KingdomCard):
	cardEval = "MilitiaCard"
	cardName = "Militia"
	cardColor = "\033[1;31m"
	description = "+$2.  Each other player discards down to 3 cards in his hand."
	cost = 4
	action = True
	attack = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerTurnTreasure += 2
		while True:
			for each in self.roster:
				if each != self.player:
					raw_input(each.playerName + "`s reaction... Press any key when ready. ")
					os.system('clear')
					print each.playerName + ": you must discard down to three cards in hand."
					each.printPlayerReveal()
					while len(each.playerHand) > 3:
						choice = raw_input("   Please choose a card to discard: ")
						if (int(choice) - 1) not in range(len(each.playerHand)):
							raw_input("   Please choose an appropriate card! ")
						else:
							each.playerDiscard.append(each.playerHand[int(choice) - 1])
							del each.playerHand[int(choice) - 1]
							each.printPlayerReveal()
			break
						
class MoneylenderCard(KingdomCard):
	cardEval = "MoneylenderCard"
	cardName = "Moneylender"
	cardColor = "\033[0m"
	description = "Trash a Copper from your hand. If you do, +$3."
	cost = 4
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		if any(i.cardName == 'copper' for i in self.player.playerHand):
			while True:
				choice = raw_input(" Would you like to trash a copper (y/n)? ")
				if choice.lower() == 'y':
					while True:
						for card in self.player.playerHand:
							if card.cardName == 'copper':
								del self.player.playerHand[card]
								self.player.playerTurnTreasure += 3
								break
				else:
					break
		else:
			return				
				
class RemodelCard(KingdomCard):
	cardEval = "RemodelCard"
	cardName = "Remodel"
	cardColor = "\033[0m"
	description = "Trash a card from your hand. Gain a card costing up to $2 more than the trashed card."
	cost = 4
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		if len(self.player.playerHand) > 0:
			while True:
				choice = raw_input("\n Please choose a card to trash: ")
				if (int(choice) - 1) not in range(len(self.player.playerHand)):
					print "Please choose an appropriate card! "
				else:
					value = 2 + self.player.playerHand[int(choice) - 1].cost
					del self.player.playerHand[int(choice) - 1]
					card = raw_input("Please choose a card to gain: ")
					self.player.gainCard(value, 1)

class SmithyCard(KingdomCard):
	cardEval = "SmithyCard"
	cardName = "Smithy"
	cardColor = "\033[0m"
	description = "+3 Cards."
	cost = 4
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		for i in range(3):
			self.player.drawOneCard()
		
