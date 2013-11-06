# Dominion player class to create and manage player objects
from dominioncards import *
from dominiondeck import *

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

	def playTurn(self, actions, buys):
		self.playerTurnActions = actions
		self.playerTurnBuys = buys
		self.printPlayerHand()
		playtype = raw_input("\n\n What would you like to do: (P)lay, (B)uy, P(a)ss, (R)ead? ")
		if self.playerTurnActions == 0 and sum(p.cardType == 'treasure' for p in self.playerPlay) <= 0 or playtype.lower == 'a':
			return
		elif playtype.lower() == 'p':
			self.play()
		elif playtype.lower() == 'b':
			self.buy()
		elif playtype.lower() == 'r':
			self.deck.readCard(raw_input("  Which card would you like to read: (n)umber? "))
			os.system('clear')
			self.playTurn(self.playerTurnActions, self.playerTurnBuys)
		else:
			print " That is not an available choice...."
			self.playTurn(self.playerTurnActions, self.playerTurnBuys)

	def play(self):
		i = int(raw_input("  Which would you like to play: (n)umber? "))
		while True:
			if i > (len(self.playerHand)):
				i = int(raw_input("  Invalid choice, please pick a (n)umber: "))
			elif self.playerHand[i - 1].cardType == 'treasure':
				self.playerPlay.append(self.playerHand[i - 1])
				self.playerTurnTreasure += self.playerHand[i - 1].value
				del self.playerHand[i - 1]
				self.playerTurnActions = 0
				os.system('clear')
				break
			elif self.playerHand[i - 1].cardType == 'action':
				if self.playerTurnActions <= 0:
					raw_input("  You have no Actions left this turn, please (B)uy or (P)ass: ")
					break
				else:
					self.playerHand[i - 1].playCard(self.player, self.roster, self.deck)
					self.playerTurnActions -= 1
			elif self.playerHand[i - 1].cardType == 'victory':
				i = int(raw_input("  Invalid choice, you cannot play a Victory card. Please pick a (n)umber: "))

		self.playTurn(self.playerTurnActions, self.playerTurnBuys)

	def buy(self):
		i = raw_input("  Which card would you like to buy? ")
		while True:
			if i not in ['p', 'd', 'e', 'g', 's', 'c', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
				i = raw_input("  Invalid selection!  Which card would you like to buy? ")
			else:
				if i.lower() in ['p', 'd', 'e', 'g', 's', 'c']:
					p = self.deck.provinceCards
					d = self.deck.duchyCards
					e = self.deck.estateCards
					g = self.deck.goldCards
					s = self.deck.silverCards
					c = self.deck.copperCards
					i = eval(i)
					if i[0].cost > self.playerTurnTreasure:
						raw_input("  You do not have enough to buy this.")
						break
					else:	
						self.playerPlay.append(i[0])
						self.playerTurnTreasure -= i[0].cost
						del i[0]
						self.playerTurnBuys -= 1
						break
				elif int(i) in range(10):
					x = 'card' + str(int(i))
					if self.deck.actionCards[x][0].cost > self.playerTurnTreasure:
						raw_input(" You do not have enough to buy this.")
						break
					else:
						self.playerPlay.append(self.deck.actionCards[x][0])
						self.playerTurnTreasure -= self.deck.actionCards[x][0].cost
						del self.deck.actionCards[x][0]
						self.playerTurnBuys -= 1
						break
		if self.playerTurnBuys < 1:
			self.playerHandCleanup()
			self.drawHand()
			return
		else:
			self.playTurn(self.playerTurnActions, self.playerTurnBuys)

	def playerHandCleanup(self):
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

	def playerDiscardToDeck(self):
		x = len(self.playerDiscard)
		while x == len(self.playerDiscard) and x > 0:
			self.playerDeck.append(self.playerDiscard[0])
			del self.playerDiscard[0]
			x -= 1

	def playerDeckToDiscard(self):
		x = len(self.playerDeck)
		while x == len(self.playerDeck) and x > 0:
			self.playerDiscard.append(self.playerDeck[0])
			del self.playerDeck[0]
			x -= 1
	
	def printPlayerHand(self):
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

