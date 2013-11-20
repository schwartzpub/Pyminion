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
		return

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

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerTurnTreasure += 2
		send_data(self.playerConn, "The top 5 cards of your deck are: ",)
		for i in range(5):
			send_data(self.player.playerConn, self.player.playerDeck[i].cardPrint + " ",)
		send_data(self.player.playerConn, "\n")
		send_data(self.player.playerConn, "Would you like to (d)iscard them or (r)eturn them to the deck?\n")
		while True:
			choice = recv_data(self.player.playerConn, 1024)
			if choice.lower() not in ['d', 'r']: continue
			elif choice.lower() == 'd':
				i = 0
				while i < 4:
					self.player.playerDiscard.append(self.player.playerDeck[0])
					del self.player.playerDeck[0]
					i += 1
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " has discarded the top 5 cards of his deck.\n")
				break
			else:
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " has done nothing.\n")
				break
		return

class OutpostCard(KingdomCard):
	cardEval = "OutpostCard"
	cardName = "Outpost"
	cardPrint = "\033[1;33mOutpost\033[0m"
	description = "You only draw 3 cards (instead of 5) in this turn's Clean-up phase. Take an extra turn after this one. This can't cause you to take more than two consecutive turns."
	action = True
	duration = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
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

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.drawOneCard()
		self.player.playerTurnActions += 1
		send_data(self.player.playerConn, "The bottom card of your deck is: " + self.player.playerDeck[-1].cardPrint + ". Put it on top of your deck (y/n)?\n")
		while True:
			choice = recv_data(self.player.playerConn, 1024)
			if choice.lower() not in ['y', 'n']: continue
			elif choice.lower() == 'y':
				self.player.playerDeck.insert(self.player.playerDeck[-1])
				del self.player.playerDeck[-1]
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " places the bottom card of his deck on top of his deck.\n")
				break
			else:
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " does nothing.\n")
				break
		return

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

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		send_data(self.player.playerConn, "Choose one: (A)ttack players, or (T)ake coins.\n")
		while True:
			choice = recv_data(self.player.playerConn, 1024)
			if choice.lower() not in ['a', 't']: continue
			elif choice.lower() == 'a':
				self.trashed = False
				self.trash = []
				for each in self.roster:
					each.playerDiscardToDeck()
					self.trash.append(each.player.playerDeck[0])
					del each.player.playerDeck[0]
					each.playerDiscardToDeck()
					self.trash.append(each.player.playerDeck[0])
					del each.player.playerDeck[0]
					if any(i.treasure for i in self.trash):
						self.trashed = True
						send_data(self.player.playerConn, "Choose one to trash: [1]" + self.trash[0].cardPrint + " [2]" + self.trash[1].cardPrint + "\n")
						for player in self.roster:
							send_data(player.playerConn, each.playerName + " reveals: [1]" + self.trash[0].cardPrint + " [2]" + self.trash[1].cardPrint + "\n")
						while True:
							choice = recv_data(self.player.playerConn, 1024)
							if choice not in ['1', '2']: continue
							elif choice == '1' and self.trash[0].treasure:
								for player in self.roster:
									send_data(player.playerConn, self.player.playerName + " trashes " + self.trash[0].cardPrint + "\n")
								del self.trash[0]
								each.playerDiscard.append(self.trash[0])
								del self.trash[0]
								break
							elif choice == '2' and self.trash[1].treasure:
								for player in self.roster:
									send_data(player.playerConn, self.player.playerName + " trashes " + self.trash[1].cardPrint + "\n")
								del self.trash[1]
								each.playerDiscard.append(self.trash[0])
								del self.trash[0]
								break
					else:
						for player in self.roster:
							send_data(player.playerConn, each.playerName + " reveals: [1]" + self.trash[0].cardPrint + " [2]" + self.trash[1].cardPrint + "\n")
						each.playerDiscard.append(self.trash[0])
						each.playerDiscard.append(self.trash[1])
						del self.trash[0]
						del self.trash[0]
				if self.trashed:
					self.player.pirateMat += 1
					break
			elif choice.lower == 't':
				self.player.playerTurnTreasure += self.player.pirateMat
				break
		return				

class SalvagerCard(KingdomCard):
	cardEval = "SalvagerCard"
	cardName = "Salvager"
	cardPrint = "\033[37mSalvager\033[0m"
	description = "+1 Buy.  Trash a card from your hand. +$ equal to its cost."
	cost = 4
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerTurnBuys += 1
		send_data(self.player.playerConn, "Please choose a card to trash, +$ equal to its cost.\n")
		while True:
			choice = recv_data(self.player.playerConn, 1024)
			try: choice = int(choice) - 1
			except: continue
			if choice not in range(len(self.player.playerHand)): continue
			else:
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " trashes a card.\n")
				del self.player.playerHand[choice]
				break
		return

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

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		for each in self.roster:
			each.playerDiscard.append(each.playerDeck[0])
			del each.playerDeck[0]
			for player in self.roster:
				send_data(player.playerConn, each.playerName + " discards a card, and gains a " + self.deck.curseCards[0] + "on top of his deck.\n")
			each.gainCard(0, 0, 'deck', 'curseCards')
		return

