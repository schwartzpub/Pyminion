#15/25

class BaronCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "BaronCard"
	cardName = "Baron"
	cardColor = "\033[0m"
	description = "You may discard an estate card. If you do, +4 Coin. Otherwise, gain an estate card."
	cost = 4
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		if any(i.cardName == 'Estate' for i in self.player.playerHand):
			while True:
				#choice = raw_input(" Would you like to discard an Estate (y/n)? ")
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
			self.player.playerDiscard.append(self.deck.estateCards[0])
			return				

class Courtyard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "CourtyardCard"
	cardName = "Courtyard"
	cardColor = "\033[0m"
	description = "Put a card from your hand on top of your deck."
	cost = 2
	action = True
	def __init__(self):
		pass

	def playCard(self, player, roster, deck):
		self.player = player
		self.hasActions = False
		self.draw = 3
		for i in draw:
			if len(self.player.playerDeck) == 0:
				self.player.playerDiscardToDeck()
				self.player.playerHand.append(self.player.playerDeck[0])
				del self.player.playerDeck[0]
			else:
				self.player.playerHand.append(self.player.playerDeck[0])
				del self.player.playerDeck[0]		
		
		#choice = int(raw_input("      Choose a card to put on top of your deck: "))
		self.send_data(self.player.playerConn, "Choose a card to put on top of your deck:\n")
		choice = self.recv_data(self.player.playerConn, 1024)
		self.player.playerDeck.insert(0, self.player.playerHand[choice - 1])
		del self.player.playerHand[choice - 1]

	return

class DukeCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "DukeCard"
	cardName = "Duke"
	cardColor = "\033[32m"
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
	cardColor = "\033[32m"
	#cardColor = "\033[0m"
	victoryPoints = 1	
	cost = 3
	victory = True
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

class HaremCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "HaremCard"
	cardName = "Harem"
	cardColor = "\033[32m"
	#cardColor = "\033[0m"
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
	cardColor = "\033[0m"
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
		choices = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		nonkingdom = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c']
		kingdom = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		while True:
			for i in range(self.number):
				choice = raw_input("    Please select a card that costs up to $" + str(self.cost) + ": ")
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
						if choice[0].cost > self.cost:
							print "    Invalid selection, please choose another card!"
						else:
							self.location.append(choice[0])
							del choice[0]
							break
				elif choice.lower() in kingdom:
					x = 'card' + choice.lower()
					if self.deck.kingdomCards[x][0].cost > cost:
						print "    Invalid selection, please choose another card!"
					else:
						self.location.append(self.deck.kingdomCards[x][0])
						del self.deck.kingdomCards[x][0]
						break
				
				self.location.append(choice[0])		
				if choice.cardType == "action":
					self.player.playerTurnActions += 1
					break
				elif choice.cardType == "treasure":
					self.player.playerTurnTreasure += 4
					break
				elif choice.cardType == "victory":
					if len(self.player.playerDeck) == 0:
						self.player.playerDiscardToDeck()
						self.player.playerHand.append(self.player.playerDeck[0])
						del self.player.playerDeck[0]
					else:
						self.player.playerHand.append(self.player.playerDeck[0])
						del self.player.playerDeck[0]
					break
			break
			return
			
class MiningVillageCard(KingdomCard):
	#cardSet = "Intrigue"
	cardEval = "MiningVillageCard"
	cardName = "Mining Village"
	cardColor = "\033[0m"
	description = "You may trash this card immediately, If you do, +2 Coins."
	cost = 4
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
		self.player.playerTurnActions += 2

		choice = raw_input(" Would you like to trash Mining Village (y/n)? ")
		if choice.lower() == 'y':
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
	cardColor = "\033[1;31m"
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
	cardColor = "\033[32m"
	#cardColor = "\033[0m"
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
	cardColor = "\033[0m"
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
	cardColor = "\033[0m"
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
	cardColor = "\033[0m"
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
	cardColor = "\033[0m"
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
	cardColor = "\033[0m"
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
	cardColor = "\033[0m"
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

			
		

