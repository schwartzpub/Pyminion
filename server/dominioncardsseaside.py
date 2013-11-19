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

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		send_data(self.player.playerConn, "Reveal a card from your hand.\n")
		self.player.printRevealHand()
		while True:
			choice = recv_data(self.player.playerConn, 1024)
			try:
				choice = int(choice) - 1
			except:
				continue
			if choice not in range(len(self.player.playerhand)): continue
			else:
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " reveals: " + self.player.playerHand[choice].cardPrint + ".\n")
				

class BazaarCard(KingdomCard):
	cardEval = "BazaarCard"
	cardName = "Bazaar"
	cardPrint = "\033[37mBazaar\033[0m"
	description = "+1 Card; +2 Actions; +$1"
	cost = 5
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.drawOneCard()
		self.player.playerTurnActions += 2
		self.player.playerTurnTreasure += 1

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

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.drawOneCard()
		self.player.playerTurnActions += 1
		self.player.playerHasDuration = True

	def playDuration(self, player, roster, deck):
		self.player = player
		self.player.drawOneCard()

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

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerTurnTreasure += 2
		for each in self.roster:
			if any(i.cardName == 'Copper' for i in each.playerhand):
				each.playerDiscard.append(each.playerHand[i])
				del each.playerHand[i]
				for player in self.roster:
					send_data(player.playerConn, each.playerName + " discards a Copper.\n")
			else:
				for player in self.roster:
					send_data(player.playerConn, each.playerName + " reveals " + ' '.join(i.cardPrint for i in each.playerHand) + ".\n")
		return

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

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		if any(i.cardName == 'Province' for i in self.player.playerhand):
			send_data(self.player.playerConn, "Would you like to reveal a Province (y/n)?\n")
			while True:
				choice = recv_data(self.player.playerConn, 1024)
				if choice.lower() not in ['y', 'n']:
					continue
				elif choice.lower() == 'y':
					for each in self.roster:
						send_data(each.playerConn, self.player.playerName + " reveals a Province.\n")
					if len(self.deck.goldCards) > 0:
						self.player.gainCard(0, 0, 'hand', goldCard)
						for each in self.roster:
							send_data(each.playerConn, self.player.playername + " gains a Gold.\n")	
					else: return
				elif choice.lower() == 'n':
					if len(self.deck.silverCards) > 0:
						self.player.gainCard(0, 0, 'hand', silverCard)
						for each in self.roster:
							send_data(each.playerConn, self.player.playername + " gains a Silver.\n")
					else: return

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

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.playerTurnActions += 2
		self.player.playerTurnTreasure += 1

	def playDuration(self, player, roster, deck):
		self.player = player
		self.player.playerTurnActions += 1
		self.player.playerTurnTreasure += 1

