#15/25
import sys, os, time, errno, socket

class IntrigueCard(object):
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

	def send_data (self, game, client, data):
		message = str(data)
		self.game = game
		try:
			return client.send(message)
		except socket.error, e:
			if e.errno == errno.EPIPE:
				for player in self.roster:
					if player.playerConn == client:
						[self.send_data(c, player.playerName + " has been disconnected and removed from the game. (Broken Pipe)\n") for c in (u.playerConn for u in self.roster if u.playerConn != client )]
						print player.playerName + " has quit mid-game. (Broken Pipe)"
						self.roster.remove(player)
						time.sleep(2)
			else:
				clients.remove(client)
				for player in self.roster:
					if player.playerConn == client:
						[self.send_data(c, player.playerName + " has been disconnected and removed from the game. (Connection Reset by Peer)\n") for c in (u.playerConn for u in self.roster if u.playerConn != client )]
						print player.playerName + " has quit. (Connection Reset By peer)"
						self.roster.remove(player)
						time.sleep(2)
	def recv_data (self, game, client, length):
		self.playerConn = client
		self.game = game
		try:
			self.playerConn.settimeout(600)
			data = self.playerConn.recv(length)
			self.playerConn.settimeout(None)
			if not data: self.send_data(self.playerConn, "Please choose an option...\n")
			return data
		except socket.timeout:
			for user in self.roster:
				if user.playerConn != self.playerConn:
					self.send_data(user.playerConn, self.playerName + " is taking a bit to respond...be patient.\n")
		except socket.error, e:
			if e.errno == errno.EPIPE:
				for player in self.roster:
					if player.playerConn == client:
						[self.send_data(c, player.playerName + " has been disconnected and removed from the game. (Broken Pipe)\n") for c in (u.playerConn for u in self.roster if u.playerConn != client )]
						print player.playerName + " has quit mid-game. (Broken Pipe)"
						self.roster.remove(player)
						self.game.playerRost.remove(player)
						time.sleep(2)
			else:
				clients.remove(client)
				for player in self.roster:
					if player.playerConn == client:
						[self.send_data(c, player.playerName + " has been disconnected and removed from the game. (Connection Reset by Peer)\n") for c in (u.playerConn for u in self.roster if u.playerConn != client )]
						print player.playerName + " has quit. (Connection Reset By peer)"
						self.roster.remove(player)
						self.game.playerRost.remove(player)
						time.sleep(2)

class BaronCard(IntrigueCard):
	cardEval = "BaronCard"
	cardName = "Baron"
	cardPrint = "\033[37mBaron\033[0m"
	description = "You may discard an Estate card. If you do, +$4. Otherwise, gain an Estate card."
	cost = 4
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		self.player.playerTurnBuys += 1
		if any(i.cardName == 'Estate' for i in self.player.playerHand):
			IntrigueCard.send_data(self, self.game, self.player.playerConn, "Would you like to discard an Estate (y/n)?\n")
			while True:
				choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
				if choice.lower() not in ['y', 'n']:
					continue
				elif choice.lower() == 'y':
					for card in each.playerHand:
						if card.cardName == 'Estate':
							self.player.playerDiscard.append(card)
							del self.current[card]
							self.player.playerTurnTreasure += 4
							for each in self.roster:
								IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " discards an Estate.\n")
							break
						else: pass
				elif choice.lower() == 'n':
					if len(self.deck.estateCards) > 0:
						self.player.gainCard(0, 1, 'discard', 'estateCards')
						for each in self.roster:
							IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " gains an Estate.\n")
					else: return
		else:
			if len(self.deck.estateCards) > 0:
				self.player.gainCard(0, 1, 'discard', 'estateCards')
				for each in self.roster:
					IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " gains an Estate.\n")
			else: return

#todo: start
class BridgeCard(IntrigueCard):
	cardEval = "BridgeCard"
	cardName = "Bridge"
	cardPrint = "\033[37mBridge\033[0m"
	description = "All cards (including cards in players' hands) cost 1 Coin less this turn, but no less than 0 Coin."
	cost = 4
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		self.player.playerTurnTreasure += 1
		self.player.playerTurnBuys += 1

