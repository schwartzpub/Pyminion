#15/25

class BaronCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "BaronCard"
	cardName = "Baron"
	cardPrint = "\033[37mBaron\033[0m"
	description = "You may discard an Estate card. If you do, +$4. Otherwise, gain an Estate card."
	cost = 4
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		if any(i.cardName == 'Estate' for i in self.player.playerHand):
			while True:
				self.send_data(self.player.playerConn, "Would you like to discard an Estate? (y/n)\n")
				choice = self.recv_data(self.player.playerConn, 1024)
				if choice.lower() not in ['y', 'n']:
					continue
				elif choice.lower() == 'y':
					while True:
						for card in self.player.playerHand:
							if card.cardName == 'Estate':
								self.player.playerDiscard.append(self.player.playerHand[card])
								del self.player.playerHand[card]
								self.player.playerTurnTreasure += 4
								break
				elif choice.lower() == 'n':
					break
		else:
			self.player.gainCard(0, 0, 'discard', 'self.deck.estateCards')
			return				

class Courtyard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "CourtyardCard"
	cardName = "Courtyard"
	cardPrint = "\033[37mCourtyard\033[0m"
	description = "Put a card from your hand on top of your deck."
	cost = 2
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.send_data(self.player.playerConn, "Choose a card to put on top of your deck:\n")
		self.player.printHandUpdate()
		choice = self.recv_data(self.player.playerConn, 1024)
		self.player.playerDeck.insert(0, self.player.playerHand[choice - 1])
		del self.player.playerHand[choice - 1]

	return

class DukeCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "DukeCard"
	cardName = "Duke"
	cardPrint = "\033[32mDuke\033[0m"
	description = "Worth 1 VP for each Duchy you have."
	cost = 5
	victoryPoints = 1 * self.
	action = False
	victory = True
	def __init__(self):
		pass
	
class GreatHallCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "GreatHallCard"
	cardName = "Great Hall"
	cardPrint = "\033[32mG\033[37mr\033[32me\033[37ma\033[32mt \033[32mH\033[37ma\033[32ml\033[37ml\033[0m"
	description = "+1 Card; +1 Action"
	victoryPoints = 1	
	cost = 3
	victory = True
	action = True

	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.player.drawOneCard()
		self.player.playerTurnActions += 1

class HaremCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "HaremCard"
	cardName = "Harem"
	cardPrint = "\033[32mH\033[33ma\033[32mr\033[33me\033[32mm"
	description = "Worth $2 and 2VP."
	victoryPoints = 2	
	cost = 6
	value = 2
	victory = True
	treasure = True

	def __init__(self):
		pass
			
class IronWorksCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "IronWorksCard"
	cardName = "Iron Works"
	cardPrint = "\033[37mIron Works\033[0m"
	description = "Gain a card costing up to 4 Coins. If it is an... Action card, +1 Action. Treasure card, +1 Coin. Victory card, +1 Card."
	cost = 4
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.cost = cost
		self.number = 1
		self.location = self.playerDiscard
		self.type = type
		self.gain = self.gainCard(4, 1, 'discard', 'any')
		if self.gain.action:
			self.player.playerTurnActions += 1
		if self.gain.treasure:
			self.player.playerTurnTreasure += 1
		if self.gain.victory:
			self.palyer.drawOneCard()
		return

class MiningVillageCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "MiningVillageCard"
	cardName = "Mining Village"
	cardPrint = "\033[37mMining Village\033[0m"
	description = "You may trash this card immediately, If you do, +2 Coins."
	cost = 4
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		send_data(self,player.playerConn, "Would you like to trash " + self.cardPrint + " (y/n)?\n")
		while True:
			choice = recv_data(self.player.playerConn, 1024)
			if choice.lower not in ['y', 'n']:
				continue
			elif choice.lower() == 'y':
				while True:
					for card in self.player.playerHand:
						if card.cardName == 'Mining Village':
							self.player.playerHand.remove(card)
							self.player.playerTurnTreasure += 2
							break
					else:
						continue
			else:
				break
		return

