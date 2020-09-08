
from IPython.display import clear_output

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
             'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card():
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck():

	def __init__(self):
		self.deck = []  # start with an empty list

		for suit in suits:
		    for rank in ranks:
		        card = Card(suit,rank)
		        self.deck.append(card)

	def __str__(self):
		for card in self.deck:
		    return f'{card.rank} of {card.suit}'

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		dealt_card = self.deck.pop()
		return dealt_card

class Hand():

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        if card.rank != 'Ace':
            self.value = self.value + values[f'{card.rank}']
        else:
            self.aces += 1
            self.value = self.value + values[f'{card.rank}']
   
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
                    
    def __str__(self):
        cards = ''
        for card in self.cards:
            cards += f'{card.rank} of {card.suit}\n'
        return cards
       
class Chips():
    
    def __init__(self,total):
        self.total = total # This can be set to a default value or supplied by a user input
        
    def win_bet(self,bet):
        self.total += bet

    def lose_bet(self,bet):
        self.total -= bet

def take_bet(player):
    while True:
        try: 
            bet = int(input('What bet would you like to place? '))
        except:
            print('Please enter an integer')
            continue
        else:
            if bet>player.total:
                print('That exceeds your total number of chips. Please choose again.')
                continue
            else: 
                return bet
                break

def hit(deck,hand):
    deck.shuffle()
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    while True:
        try: 
            choice = input('\nWould you like to hit or stand? Enter H for hit or S for stand: ')
        except:
            print('Please enter H for hit or S for stand.')
            continue
        else:
            if choice.upper() == 'H':
                hit(deck,hand)
                break
            elif choice.upper()=='S':   
                playing = False
                break

def show_some(player_hand,dealer_hand):
    print("\nPlayer's Hand: ")
    print(player_hand)
    print("\nDealer's Hand:\n<Hidden Card>")
    for card in dealer_hand.cards[1:]:
        print(card)
    
def show_all(player_hand,dealer_hand):
    print("\nPlayer's Hand: ")    
    print(player_hand)
    print(f'Score: {player_hand.value}')
    print("\nDealer's Hand:")
    print(dealer_hand)
    print(f'Score: {dealer_hand.value}')


def player_busts(player_hand,dealer_hand):
    print("You've gone bust! Dealer wins!")
    player_chips.lose_bet(player_bet)
    print(f"You lost your bet, you now have {player_chips.total}")


def player_wins(player_hand,dealer_hand):
    if player_hand.value <= 21 and dealer_hand.value <= 21 and player_hand.value > dealer_hand.value:
        print("Player wins!")
        player_chips.win_bet(player_bet)
        print(f"You won your bet, you now have {player_chips.total}")       

        
def dealer_busts(player_hand,dealer_hand):
    if dealer_hand.value > 21:
        print("Dealer is bust! Player wins!")
        player_chips.win_bet(player_bet)
        print(f"You won your bet, you now have {player_chips.total}")    


def dealer_wins(player_hand,dealer_hand):
    if player_hand.value <= 21 and dealer_hand.value <= 21 and player_hand.value < dealer_hand.value:
        print("Dealer wins!")
        player_chips.lose_bet(player_bet)
        print(f"You lost your bet, you now have {player_chips.total}")

    
def push():
    if player_hand.value == dealer_hand.value:
        print('Push! Noone wins!')
        print(f"You still have {player_chips.total}")



player_chips = Chips(500)

while True:
        try:
            begin_input = input("Welcome to BlackJack! Would you like to play? Enter Y for Yes or N for No: ")
        except:
            print("Please enter Y for Yes or N for No: ") 
            continue
        else:
            if begin_input.upper() == "Y":
                game_on = True
                break
            else:
                game_on = False
                break
                
    

# Create & shuffle the deck, deal two cards to each player          
game_loop = True
while game_loop:
        clear_output()
        game_deck = Deck()
        game_deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(game_deck.deal())
        dealer_hand.add_card(game_deck.deal())
        player_hand.add_card(game_deck.deal())
        dealer_hand.add_card(game_deck.deal())

                # Set up the Player's chips

        print(f"You have {player_chips.total} chips to play with")

                # Prompt the Player for their bet
        player_bet = take_bet(player_chips)

                # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)

            #while playing:  # recall this variable from our hit_or_stand function
        playing = True
        while playing:
                hit_or_stand(game_deck,player_hand)
                if player_hand.value > 21:
                    clear_output()
                    show_all(player_hand,dealer_hand)
                    player_busts(player_hand,dealer_hand)
                    playing = False
                else:
                    clear_output()
                    show_some(player_hand,dealer_hand)
                    continue

        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(game_deck,dealer_hand)        
                 # If Player hasn't busted, play Dealer's hand until Dealer reaches 17

               # Show all cards  

            clear_output()
            show_all(player_hand,dealer_hand)



                 # Run different winning scenarios   
            dealer_busts(player_hand,dealer_hand)
            player_wins(player_hand,dealer_hand)
            dealer_wins(player_hand,dealer_hand)
            push()

        while True:
                try:
                    carry_on = input("Would you like to play again? Enter Y for Yes or N for No: ")
                except:
                    print("Please enter Y for Yes or N for No: ") 
                    continue
                else:
                    if carry_on.upper() == "Y":
                            game_loop = True
                            break
                    else:
                            game_loop = False
                            break

#testing branch changes
#testing editing this file locally

#test 2 trying to push changes to github
   