class ConspiratorCard(IntrigueCard):
	cardEval = "ConspiratorCard"
	cardName = "Conspirator"
	cardPrint = "\033[37mConspirator\033[0m"
	description = "If you played 3 or more Actions this turn (counting this): +1 Card, +1 Action."
	cost = 4
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		self.player.playerTurnTreasure += 2
		if (self.playerActionsPlayed) > 2:
			self.player.drawOneCard()
			self.player.playerTurnActions += 1
		return

#todo: start
class CoppersmithCard(IntrigueCard):
	cardEval = "CoppersmithCard"
	cardName = "Coppersmith"
	cardPrint = "\033[37mCoppersmith\033[0m"
	description = "Copper produces an extra 1 Coin this turn."
	cost = 4
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		#CopperCard.value += 1

		
	def playDiscard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		#CopperCard.value = 1
		return

class Courtyard(IntrigueCard):
	cardEval = "CourtyardCard"
	cardName = "Courtyard"
	cardPrint = "\033[37mCourtyard\033[0m"
	description = "Put a card from your hand on top of your deck."
	cost = 2
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		for i in range(3):
			self.player.drawOneCard()
		IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose a card to put on top of your deck:\n")
		while True:
			self.player.printHandUpdate()
			choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
			try:
				choice = int(choice) - 1
			except: continue
			if choice not in range(len(self.player.playerHand)): continue
			else:
				self.player.playerDeck.insert(0, self.player.playerHand[choice])
				del self.player.playerHand[choice]
				for each in self.roster:
					IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " has put a card on top of their deck.\n")
				break

class DukeCard(IntrigueCard):
	cardEval = "DukeCard"
	cardName = "Duke"
	cardPrint = "\033[32mDuke\033[0m"
	description = "Worth 1 VP for each Duchy you have."
	cost = 5
	#todo: not sure if this is valid...
	victoryPoints = len(self.player.playerDeck.duchyCards)
	action = False
	victory = True
	def __init__(self, game):
		self.game = game
		self.embargoed = False
		self.embargo = 0

class GreatHallCard(IntrigueCard):
	cardEval = "GreatHallCard"
	cardName = "Great Hall"
	cardPrint = "\033[32mG\033[37mr\033[32me\033[37ma\033[32mt \033[32mH\033[37ma\033[32ml\033[37ml\033[0m"
	description = "+1 Card; +1 Action"
	cost = 3
	victoryPoints = 1
	victory = True
	action = True

	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.player.drawOneCard()
		self.player.playerTurnActions += 1

class HaremCard(IntrigueCard):
	cardEval = "HaremCard"
	cardName = "Harem"
	cardPrint = "\033[32mH\033[33ma\033[32mr\033[33me\033[32mm"
	description = "Worth $2 and 2VP."
	cost = 6
	value = 2
	victoryPoints = 2
	victory = True
	treasure = True

	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

class IronWorksCard(IntrigueCard):
	cardEval = "IronWorksCard"
	cardName = "Iron Works"
	cardPrint = "\033[37mIron Works\033[0m"
	description = "Gain a card costing up to 4 Coins. If it is an... Action card, +1 Action. Treasure card, +1 Coin. Victory card, +1 Card."
	cost = 4
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		self.gain = self.player.gainCard(4, 1, 'discard', 'any')
		if self.gain.action:
			self.player.playerTurnActions += 1
		if self.gain.treasure:
			self.player.playerTurnTreasure += 1
		if self.gain.victory:
			self.player.drawOneCard()