class MinionCard(KingdomCard):
	cardEval = "MinionCard"
	cardName = "Minion"
	cardPrint = "\033[1;31mMinion\033[0m"
	description = "Choose one: +2 Coins, or discard your hand, +4 cards, and each other player with at least 5 cards in hand discards his hand and draws 4 cards."
	cost = 5
	action = True
	attack = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerTurnActions += 1

		while True:
			discard = raw_input("Choose one: +2 c[o]ins or [d]iscard your hand, +4 cards, and each other player with at least 5 cards in hand discards his hand and draws 4 cards. ")
			if discard.lower() not in ['o', 'd']:
				raw_input("That is not an available option, please choose c(o)ins or (d)iscard! ")
			elif discard.lower() == 'o':
				self.player.playerTurnTreasure += 2
				break
			elif 
				for i in len(self.player.playerHand):
					self.player.playerDiscard.append(self.player.playerHand[i])
					del self.player.playerHand[i]
				self.draw = 4
				for i in draw:
					if len(self.player.playerDeck) == 0:
						self.player.playerDiscardToDeck()
						self.player.playerHand.append(self.player.playerDeck[0])
						del self.player.playerDeck[0]
					else:
						self.player.playerHand.append(self.player.playerDeck[0])
						del self.player.playerDeck[0]		

				self.player.checkReactions('attack')
				for each in self.roster:
					if each.reactionImmunity == False and each.durationImmunity == False:
						each.checkPlayerDeck()
						if len(each.player.playerHand) > 4:
							for i in len(self.player.playerHand):
								each.player.playerDiscard.append(each.player.playerHand[i])
								del each.player.playerHand[i]
							each.draw = 4
							for i in draw:
								if len(each.player.playerDeck) == 0:
									each.player.playerDiscardToDeck()
									each.player.playerHand.append(each.player.playerDeck[0])
									del each.player.playerDeck[0]
								else:
									each.player.playerHand.append(each.player.playerDeck[0])
									del each.player.playerDeck[0]		

				for each in self.roster:
					each.reactionImmunity = False
		
				break
				
class NoblesCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "NoblesCard"
	cardName = "Nobles"
	cardPrint = "\033[32mN\033[37mo\033[32mb\033[37ml\033[32me\033[37ms\033[0m"
	description = "Choose one: +3 Cards, or +2 Actions,   2 VP"
	victoryPoints = 2
	cost = 6
	victory = True
	action = True

	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck

		while True:
			discard = raw_input("Choose one: +3 [c]ards or +2 [a]ctions. ")
			if discard.lower() not in ['c', 'a']:
				raw_input("That is not an available option, please choose (c)ards or (a)ctions! ")
			elif discard.lower() == 'c':
				self.draw = 3
				for i in draw:
					if len(self.player.playerDeck) == 0:
						self.player.playerDiscardToDeck()
						self.player.playerHand.append(self.player.playerDeck[0])
						del self.player.playerDeck[0]
					else:
						self.player.playerHand.append(self.player.playerDeck[0])
						del self.player.playerDeck[0]		
				break
			elif discard.lower() == 'a':
				self.player.playerTurnActions += 2
				break

class PawnCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "PawnCard"
	cardName = "Pawn"
	cardPrint = "\033[37mPawn\033[0m"
	description = "Choose two: +1 Card, +1 Action, +1 Buy, +1 Coin. (The choices must be different)"
	cost = 2
	action = True

	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		
		while True:
			choice = raw_input("Choose one: +1 [c]ard, +1 [a]ction, +1 [b]uy, or +1 c[o]in. ")
			if choice.lower() not in ['c', 'a', 'b', 'o']:
				raw_input("That is not an available option, please choose (c)ard, (a)ction, (b)uy or c(o)in! ")
				choice = ''
				continue
			elif choice.lower() == 'c':
				if len(self.player.playerDeck) == 0:
					self.player.playerDiscardToDeck()
					self.player.playerHand.append(self.player.playerDeck[0])
					del self.player.playerDeck[0]
				else:
					self.player.playerHand.append(self.player.playerDeck[0])
					del self.player.playerDeck[0]		
			elif choice.lower() == 'a':
				self.player.playerTurnActions += 1
			elif choice.lower() == 'b':
				self.player.playerTurnBuys += 1
			elif choice.lower() == 'o':
				self.player.playerTurnTreasure += 1
			
			if len(choice) > 0: 
				break
		
		while True:
			if choice = 'c':
				choice2 = raw_input("Choose one: +1 [a]ction, +1 [b]uy, or +1 c[o]in. ")
				if choice2.lower() not in ['a', 'b', 'o']:
					raw_input("That is not an available option, please choose (a)ction, (b)uy or c(o)in! ")
					choice2 = ''
					continue
			elif choice = 'a':
				choice2 = raw_input("Choose one: +1 [c]ard, +1 [b]uy, or +1 c[o]in. ")
				if choice2.lower() not in ['c', 'b', 'o']:
					raw_input("That is not an available option, please choose (c)ard, (b)uy or c(o)in! ")
					choice2 = ''
					continue
			elif choice = 'b':
				choice2 = raw_input("Choose one: +1 [c]ard, +1 [a]ction, or +1 c[o]in. ")
				if choice2.lower() not in ['c', 'a', 'o']:
					raw_input("That is not an available option, please choose (c)ard, (a)ction or c(o)in! ")
					choice2 = ''
					continue
			elif choice = 'o':
				choice2 = raw_input("Choose one: +1 [c]ard, +1 [a]ction, or +1 b[u]y. ")
				if choice2.lower() not in ['c', 'a', 'b']:
					raw_input("That is not an available option, please choose (c)ard, (a)ction or (b)uy! ")
					choice2 = ''
					continue

			if len(choice2) > 0: 
				if choice2.lower() == 'c':
					if len(self.player.playerDeck) == 0:
						self.player.playerDiscardToDeck()
						self.player.playerHand.append(self.player.playerDeck[0])
						del self.player.playerDeck[0]
					else:
						self.player.playerHand.append(self.player.playerDeck[0])
						del self.player.playerDeck[0]		
				elif choice2.lower() == 'a':
					self.player.playerTurnActions += 1
				elif choice2.lower() == 'b':
					self.player.playerTurnBuys += 1
				elif choice2.lower() == 'o':
					self.player.playerTurnTreasure += 1
				break
				
class ShantyTownCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "ShantyTownCard"
	cardName = "Shanty Town"
	cardPrint = "\033[37mShanty Town\033[0m"
	description = "Reveal your hand. If you have no actions cards in hand, +2 Cards."
	cost = 3
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.player.playerTurnActions += 2
		self.hasActions = False
		for card in self.player.playerHand:
			self.reveal.append("\n " + self.playerName + " reveals " + self.playerHand[card].cardName + ".")
			if card.cardType == 'Action':
				self.hasActions = True
				break
			else:
				continue
		break

		if self.hasActions:
			break
		else:
			self.draw = 2
			for i in draw:
				if len(self.player.playerDeck) == 0:
					self.player.playerDiscardToDeck()
					self.player.playerHand.append(self.player.playerDeck[0])
					del self.player.playerDeck[0]
				else:
					self.player.playerHand.append(self.player.playerDeck[0])
					del self.player.playerDeck[0]		
			return
			
class StewardCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "StewardCard"
	cardName = "Steward"
	cardPrint = "\033[37mSteward\033[0m"
	description = "Choose one: +2 cards, or +2 Coins, or trash 2 cards from your hand."
	cost = 3
	action = True

	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		
		while True:
			choice = raw_input("Choose one: +2 [c]ards, or +2 C[o]ins, or [t]rash 2 cards from your hand.")
			if choice.lower() not in ['c', 'o', 't']:
				raw_input("That is not an available option, please choose +2 (c)ards, +2 c(o)ins, or (t)rash 2 cards! ")
				choice = ''
				continue
			elif choice.lower() == 'c':
				self.draw = 2
				for i in draw:
					if len(self.player.playerDeck) == 0:
						self.player.playerDiscardToDeck()
						self.player.playerHand.append(self.player.playerDeck[0])
						del self.player.playerDeck[0]
					else:
						self.player.playerHand.append(self.player.playerDeck[0])
						del self.player.playerDeck[0]
				break
			elif choice.lower() == 'o':
				self.player.playerTurnTreasure += 2
				break
			elif choice.lower() == 't':
				self.trash = 2
				for i in trash
					if len(self.player.playerHand) > 0:
						while True:
							choice = raw_input("\n Please choose a card to trash: ")
							if (int(choice) - 1) not in range(len(self.player.playerHand)):
								print "Please choose an appropriate card! "
								continue
							else:
								del self.player.playerHand[int(choice) - 1]
								break
				break

