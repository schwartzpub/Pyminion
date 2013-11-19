import dominionsock, sys, os, time

class AmbassadorCard(KingdomCard):
        cardEval = "AmbassadorCard"
        cardName = "Ambassador"
        cardPrint = "\033[1;31mAmbassador\033[0m"
        description = "Reveal a card from your hand. Return up to 2 copies of it from your hand to the Supply. Then each other player gains a copy of it."
        cost = 3
        action = True
        attack = True
        def __init__(self):
                pass

class BazaarCard(KingdomCard):
	cardEval = "BazaarCard"
	cardName = "Bazaar"
	cardPrint = "\033[37mBazaar\033[0m"
	description = "+1 Card; +2 Actions; +$1"
	cost = 5
	action = True
	def __init__(self):
		pass

class CaravanCard(KingdomCard):
	cardEval = "CaravanCard"
	cardName = "Caravan"
	cardPrint = "\033[37mCaravan\033[0m"
	description = "+1 Card; +1 Action. At the start of your next turn, +1 Card"
	cost = 4
	action = True
	duration = True
	def __init__(self):
		pass

class CutpurseCard(KingdomCard):
	cardEval = "CutpurseCard"
	cardName = "Cutpurse"
	cardPrint = "\033[1;31mCutpurse\033[0m"
	description = "+$2. Each other player discards a Copper card (or reveals a hand with no Coppers)"
	cost = 4
	action = True
	attack = True
	def __init__(self):
		pass

class EmbargoCard(KingdomCard):
	cardEval = "EmbargoCard"
	cardName = "Embargo"
	cardPrint = "\033[37mEmbargo\033[0m"
	description = "+$2. Trash this card. Put an Embargo token on top of a Supply pile.  When a player buys a card, he gains a Curse card per Embargo token on that pile."
	cost = 2
	action = True
	def __init__(self):
		pass

class ExplorerCard(KingdomCard):
	cardEval = "ExplorerCard"
	cardName = "Explorer"
	cardPrint = "\033[37mExplorer\033[0m"
	description = "You may reveal a Province card from your hand.  If you do, gain a Gold card, putting it into your hand.  Otherwise, gain a Sivler card, putting it into your hand."
	cost = 5
	action = True
	def __init__(self):
		pass

class FishingVillageCard(KingdomCard):
	cardEval = "FishingVillageCard"
	cardName = "Fishing Village"
	cardPrint = "\033[1;33mFishing Village\033[0m"
	description = "+2 Actions; +$1.  At the start of your next turn: +1 Action; +$1"
	cost = 3
	action = True
	duration = True
	def __init__(self):
		pass

class GhostShipCard(KingdomCard):
	cardEval = "GhostChipCard"
	cardName = "Ghost Ship"
	cardPrint = "\033[1;31mGhost Ship\033[0m"
	description = "+2 Cards. Each other player with 4 or more cards in hand puts cards from his hand on top of his deck until he has 3 cards in his hand."
	cost = 5
	action = True
	def __init__(self):
		pass

class HavenCard(KingdomCard):
	cardEval = "HavenCard"
	cardName = "Haven"
	cardPrint = "\033[1;33mHaven\033[0m"
	description = "+1 Card, +1 Action. Set aside a card from your hand face down. At the start of your next turn, put it into your hand."
	cost = 2
	action = True
	duration = True
	def __init__(self):
		pass

class IslandCard(KingdomCard):
	cardEval = "IslandCard"
	cardName = "Island"
	cardPrint = "\033[32mI\033[37ms\033[32ml\033[37ma\033[32mn\033[37md"
	description = "Set aside this and another card from your hand. Return them to your deck at the end of the game."
	action = True
	def __init__(self):
		pass

class LighthouseCard(KingdomCard):
	cardEval = "LighthouseCard"
	cardName = "Lighthouse"
	cardPrint = "\033[1;33mLighthouse\033[0m"
	description = "+1 Action. Now and at the start of your next turn, +$1.  While this is in play, when another player plays an Attack card, it doesn't affect you."
	action = True
	duration = True
	reaction = True
	def __init__(self):
		pass

class LookoutCard(KingdomCard):
	cardEval = "LookoutCard"
	cardName = "Lookout"
	cardPrint = "\033[37mLookout\033[0m"
	description = "Look at the top 3 cards of your deck. Trash one of them. Discard one of them. Put the other one on top of your deck."
	action = True
	def __init__(self):
		pass

class MerchantShipCard(KingdomCard):
	cardEval = "MerchantShipCard"
	cardName = "Merchant Ship"
	cardPrint = "\033[1;33mMerchant Ship\033[0m"
	description = "Now and at the start of your next turn: +$2"
	action = True
	duration = True
	def __init__(self):
		pass

