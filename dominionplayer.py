# Dominion player class to create and manage player objects
from dominioncards import *
from dominiondeck import *
import types

class Player(object):

	def __init__(self, roster):
		self.player = self
		self.playerHand = []
		self.playerName = ''
		self.playerDeck = []
		self.playerPlay = []
		self.playerTurnActions = 0
		self.playerTurnBuys = 0
		self.playerTurnTreasure = 0
		self.playerRoom = ''
		self.deck = ''
		self.playerDiscard = []
		self.roster = roster
		self.playerHasDuration = False
		self.playerSetAside = []
		self.playerTreasurePlayed = False
		self.game = ''		
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
		if len(player.playerDeck) == 0:
			self.playerDiscardToDeck()
		else:
			self.playerHand.append(self.playerDeck[0])
			del self.playerDeck[0]

	def gainCard(self, cost, number):
		self.cost = cost
		self.number = number
		choices = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		nonkingdom = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c']
		kingdom = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		while True:
			for i in range(number):
				choice = raw_input("    Please select a card that costs up to $" + str(self.cost) + ": ")
				if choice.lower() not in choices:
					print "    Invalid selection, please choose another card!"
				elif choice.lower() in nonkingdom:
					if choice.lower() == 'o' or choice.lower == 'l':
						print "    Invalid selection, please choose another card!"
					else:
						p = self.deck.provinceCards
						d = self.deck.duchyCards
						e = self.deck.estateCards
						g = self.deck.goldCards
						s = self.deck.silverCards
						c = self.deck.copperCards
						u = self.deck.copperCards
						choice = eval(choice.lower())
						if choice.cost > cost:
							print "    Invalid selection, please choose another card!"
						else:
							self.playerDiscard.append(choice[0])
							del choice[0]
							break
				elif choice.lower() in kingdom:
					x = 'card' + choice.lower()
					if self.deck.kingdomCards[x][0].cost > cost:
						print "    Invalid selection, please choose another card!"
					else:
						self.playerDiscard.append(self.deck.kingdomCards[x][0])
						del self.deck.kingdomCards[x][0]
						break

	def playTurn(self):
		self.checkPlayerDeck()
		self.checkDurationEffects()
		self.checkSetAside()
		if self.playerTurnActions == 1 and self.playerTurnBuys == 1 and self.playerTurnTreasure == 0:
			self.actionPhase()
		else:
			self.playerTurnActions = 1
			self.playerTurnBuys = 1
			self.playerTurnTreasure = 0
			self.playerTreasurePlayed = False
			self.actionPhase()
		
	def actionPhase(self):
		actionPhaseCount = 1
		while True:
			if self.playerTurnActions == 0 or self.playerTreasurePlayed == True:
				self.buyPhase()
			else:
				self.printPlayerHand()
				actionType = raw_input("\n\n What would you like to do: (P)lay, (B)uy, P(a)ss, (R)ead? ")
				if actionType.lower() not in ['p', 'b', 'a', 'r']:
					continue
				elif actionType.lower() == 'p':
					self.playCard()
					actionPhaseCount += 1
					continue
				elif actionType.lower() == 'b':
					self.buyPhase()
					break
				elif actionType.lower() == 'a':
					self.cleanUpPhase()
				elif actionType.lower() == 'r':
					self.deck.readCard(raw_input("  Which card would you like to read: (n)umber? "))
					continue

	def playCard(self):
		while True:
			i = raw_input("  Which card would you like to play: (n)umber? ")
			try:
				i = int(i)
			except:
				continue
			if i > len(self.playerHand):
				continue
			elif self.playerHand[i - 1].treasure == True:
				self.playerPlay.append(self.playerHand[i - 1])
				self.playerTurnTreasure += self.playerHand[i - 1].value
				del self.playerHand[i - 1]
				self.playerTurnActions = 0
				self.playerTreasurePlayed = True
				self.buyPhase()
				break
			elif self.playerHand[i - 1].action == True:
				if self.playerTurnActions <= 0:
					raw_input("  You have no Actions left this turn, please (B)uy or (P)ass: ")
					self.buyPhase()
				else:
					self.playerHand[i - 1].playCard(self.player, self.roster, self.deck)
					self.playerTurnActions -= 1
					self.playerDiscard.append(self.playerHand[i - 1])
					del self.playerHand[i - 1]
					break
			elif self.playerHand[i - 1].victory == True and self.playerHand[i - 1].action == False:
				print "  Invalid choice, you cannot play a Victory card."
		return

	def buyPhase(self):
		if self.playerTurnBuys == 0:
			self.cleanUpPhase()
		else:
			while True:
				self.printPlayerHand()
				actionType = raw_input("\n\n What would you like to do: (P)lay, (B)uy, P(a)ss, (R)ead? ")
				if actionType.lower() not in ['p', 'b', 'a', 'r']:
					continue
				elif actionType.lower() == 'p':
					while True:
						i = raw_input("  Which card would you like to play: (n)umber? ")
						try:
							i = int(i)
						except:
							continue
						if i > len(self.playerHand):
							continue
						elif self.playerHand[i - 1].treasure != True and self.playerHand[i - 1].action != False or self.playerHand[i - 1].treasure != True:
							raw_input("  You are in the buy phase, please play a Treasure. ")
							continue
						else:
							self.playerPlay.append(self.playerHand[i - 1])
							self.playerTurnTreasure += self.playerHand[i - 1].value
							del self.playerHand[i - 1]
							break
				elif actionType.lower() == 'b':
					while True:
						i = raw_input("  Which card would you like to buy? ")
						if i.lower() not in ['o', 'p', 'd', 'e', 'u', 'g', 's', 'c', 't', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
							print "  Invalid selection!"
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
								raw_input("  You do not have enough to buy this." )
								continue
							else:
								self.playerPlay.append(i[0])
								self.playerTurnTreasure -= i[0].cost
								del i[0]
								self.playerTurnBuys -= 1
								break
						elif int(i) in range(10):
							x = 'card' + i
							if self.deck.kingdomCards[x][0].cost > self.playerTurnTreasure:
								raw_input("  You do not have enough to buy this." )
								continue
							else:
								self.playerPlay.append(self.deck.kingdomCards[x][0])
								self.playerTurnTreasure -= self.deck.kingdomCards[x][0].cost
								del self.deck.kingdomCards[x][0]
								self.playerTurnBuys -= 1
								break
						break
					break
				elif actionType.lower() == 'a':
					self.cleanUpPhase()
				elif actionType.lower() == 'r':
					self.deck.readCard(raw_input("  Which card would you like to read: (n)umber? "))
					break
			if self.playerTurnBuys < 1:
				self.cleanUpPhase()
			else:
				self.buyPhase()

	def cleanUpPhase(self):
		self.playerTurnActions = 1
		self.playerTurnBuys = 1
		self.playerTurnTreasure = 0
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
		self.drawHand()
		self.passTurn()

	def passTurn(self):
		self.game.playerTurn += 1
		self.game.playLoop()

	def checkDurationEffects(self):
		if self.playerHasDuration == True:
			pass
		else:
			return

	def checkSetAside(self):
		if len(self.playerSetAside) > 0:
			pass
		else:
			return

	def checkPlayerDeck(self):
		if len(self.playerDeck) == 0:
			self.playerDiscardToDeck()
		else:
			return

	def playerDiscardToDeck(self):
		x = len(self.playerDiscard)
		while x == len(self.playerDiscard) and x > 0:
			self.playerDeck.append(self.playerDiscard[0])
			del self.playerDiscard[0]
			x -= 1
		random.shuffle(self.playerDeck)

	def playerDeckToDiscard(self):
		x = len(self.playerDeck)
		while x == len(self.playerDeck) and x > 0:
			self.playerDiscard.append(self.playerDeck[0])
			del self.playerDeck[0]
			x -= 1
	
	def printPlayerHand(self):
		os.system('clear')
		self.deck.printDeckCards()
		self.printPlayerCount()
		self.printTurnCount()
		print "\n  Current Hand (" + self.playerName + "):\n ",
		for card in self.playerHand:
			print card.cardColor + card.cardName + " \033[0m",

	def printPlayerReveal(self):
		print "\n Current Hand (" + self.playerName + "):\n",
		for card in self.playerHand:
			print card.cardColor + card.cardName + "\033[0m",

	def printPlayerCount(self):
		sys.stdout.write("\n\n  Deck [")
		for i in range(len(self.playerDeck)):
			sys.stdout.write("|")
		sys.stdout.write("] -- Discard [")
		for i in range(len(self.playerDiscard)):
			sys.stdout.write("|")
		sys.stdout.write("]\n\n")

	def printTurnCount(self):
		print "  Actions: " + str(self.playerTurnActions) + "    Buys ($" + str(self.playerTurnTreasure) + "): " + str(self.playerTurnBuys)

