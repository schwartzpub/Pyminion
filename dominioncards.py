a#Dominion card classes

#Treasure Cards
class TreasureCard(object):
	sctionCost = 0
	cardType = 'treasure'
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

#Action Cards
class ActionCard(object):
	cardType = 'action'
	actionCost = 1
	quantity = 10
	cost = 0
	cardsDiscarded = False
	cardsTrashed = False
	cardsDrawn = False
	cardsGained = False
	cardsGainedCost = False
	actionsGained = False
	treasureGained = False
	buysGained = False
	curseGained = False
	cardsDiscarded_enemy = False
	cardsRevealed = False
	cardsRevealed_enemy = False
	cardsRevealed_type = False
	attackCard = False
	def __init__(self, cardtype):
		self.cardtype = cardtype

class CellarCard(ActionCard):
	cardEval = "CellarCard"
	cardName = "Cellar"
	cardColor = "\033[0m"
	description = "+1 Action.  Discard any number of cards.  +1 Card per card discarded."
	cost = 2
	actionsGained = True
	cardsDiscarded = True
	def __init__(self):
		pass
	
	def displayCard():
		pass

class ChapelCard(ActionCard):
	cardEval = "ChapelCard"
	cardName = "Chapel"
	cardColor = "\033[0m"
	description = "Trash up to 4 cards from your hand."
	cost = 2
	cardsTrashed = True
	def __init__(self):
		pass

class MoatCard(ActionCard):
	cardEval = "MoatCard"
	cardName = "Moat"
	cardColor = "\033[36m"
	description = "+2 Cards.  When another player plays an Attack card, you may reveal this from your hand. if you do you are unaffected by that Attack."
	cost = 2
	cardsDrawn = True
	def __init__(self):
		pass

class ChancellorCard(ActionCard):
	cardEval = "ChancellorCard"
	cardName = "Chancellor"
	cardColor = "\033[0m"
	description = "+$2.  You may immediately put your deck into your discard pile."
	cost = 3
	cardsDiscarded = True
	def __init__(self):
		pass

class VillageCard(ActionCard):
	cardEval = "VillageCard"
	cardName = "Village"
	cardColor = "\033[0m"
	description = "+1 Card. +2 Actions."
	cost = 3
	cardsDrawn = True
	actionsGained = True
	def __init__(self):
		pass

class WoodcutterCard(ActionCard):
	cardEval = "WoodcutterCard"
	cardName = "Woodcutter"
	cardColor = "\033[0m"
	description = "+1 Buy. +$2."
	cost = 3	
	buysGained = True
	treasureGained = True
	def __init__(self):
		pass

class WorkshopCard(ActionCard):
	cardEval = "WorkshopCard"
	cardName = "Workshop"
	cardColor = "\033[0m"
	description = "Gain a card costing up to $4."
	cost = 3
	cardsGained = True
	cardsGainedCost = True
	def __init__(self):
		pass

class BureaucratCard(ActionCard):
	cardEval = "BureaucratCard"
	cardName = "Bureaucrat"
	cardColor = "\033[1;31m"
	description = "Gain a silver card; put it on top of your deck. Each other player reveals a Victory card from his hand and puts it on his deck (or reveals a hand with no Victory cards)."
	cost = 4
	cardsGained = True
	cardsRevealed_enemy = True
	def __init__(self):
		pass

class FeastCard(ActionCard):
	cardEval = "FeastCard"
	cardName = "Feast"
	cardColor = "\033[0m"
	description = "Trash this card. Gain a card costing up to $5."
	cost = 4
	cardsGained = True
	cardsGainedCost = True
	cardsTrashed = True
	def __init__(self):
		pass

class GardensCard(ActionCard):
	cardEval = "GardensCard"
	cardName = "Gardens"
	cardColor = "\033[32m"
	description = "Worth 1 Victory for every 10 cards in your deck (rounded down)."
	cost = 4
	def __init__(self):
		pass

class MilitiaCard(ActionCard):
	cardEval = "MilitiaCard"
	cardName = "Militia"
	cardColor = "\033[1;31m"
	description = "+$2.  Each other player discards down to 3 cards in his hand."
	cost = 4
	cardsDiscarded_enemy = True
	def __init__(self):
		pass

class MoneylenderCard(ActionCard):
	cardEval = "MoneylenderCard"
	cardName = "Moneylender"
	cardColor = "\033[0m"
	description = "Trash a Copper from your hand. If you do, +$3."
	cost = 4
	cardsTrashed = True
	def __init__(self):
		pass

class RemodelCard(ActionCard):
	cardEval = "RemodelCard"
	cardName = "Remodel"
	cardColor = "\033[0m"
	description = "Trash a card from your hand. Gain a card costing up to $2 more than the trashed card."
	cost = 4
	cardsTrashed = True
	cardsGained = True
	def __init__(self):
		pass