class NativeVillageCard(KingdomCard):
	cardEval = "NativeVillageCard"
	cardName = "Native Village"
	cardPrint = "\033[37mNative Village\033[0m"
	description = "+2 Actions. Choose one: Set aside the top card of your deck face down on your native Village mat, or put all the cards from your mat into your hand. You may look at the cards on your mat at any time, return them to your deck at the end of the game."
	action = True
	def __init__(self):
		pass

class NavigatorCard(KingdomCard):
	cardEval = "NavigatorCard"
	cardName = "Navigator"
	cardPrint = "\033[37mNavigator\033[0m"
	description = "+$2. Look at the top 5 cards of your deck.  Either discard all of them or put them back on top of your deck."
	action = True
	def __init__(self):
		pass

class OutpostCard(KingdomCard):
	cardEval = "OutpostCard"
	cardName = "Outpost"
	cardPrint = "\033[1;33mOutpost\033[0m"
	description = "You only draw 3 cards (instead of 5) in this turn's Clean-up phase. Take an extra turn after this one. This can't cause you to take more than two consecutive turns."
	action = True
	duration = True
	def __init__(self):
		pass

class PearlDiverCard(KingdomCard):
	cardEval = "PearlDiverCard"
	cardName = "Pearl Diver"
	cardPrint = "\033[37mPearl Diver\033[0m"
	description = "+1 Card; +1 Action. Look at the bottom card of your deck. You may put it on top."
	cost = 2
	action = True
	def __init__(self):
		pass

class PirateShipCard(KingdomCard):
	cardEval = "PirateShipCard"
	cardName = "Pirate Ship"
	cardPrint = "\033[1;31mPirate Ship\033[0m"
	description = "Choose one: Each other player reveals the top 2 cards of his deck, trashes a revealed Treasure that you choose, discards the rest, and if anyone trashed a Treasure you take a Coin token; or, +1$ per Coin token you've taken with Pirate Ships this game."
	cost = 4
	action = True
	attack = True
	def __init__(self):
		pass

class SalvagerCard(KingdomCard):
	cardEval = "SalvagerCard"
	cardName = "Salvager"
	cardPrint = "\033[37mSalvager\033[0m"
	description = "+1 Buy.  Trash a card from your hand. +$ equal to its cost."
	cost = 4
	action = True
	def __init__(self):
		pass

class SeaHagCard(KingdomCard):
	cardEval = "SeaHagCard"
	cardName = "Sea Hag"
	cardPrint = "\033[1;31mSea Hag\033[0m"
	description = "Each other player discards the top card of his deck, then gains a Curse card, putting it on top of his deck."
	cost = 4
	action = True
	attack = True
	def __init__(self):
		pass

class SmugglersCard(KingdomCard):
	cardEval = "SmugglersCard"
	cardName = "Smugglers"
	cardPrint = "\033[37mSmugglers\033[0m"
	description = "Gain a copy of a card costing up to $6 that the player to your right gained on his last turn."
	cost = 3
	action = True
	def __init__(self):
		pass

class TacticianCard(KingdomCard):
	cardEval = "TacticianCard"
	cardName = "Tactician"
	cardPrint = "\033[1;33mTactician\033[0m"
	description = "Discard your hand. If you discarded any cards this way, then at the start of your next turn, +5 Cards; +1 Buy; and +1 Action."
	cost = 5
	action = True
	duration = True
	def __init__(self):
		pass

class TreasureMapCard(KingdomCard):
	cardEval = "TreasureMapCard"
	cardName = "Treasure Map"
	cardPrint = "\033[37mTreasure Map\033[0m"
	description = "Trash this and another copy of Treasure Map from your hand. If you do trash two Treasure Maps, gain 4 Gold cards, putting them on top of your deck."
	cost = 4
	action = True
	def __init__(self):
		pass

class TreasuryCard(KingdomCard):
	cardEval = "TreasuryCard"
	cardName = "Treasury"
	cardPrint = "\033[37mTreasury\033[0m"
	description = "+1 Card; +1 Action; +$1.  When you discard this from play, if you didn't buy a Victory card this turn, you may put this on top of your deck."
	cost = 5
	action = True
	def __init__(self):
		pass

class WarehouseCard(KingdomCard):
	cardEval = "WarehouseCard"
	cardName = "Warehouse"
	cardPrint = "\033[37mWarehouse\033[0m"
	description = "+3 Cards; +1 Action; Discard 3 cards."
	cost = 3
	action = True
	def __init__(self):
		pass

class WharfCard(KingdomCard):
	cardEval = "WharfCard"
	cardName = "Wharf"
	cardPrint = "\033[1;33mWharf\033[0m"
	description = "Now and at the start of your next turn: +2 Cards; +1 Buy."
	cost = 5
	action = True
	duration = True
	def __init__(self):
		pass
