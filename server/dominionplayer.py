# Dominion player class to create and manage player objects
from dominioncards import *
from dominiondeck import *
import types, time, errno

class Player(object):

	def __init__(self, roster):
		self.player = self
		self.playerHand = []
		self.playerName = ''
		self.playerDeck = []
		self.playerPlay = []
		self.playerDuration = []
		self.playerTurnActions = 0
		self.playerTurnBuys = 0
		self.playerTurnTreasure = 0
		self.playerActionsPlayed = 0
		self.deck = ''
		self.playerDiscard = []
		self.roster = roster
		self.playerHasDuration = False
		self.playerSetAside = []
		self.playerTreasurePlayed = False
		self.game = ''		
		self.reactionImmunity = False
		self.durationImmunity = False
		self.totalVictory = 0
		self.playerConn = ''
		self.playerTurn = False
		self.islandMat = []
		self.pirateMat = 0
		self.nativeMat = []

	def send_data (self, client, data):
		message = str(data)
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

	def recv_data (self, client, length):
		try:
			self.playerConn.settimeout(600)
			data = client.recv(length)
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

	def drawToPlayer(self, hand):
		if hand == 0:
			for i in range(3):
				self.playerDeck.append(EstateCard)
			for i in range(7):
				self.playerDeck.append(CopperCard)
			random.shuffle(self.playerDeck)
		elif hand > 0:
			pass

	def drawHand(self):
		for i in range(5):
			if len(self.playerDeck) > 0:
				self.playerHand.append(self.playerDeck[0])
				del self.playerDeck[0]
			else:
				self.playerDiscardToDeck()
				self.playerHand.append(self.playerDeck[0])
				del self.playerDeck[0]

	def drawOneCard(self):
		self.playerDiscardToDeck()
		self.playerHand.append(self.playerDeck[0])
		del self.playerDeck[0]

	def gainCard(self, cost, number, location, type):
		self.cost = cost
		self.number = number
		self.location = location
		self.type = type
		if self.location == 'discard':
			self.location = self.playerDiscard
		elif self.location == 'hand':
			self.location = self.playerHand
		elif self.location == 'deck':
			self.location = self.playerDeck
		choices = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		nonkingdom = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c']
		kingdom = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		while True:
			for i in range(self.number):
				if self.type == 'treasure':
					self.send_data(self.playerConn, "Please select a Treasure card that costs up to $" + str(self.cost) + ":\n")
					choice = self.recv_data(self.playerConn, 1024)
					if choice.lower() not in ['l', 'g', 's', 'c']:
						self.send_data(self.playerConn, "Invalid selection, please choose a Treasure card!\n")
						continue
				elif self.type == 'kingdom':
					self.send_data(self.playerConn, "Please select a Kingdom card that costs up to $" + str(self.cost) + ":\n")
					choice = self.recv_data(self.playerConn, 1024)
					if choice.lower() not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
						self.send_data(self.playerConn, "Invalid selection, please choose a Kingdom card!\n")
						continue
				elif self.type == 'victory':
					self.send_data(self.playerConn, "Please select a Victory card that costs up to $" + str(self.cost) + ":\n")
					choice = self.recv_data(self.playerConn, 1024)
					if choice.lower() not in ['o', 'p', 'd', 'e']:
						self.send_data(self.playerConn, "Invalid Selection, please choose a Victory card!\n")
						continue
				elif self.type == 'any':
					self.send_data(self.playerConn, "Please select a card that costs up to $" + str(self.cost) + ":\n")
					choice = self.recv_data(self.playerConn, 1024)
					if choice.lower() not in choices:
						self.send_data(self.playerConn, "Invalid selection, please choose another card!\n")
				elif self.type not in ['treasure', 'kingdom', 'victory', 'any']:
					if len(eval(self.type)) == 0:
						break
					else:
						self.player.playerDiscard.append(eval(self.type)[0])
						del eval(self.type)[0]
						break
				if choice.lower() in nonkingdom:
					if choice.lower() == 'o' or choice.lower == 'l':
						self.send_data(self.playerConn, "Invalid selection, please choose another card!\n")
						continue
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
							self.send_data(self.playerConn, "Invalid selection, please choose another card!\n")
							continue
						else:
							self.location.append(choice[0])
							for each in self.roster:
								self.send_data(each.playerConn, self.playerName + " has gained a " + choice[0].cardPrint + ".\n")
							del choice[0]
							break
				elif choice.lower() in kingdom:
					x = 'card' + choice.lower()
					if self.deck.kingdomCards[x][0].cost > cost:
						self.send_data(self.playerConn, "Invalid selection, please choose another card!\n")
						continue
					else:
						self.location.append(self.deck.kingdomCards[x][0])
						for each in self.roster:
								self.send_data(each.playerConn, self.playerName + " has gained a " + self.deck.kingdomCards[x][0].cardPrint + ".\n")
						del self.deck.kingdomCards[x][0]
						break
			break
		return self.location[-1]

	def playTurn(self):
		if len(self.game.playerRost) == 1: return
		self.checkPlayerDeck()
		self.checkSetAside()
		if self.playerTurnActions == 1 and self.playerTurnBuys == 1 and self.playerTurnTreasure == 0:
			self.checkDurationEffects()
			self.actionPhase()
			self.buyPhase()
			self.cleanUpPhase()
			return
		else:
			self.playerTurnActions = 1
			self.playerTurnBuys = 1
			self.playerTurnTreasure = 0
			self.playerTreasurePlayed = False
			self.checkDurationEffects()
			self.actionPhase()
			self.buyPhase()
			self.cleanUpPhase()
			return
		return

	def actionPhase(self):
		actionPhaseCount = 1
		self.printRosterHand(self.roster)
		while True:
			if self.playerTurnActions == 0 or self.playerTreasurePlayed == True:
				return
			else:
				self.printPlayerHand()
				self.send_data(self.playerConn, "\nWhat would you like to do: (P)lay, (B)uy, P(a)ss, (R)ead? \n")
				while True:
					response = str(self.recv_data(self.playerConn, 1024))
					if response not in ['p', 'b', 'a', 'r']:
						self.send_data(self.playerConn, "Sorry, that is not an available choice.\n")
					elif response == 'p':
						self.playCard()
						actionPhaseCount += 1
						break
					elif response == 'b':
						self.send_data(self.playerConn, "Which card would you like to buy ((x) to cancel)?\n")
						choice = str(self.recv_data(self.playerConn, 1024))
						if choice.lower() == 'x': break
						while True:
							if choice.lower() not in ['o', 'p', 'd', 'e', 'u', 'g', 's', 'c', 't', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
								self.send_data(self.playerConn,"Invalid selection!\n")
							elif choice.lower() in ['o', 'l', 't']:
									continue
							elif choice.lower() in ['p', 'd', 'e', 'u', 'l', 'g', 's', 'c', 'o']:
								p = self.deck.provinceCards
								d = self.deck.duchyCards
								e = self.deck.estateCards
								g = self.deck.goldCards
								s = self.deck.silverCards
								c = self.deck.copperCards
								u = self.deck.curseCards
								i = eval(i.lower())
								if i[0].cost > self.playerTurnTreasure:
									self.send_data(self.playerConn, " You do not have enough to buy this.\n" )
									break
								else:
									self.playerPlay.append(i[0])
									self.playerTurnTreasure -= i[0].cost
									for each in self.roster:
										self.send_data(each.playerConn, self.playerName + " has bought a " + i[0].cardPrint + ".\n")
									del i[0]
									self.playerTurnBuys -= 1
									return
							elif int(choice) in range(10):
								x = 'card' + str(choice)
								if self.deck.kingdomCards[x][0].cost > self.playerTurnTreasure:
									self.send_data(self.playerConn, " You do not have enough to buy this.\n")
									break
							else:
								self.playerPlay.append(self.deck.kingdomCards[x][0])
								self.playerTurnTreasure -= self.deck.kingdomCards[x][0].cost
								for each in self.roster:
									self.send_data(each.playerConn, self.playerName + " has bought a " + self.deck.kingdomCards[x][0].cardPrint + ".\n")
								del self.deck.kingdomCards[x][0]
								self.playerTurnBuys -= 1
								return
							break
						self.buyPhase()
						return
					elif response.lower() == 'a':
						return
					elif response.lower() == 'r':
						self.send_data(self.playerConn, "Which card would you like to read: (n)umber?\n")
						cardToRead = str(self.recv_data(self.playerConn, 1024))
						self.deck.readCard(cardToRead, self.playerConn)
						break
				continue
		return

	def playCard(self):
		if len(self.playerHand) == 0: return
		while True:
			self.send_data(self.playerConn, "Which card would you like to play: (n)umber?\n")
			i = str(self.recv_data(self.playerConn, 1024))
			try:
				i = int(i)
			except:
				continue
			if i > len(self.playerHand):
				continue
			elif self.playerHand[i - 1].treasure == True:
				self.playerPlay.append(self.playerHand[i - 1])
				self.playerTurnTreasure += self.playerHand[i - 1].value
				for each in self.roster:
					self.send_data(each.playerConn, self.playerName + " has played a " + self.playerHand[i - 1].cardPrint + ".\n")
				del self.playerHand[i - 1]
				self.playerTreasurePlayed = True
				return
			elif self.playerHand[i - 1].action == True:
				if self.playerTurnActions <= 0:
					self.send_data(self.playerConn, "You have no Actions left this turn, please (b)uy or p(a)ss.\n")
					self.buyPhase()
					return
				else:
					if self.playerHand[i - 1].duration:
                                                self.playerDuration.append(self.playerHand[i - 1])
                                                for each in self.roster:
                                                        self.send_data(each.playerConn, self.playerName + " has played a " + self.playerHand[i - 1].cardPrint + ".\n")
                                                del self.playerHand[i - 1]
                                                self.playerTurnActions -= 1
                                                self.playerActionsPlayed += 1
                                                self.playerDuration[-1].playCard(self.player, self.roster, self.deck)
                                                return
					else:
						self.playerPlay.append(self.playerHand[i - 1])
						for each in self.roster:
							self.send_data(each.playerConn, self.playerName + " has played a " + self.playerHand[i - 1].cardPrint + ".\n")
						del self.playerHand[i - 1]
						self.playerTurnActions -= 1
						self.playerActionsPlayed += 1
						self.playerPlay[-1].playCard(self.player, self.roster, self.deck)
						return
			elif self.playerHand[i - 1].victory == True and self.playerHand[i - 1].action == False:
				self.send_data(self.playerConn, "Invalid choice, you cannot play this card.\n")
		return

	def buyPhase(self):
		if self.playerTurnBuys == 0:
			return
		else:
			while True:
				if self.playerTurnBuys == 0: return
				self.printPlayerHand()
				self.send_data(self.playerConn, "\nWhat would you like to do: (P)lay, (B)uy, P(a)ss, (R)ead?\n")
				choice = str(self.recv_data(self.playerConn, 1024))
				if choice.lower() not in ['p', 'b', 'a', 'r']:
					continue
				elif choice.lower() == 'p':
					while True:
						self.send_data(self.playerConn, "Which card would you like to play: (n)umber?\n")
						i = self.recv_data(self.playerConn, 2014)
						try:
							i = int(i)
						except:
							continue
						if i > len(self.playerHand) or i <= 0:
							continue
						elif self.playerHand[i - 1].treasure != True and self.playerHand[i - 1].action != False or self.playerHand[i - 1].treasure != True:
							self.send_data(self.playerConn, "You are in the buy phase, please play a Treasure.\n")
							time.sleep(2)
							break
						else:
							self.playerPlay.append(self.playerHand[i - 1])
							self.playerTurnTreasure += self.playerHand[i - 1].value
							for each in self.roster:
								self.send_data(each.playerConn, self.playerName + " has played a " + self.playerHand[i - 1].cardPrint + ".\n")
							del self.playerHand[i - 1]
							break
				elif choice.lower() == 'b':
					while True:
						self.send_data(self.playerConn, "Which card would you like to buy ((x) to cancel)?\n")
						i = self.recv_data(self.playerConn, 2014)
						if i.lower() == 'x': break
						if i.lower() not in ['o', 'p', 'd', 'e', 'u', 'g', 's', 'c', 't', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
							self.send_data(self.playerConn,  " Invalid selection!\n")
						elif i.lower() in ['o', 'l', 't']:
							continue
						elif i.lower() in ['p', 'd', 'e', 'u', 'l', 'g', 's', 'c', 'o']:
							p = self.deck.provinceCards
							d = self.deck.duchyCards
							e = self.deck.estateCards
							g = self.deck.goldCards
							s = self.deck.silverCards
							c = self.deck.copperCards
							u = self.deck.curseCards	
							i = eval(i.lower())
							if i[0].cost > self.playerTurnTreasure:
								self.send_data(self.playerConn, " You do not have enough to buy this.\n")
								continue
							else:
								self.playerPlay.append(i[0])
								self.playerTurnTreasure -= i[0].cost
								for each in self.roster:
									self.send_data(each.playerConn, self.playerName + " has bought a " + i[0].cardPrint + ".\n")
								del i[0]
								self.playerTurnBuys -= 1
								break
						elif int(i) in range(10):
							x = 'card' + i
							if self.deck.kingdomCards[x][0].cost > self.playerTurnTreasure:
								self.send_data(self.playerConn, " You do not have enough to buy this.\n")
								continue
							else:
								self.playerPlay.append(self.deck.kingdomCards[x][0])
								self.playerTurnTreasure -= self.deck.kingdomCards[x][0].cost
								for each in self.roster:
									self.send_data(each.playerConn, self.playerName + " has bought a " + self.deck.kingdomCards[x][0].cardPrint + ".\n")
								del self.deck.kingdomCards[x][0]
								self.playerTurnBuys -= 1
								break
						break
					continue
				elif choice.lower() == 'a':
					return
				elif choice.lower() == 'r':
					self.send_data(self.playerConn, "Which card would you like to read: (n)umber?\n")
					cardToRead = str(self.recv_data(self.playerConn, 1024))
					self.deck.readCard(cardToRead, self.playerConn)
					break
		return

	def cleanUpPhase(self):
		self.playerActionsPlayed = 0
		self.playerTurnActions = 1
		self.playerTurnBuys = 1
		self.playerTurnTreasure = 0
		self.playerTreasurePlayed = False
		x = len(self.playerPlay)
		y = len(self.playerHand)
		while x == len(self.playerPlay) and x > 0:
			self.playerDiscard.append(self.playerPlay[0])
			del self.playerPlay[0]
			x -= 1
		while y == len(self.playerHand) and y > 0:
			self.playerDiscard.append(self.playerHand[0])
			del self.playerHand[0]
			y -= 1
		time.sleep(1)
		self.drawHand()
		self.checkWin()
		return

	def passTurn(self):
		return

	def checkDurationEffects(self):
		if self.playerHasDuration:
			while len(self.playerDuration) > 0:
				self.playerDuration[0].playDuration(self.player, self.roster, self.deck)
				self.playerDiscard.append(self.playerDuration[0])
				del self.playerDuration[0]
			self.playerHasDuration = False
			return				
		else:
			return

	def checkSetAside(self):
		if len(self.playerSetAside) > 0:
			pass
		else:
			return

	def checkReactions(self, type):
		self.type = type
		if self.type == 'attack':
			for each in self.roster:
				if each != self:
					for card in each.playerHand:
						if card.reaction == True:
							card.reactCard(each, self.roster, 'attack')
						else:
							pass
					for card in each.playerDuration:
                                                if card.reaction == True:
                                                        card.reactCard(each, self.roster, 'attack')
                                                else:
                                                        pass
		elif self.type == 'gain':
			for each in self.roster:
				if any(i.reaction == True for i in each.playerHand):
					each.playerHand[i].reactCard('gain')


	def checkPlayerDeck(self):
		if len(self.playerDeck) == 0:
			self.playerDiscardToDeck()
		else:
			return

	def playerDiscardToDeck(self):
		if len(self.playerDeck) == 0:
			x = len(self.playerDiscard)
			while x == len(self.playerDiscard) and x > 0:
				self.playerDeck.append(self.playerDiscard[0])
				del self.playerDiscard[0]
				x -= 1
			random.shuffle(self.playerDeck)

		else: return
	def playerDeckToDiscard(self):
		x = len(self.playerDeck)
		while x == len(self.playerDeck) and x > 0:
			self.playerDiscard.append(self.playerDeck[0])
			del self.playerDeck[0]
			x -= 1
	
	def printPlayerHand(self):
		self.rosterFake = []
		self.rosterFake.append(self)
		self.printRosterHand(self.rosterFake)

	def printHandUpdate(self):
		i = 1
		for card in self.playerHand:
			self.send_data(self.playerConn, "[" + str(i) + "]" + card.cardPrint + "  \033[0m",)
			i += 1
		self.send_data(self.playerConn, "\n")

	def printRosterHand(self, roster):
		self.printPlayerTurn(roster)
		self.deck.printDeckCards(roster)
		self.printPlayerCount(roster)
		self.printTurnCount(roster)
		for user in roster:
			i = 1
			self.send_data(user.playerConn, "\nCurrent Hand (" + user.playerName + "):\n")
			for card in user.playerHand:
				self.send_data(user.playerConn, "[" + str(i) + "]" + card.cardPrint + "  \033[0m",)
				i += 1
			self.send_data(user.playerConn, "\n")

	def printPlayerTurn(self, roster):
		self.temproster = roster
		for user in self.temproster:
			self.send_data(user.playerConn, "CLRSCRN_FULL\n")
			for each in self.roster:
				if each.playerTurn == True:
					self.send_data(user.playerConn, "\033[32m" + each.playerName + "\033[0m ",)
				else:
					self.send_data(user.playerConn, "\033[37m" + each.playerName + "\033[0m ",)
			self.send_data(user.playerConn, "\n")

	def printPlayerReveal(self):
		for user in self.roster:
			i = 1
			self.send_data(user.playerConn, "\nCurrent hand (" + user.playerName + "):\n")
			for card in user.playerHand:
				self.send_data(user.playerConn, "[" + str(i) + "]" + card.cardPrint + "  \033[0m",)
				i += 1
			self.send_data(user.playerConn, "\n")

	def printPlayerCount(self, roster):
		for user in roster:
			self.send_data(user.playerConn, "\n\nDeck [",)
			for i in range(len(user.playerDeck)):
				self.send_data(user.playerConn, "|",)
			self.send_data(user.playerConn, "] -- Discard [",)
			for i in range(len(user.playerDiscard)):
				self.send_data(user.playerConn, "|",)
			self.send_data(user.playerConn, "]\n\n")

	def printTurnCount(self, roster):
		for user in roster:
			self.send_data(user.playerConn, "Actions: " + str(user.playerTurnActions) + "    Buys ($" + str(user.playerTurnTreasure) + "): " + str(user.playerTurnBuys) + "\n")

	def checkWin(self):
		self.zeroTally = 0
		if len(self.deck.duchyCards) == 0: self.zeroTally += 1
		if len(self.deck.estateCards) == 0: self.zeroTally += 1
		if len(self.deck.curseCards) == 0: self.zeroTally += 1
		if len(self.deck.goldCards) == 0: self.zeroTally += 1
		if len(self.deck.silverCards) == 0: self.zeroTally += 1
		if len(self.deck.copperCards) == 0: self.zeroTally += 1
		for i in range(10):
			if len(self.deck.kingdomCards['card' + str(i)]) == 0:
				self.zeroTally += 1
			else:
				pass
		if len(self.deck.provinceCards) == 0:
			self.endGame()
			return
		elif self.zeroTally == 3:
			self.endGame()
			return
		else:
			self.passTurn()
			return
	def endGame(self):
		for each in self.roster:
			self.send_data(each.playerConn, "GAME OVER! The scores are: ")
		for each in self.roster:
			each.playerDeckToDiscard()
			for i in range(len(each.playerHand)):
				each.playerDiscard.append(each.playerHand[0])
				del each.playerHand[0]
			for i in each.playerDiscard:
				if i.cardName == 'Gardens': each.totalVictory += (1 * (len(each.playerDiscard) // 10))
				else: each.totalVictory += i.victoryPoints
			for player in self.roster:
				self.send_data(player.playerConn, "  " + each.playerName + ": " + str(each.totalVictory) + " ",)
		for player in self.roster:
			self.send_data(player.playerConn, "\n")
		time.sleep(10)
		self.game.playerTurn = 'gameover'
		return