class GhostShipCard(KingdomCard):
	cardEval = "GhostChipCard"
	cardName = "Ghost Ship"
	cardPrint = "\033[1;31mGhost Ship\033[0m"
	description = "+2 Cards. Each other player with 4 or more cards in hand puts cards from his hand on top of his deck until he has 3 cards in his hand."
	cost = 5
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.drawOneCard()
		self.player.drawOneCard()
		for each in self.roster:
			if len(each.playerHand) >= 4 or each != self.player or each.reactionImmunity == False or each.durationImmunity == False:
				send_data(each.playerConn, "Please discard cards until you have 3 cards in your hand.")
				while len(each.playerHand) > 3:
					each.printPlayerReveal()
					choice = (each.playerConn, 1024)
					try:
						choice = int(choice) - 1
					except:
						continue
					if choice not in range(len(each.playerHand)): continue
					else:
						each.playerDiscard.append(each.playerHand[choice])
						del each.playerHand[choice]
						for player in self.roster:
							send_data(player.playerConn, each.playerName + " discards a card.\n")
		

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

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.drawOneCard()
		self.player.playerTurnActions += 1
		self.player.playerHasDuration = True
		send_data(self.player.playerConn, "Please choose a card to set aside:\n")
		while True:
			self.player.printPlayerReveal()
			choice = (self.player.playerConn, 1024)
			try:
				choice = int(choice) - 1
			except: continue
			if choice not in range(len(self.player.playerHand)): continue
			else:
				self.player.playerSetAside.append(self.player.playerHand[choice])
				del self.player.playerHand[choice]
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " has set aside a card.\n")
				break

	def playDuration(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerHand.append(self.player.playerSetAside[0])
		del self.player.playerSetAside[0]
		for each in self.roster:
			send_data(each.playerConn, self.player.playerName + " has picked up set aside card.\n")

class IslandCard(KingdomCard):
	cardEval = "IslandCard"
	cardName = "Island"
	cardPrint = "\033[32mI\033[37ms\033[32ml\033[37ma\033[32mn\033[37md"
	description = "Set aside this and another card from your hand. Return them to your deck at the end of the game."
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		send_data(self.player.playerConn, "Please choose a card to set aside.\n")
		while True:
			self.player.printPlayerReveal()
			choice = recv_data(self.player.playerConn, 1024)
			try:
				choice = int(choice) - 1
			except: continue
			if choice not in range(len(self.player.playerHand)): continue
			else:
				self.player.islandMat.append(self.player.playerHand[choice])
				del self.player.playerHand[choice]
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " has placed a card on his Island mat.\n")
				if any(i.cardName == 'Island' for i in self.player.playerHand):
					self.player.islandMat.append(i)
					self.player.playerHand.remove(i)
					break

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
	
	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerTurnActions += 1
		self.player.playerTurnTreasure += 1
		self.player.durationImmunity = True
		self.player.playerHasDuration = True

	def playDuration(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerTurnTreasure += 1
		self.player.durationImmunity = False

class LookoutCard(KingdomCard):
	cardEval = "LookoutCard"
	cardName = "Lookout"
	cardPrint = "\033[37mLookout\033[0m"
	description = "Look at the top 3 cards of your deck. Trash one of them. Discard one of them. Put the other one on top of your deck."
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.current = []
		i = 1
		while i <= 3:
			self.current.append(self.player.playerHand[0])
			del self.player.playerHand[0]
			i += 1
		send_data(self.player.playerConn, "Choose a card to trash:\n")
		while True:
			for each in self.current:
				send_data(self.player.playerConn, each.cardPrint + ,)
			send_data(self.player.playerConn, "\n")
			choice = recv_data(self.player.playerConn, 1024)
			try:
				choice = int(choice) - 1
			except: continue
			if choice not in range(len(self.current)): continue
			else:
				del self.current[choice]
				break
		send_data(self.player.playerConn, "Choose a card to discard:\n")
                while True:
                        for each in self.current:
                                send_data(self.player.playerConn, each.cardPrint + ,)
                        send_data(self.player.playerConn, "\n")
                        choice = recv_data(self.player.playerConn, 1024)
                        try:
                                choice = int(choice) - 1
                        except: continue
                        if choice not in range(len(self.current)): continue
                        else:
				self.player.playerDiscard.append(self.current[choice])
				del self.current[choice]
				break
		self.player.playerDeck.insert(self.current[0])

class MerchantShipCard(KingdomCard):
	cardEval = "MerchantShipCard"
	cardName = "Merchant Ship"
	cardPrint = "\033[1;33mMerchant Ship\033[0m"
	description = "Now and at the start of your next turn: +$2"
	action = True
	duration = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.playerTurnTreasure += 2
		self.player.playerHasDuration = True

	def playDuration(self, player, roster, deck):
		self.player.playerTurnTreasure += 2

class NativeVillageCard(KingdomCard):
	cardEval = "NativeVillageCard"
	cardName = "Native Village"
	cardPrint = "\033[37mNative Village\033[0m"
	description = "+2 Actions. Choose one: Set aside the top card of your deck face down on your native Village mat, or put all the cards from your mat into your hand. You may look at the cards on your mat at any time, return them to your deck at the end of the game."
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerTurnActions += 2
		send_data(self.player.playerConn, "Choose one: [1]Set aside the top card of your deck face down on Native Village mat. [2]Place contents of Native Village mat into hand.\n")
		while True:
			choice = recv_data(self.player.playerConn, 1024)
			if choice not in ['1', '2']: continue
			elif choice == '1':
				self.player.playerDiscardToDeck()
				send_data(self.player.playerConn, "Placing " + self.player.playerDeck[0].cardPrint + " on your Native Village mat.\n")
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " places a card on the Native Village mat.\n")
				self.player.nativeVillageMat.append(self.player.playerDeck[0])
				del self.player.playerDeck[0]
				break
			elif choice == '2':
				while len(self.player.nativeVillageMat) > 0:
					self.player.playerHand.append(self.player.nativeVillageMat[0])
					del self.player.nativeVillageMat[0]
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " has placed the contents of his Native Village Mat into his hand.\n")
				break

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