#todo: needs work, current code from smugglers
class MasqueradeCard(IntrigueCard):
	cardEval = "MasqueradeCard"
	cardName = "Masquerade"
	cardPrint = "\033[37mMasquerade\033[0m"
	description = "Each player passes a card from his hand to the left at once. Then you may trash a card from your hand."
	cost = 3
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		self.player.drawOneCard()
		self.player.drawOneCard()


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
						SeasideCard.send_data(self, self.game, self.player.playerConn, "Please choose a card to Gain: ",)
						for card in self.options:
							SeasideCard.send_data(self, self.game, self.player.playerConn, "[" + str(i) + "]" + card.cardPrint + " ",)
							i += 1
						SeasideCard.send_data(self, self.game, self.player.playerConn, "\n")
						while True:
							choice = SeasideCard.recv_data(self, self.game, self.player.playerConn, 1024)
							try: choice = int(choice) - 1
							except: continue
							if choice not in range(len(self.options)): continue
							else:
								self.player.gainCard(0, 1, 'discard', card)
								for each in self.roster:
									SeasideCard.send_data(self, self.game, each.playerConn, self.player.playerName + " gains a " + card.cardPrint + ".\n")
								break
					else: return
				else:
					if any(i.cost <= 6 for i in self.roster[self.previous].gained) and len(self.roster[self.previous].gained) > 0:
						self.previous = position - 1
						for card in self.roster[self.previous].gained:
							if card.cost <= 6:
								self.options.append(card)
							else: pass
						SeasideCard.send_data(self, self.game, self.player.playerConn, "Please choose a card to Gain: ",)
						for card in self.options:
							SeasideCard.send_data(self, self.game, self.player.playerConn, "[" + str(i) + "]" + card.cardPrint + " ",)
							i += 1
						SeasideCard.send_data(self, self.game, self.player.playerConn, "\n")
						while True:
							choice = SeasideCard.recv_data(self, self.game, self.player.playerConn, 1024)
							try: choice = int(choice) - 1
							except: continue
							if choice not in range(len(self.options)): continue
							else:
								self.player.gainCard(0, 1, 'discard', card)
								for each in self.roster:
									SeasideCard.send_data(self, self.game, each.playerConn, self.player.playerName + " gains a " + card.cardPrint + ".\n")
								break
					else: return
		return

class MiningVillageCard(IntrigueCard):
	cardEval = "MiningVillageCard"
	cardName = "Mining Village"
	cardPrint = "\033[37mMining Village\033[0m"
	description = "You may trash this card immediately, If you do, +2 Coins."
	cost = 4
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		IntrigueCard.send_data(self, self.game, self.player.playerConn, "Would you like to trash " + self.cardPrint + " (y/n)?\n")
		while True:
		choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
			if choice.lower not in ['y', 'n']:
				continue
			elif choice.lower() == 'y':
				while True:
					for card in self.player.playerPlay:
						if card.cardName != 'Mining Village': pass
						else:
						self.player.playerPlay.remove(card)
						#todo: do i need two breaks here??
						break
				self.player.playerTurnTreasure += 2
			else:
				break
		return

class MinionCard(IntrigueCard):
	cardEval = "MinionCard"
	cardName = "Minion"
	cardPrint = "\033[1;31mMinion\033[0m"
	description = "Choose one: +2 Coins, or discard your hand, +4 cards, and each other player with at least 5 cards in hand discards his hand and draws 4 cards."
	cost = 5
	action = True
	attack = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.player.playerTurnActions += 1

		while True:
			choice = IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose one: +2 c[o]ins or [d]iscard your hand, +4 cards, and each other player with at least 5 cards in hand discards his hand and draws 4 cards.\n")
			if choice.lower() not in ['o', 'd']:
				continue
			elif discard.lower() == 'o':
				self.player.playerTurnTreasure += 2
				break
			elif discard.lower() == 'd':

				for each in self.roster:
					IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " discards his hand.  +4 cards, and each other player with at least 5 cards in hand discards his hand and draws 4 cards.\n")
					
				i = 0
				while i < len(self.player.playerHand):
					self.player.playerDiscard.append(self.player.playerHand[0])
					del self.player.playerHand[0]

				for i in range(4):
					self.player.drawOneCard()

				self.player.checkReactions('attack')
				for each in self.roster:
					if each != self.player and each.reactionImmunity == False and each.durationImmunity == False:
						while i < len(each.player.playerHand):
							each.player.playerDiscard.append(each.player.playerHand[0])
							del each.player.playerHand[0]
							for each in self.roster:
						for i in range(4):
							each.drawOneCard()
						for player in self.roster:
							IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " has discarded their hand and drew 4 cards.\n")

					else:
						if each.reactionImmunity == True:
							for player in self.roster:
								IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " was protected by reaction immunity.\n")
						elif each.durationImmunity == True:
							for player in self.roster:
								IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " was protected by duration immunity.\n")
						pass

				#todo: IS THIS REALLY NECESSARY?
				for each in self.roster:
					each.reactionImmunity = False

				return

