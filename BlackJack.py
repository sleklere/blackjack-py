# Imports and Global Variables

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


# Classes

### Card ###
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


###  Deck  ###
class Deck():
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

    def __str__(self):
        deck_comp = ''
        for card in self.all_cards:
            deck_comp += '\n'+ card.__str__()
        return "The deck has: "+deck_comp

### Hand ###
class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        cards = []
        for i in self.cards:
            cards.append(str(i))
        return str(cards)


### Chips ###
class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet
        print(self.total)

    def lose_bet(self):
        self.total -= self.bet
        print(self.total)
        pass


### Functions ###

### Taking a bet ###
def take_bet(chips):
    x = True
    while x:
        try:
            bet = int(input('Choose your bet size: '))
            if bet <= chips.total:
                chips.bet += bet
                x = False
            else:
                print(f'Sorry you only have {chips.total} chips!')
                pass
        except ValueError:
            print("Sorry that's invalid, try again")


### Hit ###
def hit(deck,hand):
    hand.add_card(deck.deal_one())
    hand.adjust_for_ace()

### Hit or Stand? ###

def hit_or_stand(deck, hand):
    global playing
    while True:
        a = input("Hit or Stand?:  ")
        if a[0].lower() == "h":
            hit(deck, hand)
        elif a[0].lower() == "s":
            print("Player stands. Dealer´s Turn")
            playing = False
        else:
            print("Please enter Hit or Stand only")
            continue
        break


### Display Cards ###
def show_some(player, dealer):
    print(f"Dealer's hand (first card hidden): {dealer.cards[1]}")
    print(f"Player's hand: {player}")


def show_all(player, dealer):
    print(f"Player's value is: {player.value}")
    print(player)
    print(f"Dealer's value is: {dealer.value}")
    print(dealer)

### End of Game Scenarios ###
def player_busts(player,dealer,chips):
    print('Player bust!')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('Player wins!')
    chips.win_bet()


def dealer_busts(player,dealer,chips):
    print('Dealer bust!')
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print('Dealer wins!')
    chips.lose_bet()


def push(player, dealer):
    print("Dealer and player tie! PUSH")
    pass

###################
###################

# GAME #
a = True
player_chips = Chips()
while a:
    print('Welcome to Black Jack!')
    game_deck = Deck()
    game_deck.shuffle()
    playerhand = Hand()
    dealerhand = Hand()
    for x in range(2):
        hit(game_deck, playerhand)
        hit(game_deck, dealerhand)
    take_bet(player_chips)
    show_some(playerhand,dealerhand)
    while playing:
        hit_or_stand(game_deck,playerhand)
        show_some(playerhand, dealerhand)
        if playerhand.value > 21:
            player_busts(playerhand,dealerhand,player_chips)
            break
    if playerhand.value <= 21:
        while dealerhand.value < 17:
            hit(game_deck, dealerhand)
        show_all(playerhand, dealerhand)
        if dealerhand.value > 21:
            dealer_busts(playerhand,dealerhand,player_chips)
        elif dealerhand.value > playerhand.value:
            dealer_wins(playerhand,dealerhand,player_chips)
        elif playerhand.value > dealerhand.value:
            player_wins(playerhand,dealerhand,player_chips)
        else:
            push(playerhand,dealerhand)
    print(f'\n Player total chips are at: {player_chips.total}')
    if player_chips.total <= 0:
        print('Sorry, you ran out of chips! \nThanks for playing!')
        break
    new_game = input('Would you like to play again?(Y/N) ')
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing!')
        break
