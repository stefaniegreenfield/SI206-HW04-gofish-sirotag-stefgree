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