class NoblesCard(IntrigueCard):
	cardEval = "NoblesCard"
	cardName = "Nobles"
	cardPrint = "\033[32mN\033[37mo\033[32mb\033[37ml\033[32me\033[37ms\033[0m"
	description = "Choose one: +3 Cards, or +2 Actions, 2 VP"
	victoryPoints = 2
	cost = 6
	victory = True
	action = True

	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose one: +3 [c]ards, or +2 [a]ctions:\n")
		while True:
		choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
			if choice.lower not in ['c', 'a']:
				continue
			elif choice.lower() == 'c':
				for i in range(3):
					self.player.drawOneCard()
			elif choice.lower() == 'a':
				self.player.playerTurnActions += 2
			else:
				break
		return

class PawnCard(IntrigueCard):
	cardEval = "PawnCard"
	cardName = "Pawn"
	cardPrint = "\033[37mPawn\033[0m"
	description = "Choose two: +1 Card, +1 Action, +1 Buy, +1 Coin. (The choices must be different)"
	cost = 2
	action = True

	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.roster = roster

		IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose one: +1 [c]ard, +1 [a]ction, +1 [b]uy, or +1 c[o]in: \n")
		while True:
		choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
			if choice.lower() not in ['c', 'a', 'b', 'o']:
				continue
			elif choice.lower() == 'c':
				self.player.drawOneCard()
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
			    IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose one: +1 [a]ction, +1 [b]uy, or +1 c[o]in: \n")
				choice2 = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
				if choice2.lower() not in ['a', 'b', 'o']:
					continue
			elif choice = 'a':
			    IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose one: +1 [c]ard, +1 [b]uy, or +1 c[o]in: \n")
				choice2 = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
				if choice2.lower() not in ['c', 'b', 'o']:
					continue
			elif choice = 'b':
				IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose one: +1 [c]ard, +1 [a]ction, or +1 c[o]in: \n")
				choice2 = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024))
				if choice2.lower() not in ['c', 'a', 'o']:
					continue
			elif choice = 'o':
				IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose one: +1 [c]ard, +1 [a]ction, or +1 b[u]y: \n")
				choice2 = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024))
				if choice2.lower() not in ['c', 'a', 'b']:
					continue

			if len(choice2) > 0: 
				if choice2.lower() == 'c':
					self.player.drawOneCard()
				elif choice2.lower() == 'a':
					self.player.playerTurnActions += 1
				elif choice2.lower() == 'b':
					self.player.playerTurnBuys += 1
				elif choice2.lower() == 'o':
					self.player.playerTurnTreasure += 1
				break
			
		return

#todo: REVIEW: need to limit options, verify breaks in correct place
class SaboteurCard(IntrigueCard):
	cardEval = "SaboteurCard"
	cardName = "Saboteur"
	cardPrint = "\033[1;31mSaboteur\033[0m"
	description = "Each other player reveals cards from the top of his deck until revealing one costing 3 Coins or more. He trashes that card and may gain a card costing at most 2 Coins less than it. He discards the other revealed cards."
	cost = 5
	action = True
	attack = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		self.options = []

		self.player.checkReactions('attack')
			for each in self.roster:
				if each != self.player and each.reactionImmunity == False and each.durationImmunity == False:

					self.trashed = False
					self.trash = []
					for each in self.roster:
						if each == self.player: pass
						else:
							for i in each.player.playerDeck:
								for player in self.roster:
									#if player.playerTurn: pass
									IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " reveals a " + each.player.playerDeck[i].cardPrint + ".\n")
								
								if (i.cost > 2):
									self.trashed = True
									for player in self.roster:
										#if player.playerTurn: pass
										IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " trashes a " + each.player.playerDeck[i].cardPrint + ".\n")
									
									each.playerDiscardToDeck()
									self.trash.append(each.player.playerDeck[i])
									del each.player.playerDeck[i]
									
									IntrigueCard.send_data(each, each.game, each.player.playerConn, "Please choose a card costing up to " + i.cost - 2 + " to gain: ",)
									choice = IntrigueCard.recv_data(each, each.game, each.player.playerConn, 1024)
									
									#limit options? is self.gain enough??
									self.gain = self.player.gainCard(i.cost - 2, 1, 'discard', 'any')
									
									for card in self.options:
										IntrigueCard.send_data(self, self.game, self.player.playerConn, "[" + str(i) + "]" + card.cardPrint + " ",)
										i += 1
										IntrigueCard.send_data(self, self.game, self.player.playerConn, "\n")

										while True:
											choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
											try: choice = int(choice) - 1
											except: continue
											if choice not in range(len(self.options)): continue
											else:
												self.player.gainCard(0, 1, 'discard', card)
												for each in self.roster:
													if player.playerTurn: pass
													IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " gains a " + card.cardPrint + ".\n")
												break

								else:
									for player in self.roster:
										if player.playerTurn: pass
										IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " discards a " + each.player.playerDeck[i].cardPrint + ".\n")

									each.playerDiscard.append(i)
									each.player.playerDeck.remove(i)
									continue
									
									

				else:
					if each.reactionImmunity == True:
						for player in self.roster:
							IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " was protected by reaction immunity.\n")
					elif each.durationImmunity == True:
						for player in self.roster:
							IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " was protected by duration immunity.\n")
					pass