class TradingPost(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "TradingPostCard"
	cardName = "Trading Post"
	cardPrint = "\033[37mTrading Post\033[0m"
	description = "Trash 2 cards from your hand. If you do, gain a Silver card, put it into your hand."
	cost = 5
	action = True

	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck

		while True:
			trash = raw_input("Would you like to trash 2 cards from your hand (y/n)? ")
			if trash.lower() not in ['y', 'n']:
				raw_input("That is not an available option, please choose (y)es or (n)o! ")
			elif trash.lower() == 'n':
				break
			elif trash.lower() == 'y':
				self.trashCards = 2
				for i in trashCards
					if len(self.player.playerHand) > 0:
						while True:
							choice = raw_input("\n Please choose a card to trash: ")
							if (int(choice) - 1) not in range(len(self.player.playerHand)):
								print "Please choose an appropriate card! "
								continue
							else:
								del self.player.playerHand[int(choice) - 1]
								self.trashed += 1
								break

				if self.trashed = 2:
					if len(self.deck.silverCards) == 0:
						pass
					else:
						self.player.gainCard(value, 1, 'hand', 'treasure')
						
				break
				
class UpgradeCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "UpgradeCard"
	cardName = "Upgrade"
	cardPrint = "\033[37mUpgrade\033[0m"
	description = "Trash a card form your hand. Gain a card costing exactly 1 Coin more than it."
	cost = 5
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.player.playerTurnActions += 1
		if len(self.player.playerDeck) == 0:
			self.player.playerDiscardToDeck()
			self.player.playerHand.append(self.player.playerDeck[0])
			del self.player.playerDeck[0]
		else:
			self.player.playerHand.append(self.player.playerDeck[0])
			del self.player.playerDeck[0]		

		if len(self.player.playerHand) > 0:
			while True:
				choice = raw_input("\n Please choose a card to trash: ")
				if (int(choice) - 1) not in range(len(self.player.playerHand)):
					print "Please choose an appropriate card! "
				else:
					value = 1 + self.player.playerHand[int(choice) - 1].cost
					del self.player.playerHand[int(choice) - 1]
					self.player.gainCard(value, 1, 'discard', 'any')
					break

class WishingWellCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "WishingWellCard"
	cardName = "Wishing Well"
	cardPrint = "\033[37mWishing Well\033[0m"
	description = "Name a card. Reveal the top card of your deck. If it’s the named card, put it into your hand."
	cost = 3
	action = True
	def __init__(self):
		pass

		def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.player.playerTurnActions += 1
		if len(self.player.playerDeck) == 0:
			self.player.playerDiscardToDeck()
			self.player.playerHand.append(self.player.playerDeck[0])
			del self.player.playerDeck[0]
		else:
			self.player.playerHand.append(self.player.playerDeck[0])
			del self.player.playerDeck[0]		

		self.type = type
		self.location = self.playerHand
		choices = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		nonkingdom = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c']
		kingdom = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		while True:
			choice = raw_input("    Please name a card: ")
				if choice.lower() not in choices:
						print "    Invalid selection, please choose another card!"
				if choice.lower() in nonkingdom:
					if choice.lower() == 'o' or choice.lower == 'l':
						print "    Invalid selection, please choose another card!"
					else:
						p = self.deck.provinceCards
						d = self.deck.duchyCards
						e = self.deck.estateCards
						g = self.deck.goldCards
						s = self.deck.silverCards
						c = self.deck.copperCards
						u = self.deck.curseCards

						choice = eval(choice.lower())
						print self.playerName + " reveals: " + self.playerDeck[0].cardName + "..."						
						if self.playerDeck[0].cardName = choice.cardName:
							self.player.playerHand.append(self.player.playerDeck[0])
						else:
							self.playerDiscard.append(self.playerDeck[card])
						del self.player.playerDeck[0]

						break
				elif choice.lower() in kingdom:
					x = 'card' + choice.lower()
					print self.playerName + " reveals: " + self.playerDeck[0].cardName + "..."											
					if self.playerDeck[0].cardName = choice.cardName:
						self.player.playerHand.append(self.player.playerDeck[0])
					else:
						self.playerDiscard.append(self.player.playerDeck[0])
					del self.player.playerDeck[0]
					break
			break

			
		

