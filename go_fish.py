import random

class Card(object):
	suit_names =  ["Diamonds","Clubs","Hearts","Spades"]
	rank_levels = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}

	def __init__(self, suit=0,rank=2):

		"""
		self.suit = self.suit_names[suit]
		if rank in self.faces: # self.rank handles printed representation
			self.rank = self.faces[rank]
		else:
			self.rank = rank
		self.rank_num = rank # To handle winning comparison
		"""
		self.suit = suit
		self.rank = rank

	def __str__(self):
		return "{} of {}".format(self.faces.get(self.rank, self.rank),self.suit_names[self.suit])

class Deck(object):
	def __init__(self): # Don't need any input to create a deck of cards
		# This working depends on Card class existing above
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card) # appends in a sorted order

	def __str__(self):
		total = []
		for card in self.cards:
			total.append(card.__str__())
		# shows up in whatever order the cards are in
		return "\n".join(total) # returns a multi-line string listing each card

	def pop_card(self, i=-1):
		# removes and returns a card from the Deck
		# default is the last card in the Deck
		return self.cards.pop(i) # this card is no longer in the deck -- taken off

	def shuffle(self):
		random.shuffle(self.cards)

	def replace_card(self, card):
		card_strs = [] # forming an empty list
		for c in self.cards: # each card in self.cards (the initial list)
			card_strs.append(c.__str__()) # appends the string that represents that card to the empty list
		if card.__str__() not in card_strs: # if the string representing this card is not in the list already
			self.cards.append(card) # append it to the list

	def sort_cards(self):
		# Basically, remake the deck in a sorted way
		# This is assuming you cannot have more than the normal 52 cars in a deck
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card)

	def deal(self,hands_num,cards_num):
		hands=[Hand([]) for x in range(hands_num)]

		if cards_num == -1:
			card_count = 0
			while(len(self.cards) != 0):
				hands[card_count % hands_num].add_card(self.pop_card())
				card_count += 1
			return hands

		for x in range(cards_num):
			for hand in hands:
				hand.add_card(self.pop_card())

		return hands
class Hand():
	def __init__(self, init_cards):
		self.cards=init_cards
		self.score = 0
	def add_card(self, card):
		card_strs = []
		for c in self.cards:
			card_strs.append(c.__str__())
		if card.__str__() not in card_strs:
			self.cards.append(card)
	def remove_card(self, card):
		card_strs = []
		for c in self.cards:
			card_strs.append(c.__str__())
		if card.__str__() in card_strs:
			card_index= card_strs.index(card.__str__())
			del self.cards[card_index]
			return card
	def draw(self, deck):
		self.add_card(deck.pop_card())

	def remove_pairs(self):
		pairs={}
		for x in self.cards:
			if x.rank in pairs:
				pairs[x.rank].append(x)
			else:
				pairs[x.rank]=[x]
		non_paired_cards = []
		for lst in pairs.values():
			pair_present = len(lst) % 2
			if pair_present == 1:
				non_paired_cards.append(lst[0])
		self.cards = non_paired_cards

deck=Deck()
deck.shuffle()
hands = deck.deal(2,7)
current_player=1
while True:

	for hand in hands:
		card_count = {}
		for card in hand.cards:
			if card.rank in card_count:
				card_count[card.rank] += 1
			else:
				card_count[card.rank] = 1
		for rank, freq in card_count.items():
			if freq == 4:
				for suit in range(4):
					hand.remove_card(Card(suit, rank))
				hand.score += 1

	# Check if game over
	if len(deck.cards) == 0 and len(hands[0].cards) == 0 and len(hands[1].cards) == 0:
		print("\n\nGame over!\n\n")
		if hands[0].score > hands[1].score:
			print("Player 1 wins.")
		elif hands[0].score < hands[1].score:
			print("Player 2 wins.")
		else:
			print("It's a tie.")
		print("Player 1: {}.  Player 2: {}.".format(hands[0].score, hands[1].score))
		break

	print("P1")
	for card in hands[0].cards:
		print(card)

	print()

	print("P2")
	for card in hands[1].cards:
		print(card)


	number= input('Player {}: Please choose a card rank you would like to ask the other player if they have (between 1-13): '.format(current_player))
	while not number.isdigit() or int(number) > 13 or int(number) < 1:
		print("Please choose a valid number between 1 and 13!!")
		number= input('Player {}: Please choose a card rank you would like to ask the other player if they have (between 1-13): '.format(current_player))

	# Only enforce asking for rank in hand if cards in hand
	if len(hands[current_player-1].cards) > 0:
		while int(number) not in [card.rank for card in hands[current_player-1].cards]:
			print("Please choose a card in your hand!!")
			number= input('Player {}: Please choose a card rank you would like to ask the other player if they have (between 1-13): '.format(current_player))

	cards_to_move = []
	being_asked = None
	if current_player == 1:
		being_asked = 1
	else:
		being_asked = 0
	for suit in range(4):
		test_card = Card(suit, int(number))
		remove_card = hands[being_asked].remove_card(test_card)
		if remove_card:
			cards_to_move.append(remove_card)

	if cards_to_move == []:
		print("\nGO FISH!!\n")
		draw = deck.pop_card()
		hands[current_player-1].add_card(draw)
		if draw.rank == int(number):
			print("You drew the rank you asked for.  Go again!\n")
			continue
	else:
		for each_card in cards_to_move:
			hands[current_player-1].add_card(each_card)



	if current_player == 1:
		current_player = 2
	else:
		current_player = 1