class ScoutCard(IntrigueCard):
	cardEval = "ScoutCard"
	cardName = "Scout"
	cardPrint = "\033[37mScout\033[0m"
	description = "Reveal the top 4 cards of your deck. Put the revealed Victory cards into your hand. Put the other cards on top your deck in any order."
	cost = 4
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		self.reveal = []

		for i in range(4):
			self.reveal.append(self.player.playerDeck[i])
			del self.player.playerDeck[i]

		for player in self.roster:
			IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " reveals: [1]" + self.reveal[0].cardPrint + " [2]" + self.reveal[1].cardPrint + " [3]" + self.reveal[2].cardPrint + " [4]" + self.reveal[3].cardPrint + "\n")

		for i in self.reveal:
			if i.victory: 
				self.player.playerHand.append(i)
				del self.reveal[i]

		if len(self.reveal) > 2:
			IntrigueCard.send_data(self, self.game, self.player.playerConn, "Place the cards back on your deck one at a time: ")
			i = 0
			ri = len(self.reveal)
			while i < len(self.reveal):
				x = 0
				for card in self.reveal:
					x += 1
					IntrigueCard.send_data(self, self.game, self.player.playerConn, "[" + str(x) + "]" + card.cardPrint + " ",)
					IntrigueCard.send_data(self, self.game, self.player.playerConn, "\n")
					choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
					try: choice = int(choice) - 1
					except: continue
					if choice not in range(len(self.reveal)): continue
					else:
						self.player.playerDeck.insert(0, self.reveal[choice])
						del self.reveal[choice]
						i += 1
				for each in self.roster:
					IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " placed " + ri + " cards back on top of his deck.\n")
				break

		elif len(self.reveal) == 1:
				self.player.playerDeck.append(self.reveal[0])
				del self.reveal[0]
				for each in self.roster:
					IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " placed 1 card back on top of his deck.\n")
		else:
			for each in self.roster:
				IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " placed no cards back on top of his deck.\n")