class SmugglersCard(KingdomCard):
	cardEval = "SmugglersCard"
	cardName = "Smugglers"
	cardPrint = "\033[37mSmugglers\033[0m"
	description = "Gain a copy of a card costing up to $6 that the player to your right gained on his last turn."
	cost = 3
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.previous = 0
		self.options = []
		i = 1
		for position, user in enumerate(self.roster):
			if user.playerName == self.player.playerName:
				if position == 0:
					if any(i.cost <= 6 for i in self.roster[-1].gained) and len(self.roster[-1].gained) > 0:
						for card in self.roster[-1].gained:
							if card.cost <= 6:
								self.options.append(card)
							else: pass
						send_data(self.player.playerConn, "Please choose a card to Gain: ",)
						for card in self.options:
							send_data(self.player.playerConn, "[" + str(i) + "]" + card.cardPrint + " ",)
							i += 1
						send_data(self.player.playerConn, "\n")
						while True:
							choice = recv_data(self.player.playerConn, 1024)
							try: choice = int(choice) - 1
							except: continue
							if choice not in range(len(self.options)): continue
							else:
								self.player.gainCard(0, 0, 'discard', card.cardName)
								for each in self.roster:
									send_data(each.playerConn, self.player.playerName + " gains a " + card.cardPrint + ".\n")
								break
					else: return
				else:
					if any(i.cost <= 6 for i in self.roster[self.previous].gained) and len(self.roster[self.previous].gained) > 0:
						self.previous = position - 1
						for card in self.roster[self.previous].gained:
							if card.cost <= 6:
								self.options.append(card)
							else: pass
						send_data(self.player.playerConn, "Please choose a card to Gain: ",)
						for card in self.options:
							send_data(self.player.playerConn, "[" + str(i) + "]" + card.cardPrint + " ",)
							i += 1
						send_data(self.player.playerConn, "\n")
						while True:
							choice = recv_data(self.player.playerConn, 1024)
							try: choice = int(choice) - 1
							except: continue
							if choice not in range(len(self.options)): continue
							else:
								self.player.gainCard(0, 0, 'discard', card.cardName)
								for each in self.roster:
									send_data(each.playerConn, self.player.playerName + " gains a " + card.cardPrint + ".\n")
								break
					else: return
		return

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

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerHasDuration = True
		if len(self.player.playerHand) == 0: return
		else:
			i = 0
			while i < len(self.player.playerHand):
				self.player.playerDiscard.append(self.player.playerHand[0])
				del self.player.playerHand[0]
				for each in self.roster:
					send_data(each.playerConn, self.player.playerName + " discards his hand.  Next turn +5 cards, +1 Buy, +1 Action.\n")
				break
			return

	def playDuration(self, player, roster, deck):
		self.player = player
		self.roster = roster
		for i in range(5):
			self.player.drawOneCard()
		self.player.playerTurnBuys += 1
		self.player.playerTurnActions += 1
		return

class TreasureMapCard(KingdomCard):
	cardEval = "TreasureMapCard"
	cardName = "Treasure Map"
	cardPrint = "\033[37mTreasure Map\033[0m"
	description = "Trash this and another copy of Treasure Map from your hand. If you do trash two Treasure Maps, gain 4 Gold cards, putting them on top of your deck."
	cost = 4
	action = True
	def __init__(self):
		pass


	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		if any(i.cardName == 'Treasure Map' for i in self.player.playerHand):
			del self.player.playerPlay[-1]
			for card in self.player.playerHand:
				if card.cardName != 'Treasure Map': pass
				else:
					self.player.playerHand.remove(card)
					for i in range(4):
						if len(self.deck.goldCards) > 0:
							self.player.playerDeck.insert(self.deck.goldCards[0])
						else: pass
			for each in self.roster:
				send_data(each.playerConn, self.player, playerName + " has trashed two Treasure Maps, and gained 4 " + self.deck.goldCards[0].cardPrint + "s on his deck.\n")
		else:
			del self.player.playerPlay[-1]
			for each in self.roster:
				send_data(each.playerConn, self.player.playerName + " has trashed a Treasure Map.\n")
		return

class TreasuryCard(KingdomCard):
	cardEval = "TreasuryCard"
	cardName = "Treasury"
	cardPrint = "\033[37mTreasury\033[0m"
	description = "+1 Card; +1 Action; +$1.  When you discard this from play, if you didn't buy a Victory card this turn, you may put this on top of your deck."
	cost = 5
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.drawOneCard()
		self.playerTurnActions += 1
		self.playerTurnTreasure += 1

	def playDiscard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		if not self.player.boughtVictory:
			self.player.playerDeck.insert(self.player.playerPlay[0])
			del self.player.playerPlay[0]
		for each in self.roster:
			send_data(each.playerConn, self.player.playerName + " places a Treasury on top of his deck.\n")

class WarehouseCard(KingdomCard):
	cardEval = "WarehouseCard"
	cardName = "Warehouse"
	cardPrint = "\033[37mWarehouse\033[0m"
	description = "+3 Cards; +1 Action; Discard 3 cards."
	cost = 3
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		for i in range(3):
			self.player.drawOneCard()
		self.player.playerTurnActions += 1
		for i in range(3):
			send_data(self.player.playerConn, "Choose one to discard:\n")
			self.player.printPlayerReveal()
			while True:
				choice = recv_data(self.player.playerConn, 1024)
				try: choice = int(choice) - 1
				except: continue
				if choice not in range(len(self.player.playerHand)): continue
				else:
					self.player.playerDiscard.append(self.player.playerHand[choice])
					del self.player.playerHand[choice]
		for each in self.roster:
			send_data(each.playerConn, self.player.playerName + " draws 3 cards, and discards 3 cards.\n")
		return

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

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.drawOneCard()
		self.player.drawOneCard()
		self.player.playerTurnBuys += 1
		for each in self.roster:
			send_data(each.playerConn, self.player.playerName + " draws two cards.\n")

	def playDuration(self. player, roster, deck):
		self.player = player
		self.roster = roster
				self.player.drawOneCard()
		self.player.drawOneCard()
		self.player.playerTurnBuys += 1
		for each in self.roster:
			send_data(each.playerConn, self.player.playerName + " draws two cards and gets +1 Buy from his Wharf.\n")