class SecretChamberCard(IntrigueCard):
	cardEval = "SecretChamberCard"
	cardName = "Secret Chamber"
	cardPrint = "\033[36mSecret Chamber\033[0m"
	description = "[Action]: Discard any number of cards. +1 Coin for per card discarded. [Reaction]: When another player plays an Attack card, you may reveal this from your hand. If you do, +2 Cards, then put 2 cards from your hand on top of your deck."
	cost = 2
	action = True
	reaction = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck

		#todo: test
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
						for each in self.roster:
							IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " discarded a " + self.player.playerHand[choice - 1] + ".\n")
						del self.player.playerHand[choice - 1]
						break
				for i in range(int(discard)):
					self.player.playerTurnTreasure += 1
				break

	def reactCard(self, reactor, roster, type):
		self.type = type
		self.reactor = reactor
		self.roster = roster
		if self.type == 'attack':
			while True:
				self.send_data(self.reactor.playerConn, "Would you like to reveal your " + self.cardPrint + "? (y)es or (n)o\n")
				choice = self.recv_data(self.reactor.playerConn, 1024)
				if choice.lower() not in ['y', 'n']:
					continue
				elif choice.lower() == 'y':
					for each in self.roster:
						self.send_data(each.playerConn, self.reactor.playerName + " reveals a " + self.cardPrint + "!\n")

					self.player.drawOneCard()
					self.player.drawOneCard()
					IntrigueCard.send_data(self, self.game, self.player.playerConn, "Place two cards back on your deck one at a time: ")

					i = 0
					while i < 2:
						x = 0
						for card in self.player.playerHand:
							x += 1
							IntrigueCard.send_data(self, self.game, self.player.playerConn, "[" + str(x) + "]" + card.cardPrint + " ",)
						IntrigueCard.send_data(self, self.game, self.player.playerConn, "\n")
						choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
						try: choice = int(choice) - 1
						except: continue
						if choice not in range(len(self.player.playerHand)): continue
						else:
							self.player.playerDeck.insert(0, self.player.playerHand[choice])
							del self.player.playerHand[choice]
							i += 1

					for each in self.roster:
						SeasideCard.send_data(self, self.game, each.playerConn, self.player.playerName + " placed 2 cards back on top of his deck.\n")
					break

				elif choice.lower() == 'n':
					break
		else:
			return
		return

class ShantyTownCard(IntrigueCard):
	cardEval = "ShantyTownCard"
	cardName = "Shanty Town"
	cardPrint = "\033[37mShanty Town\033[0m"
	description = "Reveal your hand. If you have no actions cards in hand, +2 Cards."
	cost = 3
	action = True

	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.roster = roster
		self.player.playerTurnActions += 2
		IntrigueCard.send_data(self, self.game, player.playerConn, self.player.playerName + " reveals " + ' '.join(i.cardPrint for i in self.player.playerHand) + ".\n")
		#if any(i.cardType == 'action' for i in self.player.playerHand):
		if any(i.action for i in self.player.playerHand):
			break
		else:
			self.player.drawOneCard()
			self.player.drawOneCard()
		return

class StewardCard(IntrigueCard):
	cardEval = "StewardCard"
	cardName = "Steward"
	cardPrint = "\033[37mSteward\033[0m"
	description = "Choose one: +2 cards, or +2 Coins, or trash 2 cards from your hand."
	cost = 3
	action = True

	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.roster = roster

		IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose one: +2 [c]ards, or +2 C[o]ins, or [t]rash 2 cards from your hand: \n")
		while True:
			choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
			if choice.lower() not in ['c', 'o', 't']:
				continue
			elif choice.lower() == 'c':
				self.player.drawOneCard()
				self.player.drawOneCard()
				break
			elif choice.lower() == 'o':
				self.player.playerTurnTreasure += 2
				break
			elif choice.lower() == 't':
				if len(self.player.playerHand) > 1:
					self.trash = 2
				else:
				    self.trash = len(self.player.playerHand)
				
				for i in self.trash
					IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose a card to trash:\n")
					while True:
						x = 0
						for each in self.current:
							x += 1
							IntrigueCard.send_data(self, "[" + str(x) + "]" + self.game, self.player.playerConn, each.cardPrint + " ",)
						IntrigueCard.send_data(self, self.game, self.player.playerConn, "\n")
						choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
						try:
							choice = int(choice) - 1
						except: continue
						if choice not in range(len(self.current)): continue
						else:
							for each in self.roster:
								IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " trashed a " + self.current[choice] + ".\n")

							del self.current[choice]
							if i > 1: 
								break
		return

#todo: fix target card selection
class SwindlerCard(IntrigueCard):
	
	
	cardEval = "SwindlerCard"
	cardName = "Swindler"
	cardPrint = "\033[1;31mSwindler\033[0m"
	description = "Each other player trashes the top card of his deck and gains a card of the same cost that you choose."
	cost = 3
	action = True
	attack = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		self.player.playerTurnTreasure += 2
		#todo: 
		self.options = []

		self.player.checkReactions('attack')
		for each in self.roster:
			if each != self.player and each.reactionImmunity == False and each.durationImmunity == False:

				self.trashed = False
				self.trash = []
				self.trashedcost = each.player.playerDeck[0].cost

				for player in self.roster:
					IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " trashes a " + each.player.playerDeck[0].cardPrint + ".\n")

				del each.player.playerDeck[0].cost

				IntrigueCard.send_data(self, self.game, self.player.playerConn, "Please choose a card costing exactly " + self.trashedcost + " for " + each.playerName & " to gain: ",)

				#todo: ask self which self.trashedcost card for each to gain
				while True:
					choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
					try: choice = int(choice) - 1
					except: continue
					if choice not in range(len(self.options)): continue
					else:
						#self.player.gainCard(self.trashedcost, 1, 'discard', 'any')

						for player in self.roster:
							if player.playerTurn: pass
							IntrigueCard.send_data(self, self.game, player.playerConn, each.player.playerName + " gains a " + card.cardPrint + ".\n")
						break

			else:
				if each.reactionImmunity == True:
					for player in self.roster:
						IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " was protected by reaction immunity.\n")
				elif each.durationImmunity == True:
					for player in self.roster:
						IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " was protected by duration immunity.\n")
				pass

class TorturerCard(IntrigueCard):
	cardEval = "TorturerCard"
	cardName = "Torturer"
	cardPrint = "\033[1;31mTorturer\033[0m"
	description = "Each other player chooses one: he discards 2 cards, or he gains a Curse card, putting it in his hand."
	cost = 5
	action = True
	attack = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck
		for i in range(3):
			self.player.drawOneCard()
		
		self.player.checkReactions('attack')
			for each in self.roster:
				if each != self.player and each.reactionImmunity == False and each.durationImmunity == False:

					self.trashed = False
					self.trash = []
					self.trashedcost = 0
					self.discarded = 0 
					
					if len(each.playerHand) < 2:
						if len(self.deck.curseCards) > 0:
							each.player.gainCard(0, 1, 'hand', 'curseCards')
							for each2 in self.roster:
								IntrigueCard.send_data(self, self.game, each2.playerConn, each.player.playerName + " gains a Curse into their hand.\n")
							else: return
					else:
						IntrigueCard.send_data(self, self.game, each.player.playerConn, "Choose one: [d]iscard two cards, or gain a [C]urse card into your hand.\n")
						while True:
							choice = IntrigueCard.recv_data(self, self.game, each.player.playerConn, 1024)
							if choice.lower() not in ['c', 'd']:
								continue
							elif choice.lower() == 'd':
								while self.discarded < 2:
									IntrigueCard.send_data(self, self.game, each.player.playerConn, "Please choose a card to discard:\n")
									each.printHandUpdate()
									choice = IntrigueCard.recv_data(self, self.game, each.playerConn, 1024)
									try:
										choice = int(choice) - 1
									except:
										continue
									if choice not in range(len(each.playerHand)): continue
									else:
										each.playerDiscard.append(each.playerHand[choice])
										del each.playerHand[choice]
										self.discarded += 1
										for player in self.roster:
											#todo: i think we should be displaying these?
											IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " discards a card.\n")

							elif choice.lower() == 'c':
								if len(self.deck.curseCards) > 0:
									each.player.gainCard(0, 1, 'hand', 'curseCards')
									for each2 in self.roster:
										IntrigueCard.send_data(self, self.game, each2.playerConn, each.player.playerName + " gains a Curse into their hand.\n")
								else: return

				else:
					if each.reactionImmunity == True:
						for player in self.roster:
							IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " was protected by reaction immunity.\n")
					elif each.durationImmunity == True:
						for player in self.roster:
							IntrigueCard.send_data(self, self.game, player.playerConn, each.playerName + " was protected by duration immunity.\n")
					pass

class TradingPost(IntrigueCard):
	cardEval = "TradingPostCard"
	cardName = "Trading Post"
	cardPrint = "\033[37mTrading Post\033[0m"
	description = "Trash 2 cards from your hand. If you do, gain a Silver card, put it into your hand."
	cost = 5
	action = True

	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.roster = roster
		self.trashed = 0 
		
		if len(self.player.playerHand) > 1:
			self.trash = 2
		else:
			self.trash = len(self.player.playerHand)

		for i in self.trash
			IntrigueCard.send_data(self, self.game, self.player.playerConn, "Choose a card to trash:\n")
			while True:
				x = 0
				for each in self.current:
					x += 1
					IntrigueCard.send_data(self, "[" + str(x) + "]" + self.game, self.player.playerConn, each.cardPrint + " ",)
				IntrigueCard.send_data(self, self.game, self.player.playerConn, "\n")
				choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
				try:
					choice = int(choice) - 1
				except: continue
				if choice not in range(len(self.current)): continue
				else:
					for each in self.roster:
						IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " trashed a " + self.current[choice] + ".\n")
				
					del self.current[choice]
					self.trashed += 1
						if i > 1: 
						break
		
		if len(self.deck.silverCards) > 0 and self.trashed == 2:
			self.player.gainCard(0, 1, 'hand', 'silverCards')
			for each in self.roster:
				IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " gains a Silver into his hand.\n")
		else: return

#todo: start
class TributeCard(TributeCard):
	cardEval = "TributeCard"
	cardName = "Tribute"
	cardPrint = "\033[37mTribute\033[0m"
	description = "The player to your left reveals and then discards the top 2 cards of his deck. For each different named card revealed, if it is an... Action card, +2 Actions; Treasure card, +2 Coins; Victory Card, +2 Cards."
	cost = 5
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.roster = roster
		self.deck = deck

#todo: do we have a gainCard check for EXACTLY +1? 
class UpgradeCard(IntrigueCard):
	cardEval = "UpgradeCard"
	cardName = "Upgrade"
	cardPrint = "\033[37mUpgrade\033[0m"
	description = "Trash a card form your hand. Gain a card costing exactly 1 Coin more than it."
	cost = 5
	action = True
	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.roster = roster
		self.player.drawOneCard()
		self.player.playerTurnActions += 1
		IntrigueCard.send_data(self, self.game, self.player.playerConn, "Please choose a card to trash: \n")
		while True:
			choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
			try: choice = int(choice) - 1
			except: continue
			if choice not in range(len(self.player.playerHand)): continue
			else:
				for each in self.roster:
					IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " trashes a " + choice.cardPrint + ".\n")

				del self.player.playerHand[choice]
				#todo: do we have a gainCard check for EXACTLY +1? 
				self.gain = self.player.gainCard(choice.cost + 1, 1, 'discard', 'any')

				for each in self.roster:
					IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " gains a " + self.gain.cardPrint + ".\n")
				break
		return

class WishingWellCard(IntrigueCard):
	cardEval = "WishingWellCard"
	cardName = "Wishing Well"
	cardPrint = "\033[37mWishing Well\033[0m"
	description = "Name a card. Reveal the top card of your deck. If it's the named card, put it into your hand."
	cost = 3
	action = True

	def __init__(self):
		self.game = game
		self.embargoed = False
		self.embargo = 0

	def playCard(self, player, roster, deck):
		self.player = player
		self.deck = deck
		self.roster = roster
		self.player.playerTurnActions += 1
		self.player.drawOneCard()

		self.type = type
		self.location = self.playerHand
		choices = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		nonkingdom = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c']
		kingdom = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

		IntrigueCard.send_data(self, self.game, self.player.playerConn, "Please name a card: \n")
		while True:
			choice = IntrigueCard.recv_data(self, self.game, self.player.playerConn, 1024)
			if choice.lower() not in choices: continue
			elif choice.lower() == 'o' or choice.lower == 'l': continue
			else:
				p = self.deck.provinceCards
				d = self.deck.duchyCards
				e = self.deck.estateCards
				g = self.deck.goldCards
				s = self.deck.silverCards
				c = self.deck.copperCards
				u = self.deck.curseCards
				choice = eval(choice.lower())
				x = 'card' + choice.lower()
				for each in self.roster:
					IntrigueCard.send_data(self, self.game, each.playerConn, self.player.playerName + " reveals a " + self.player.playerDeck[0].cardPrint + "... \n")
				if self.playerDeck[0].cardName = choice.cardName:
					for each in self.roster:
						IntrigueCard.send_data(self, self.game, each.playerConn, "...and puts it into his/her hand. \n")
					self.player.playerHand.append(self.player.playerDeck[0])
					del self.player.playerDeck[0]
				else:
					for each in self.roster:
						IntrigueCard.send_data(self, self.game, each.playerConn, "...and puts it back on top of his/her deck. \n")
				break

		return

