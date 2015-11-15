# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
dealer_outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def __str__(self):
        # return a string representation of a hand
        handStr = ""
        for card in self.cards:
            handStr += (" " + str(card))
        
        return "Hand contains " + handStr
        

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        aces_present = False
        handValue = 0
        for card in self.cards:
            if card.get_rank() == 'A':
                aces_present = True
            handValue += VALUES[card.get_rank()]
                
        if aces_present == False:
            return handValue
        else:
            if (handValue + 10) <= 21:
                return handValue + 10
            else:
                return handValue
            
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        ind = 0
        for card in self.cards:
            x = pos[0] + ind*CARD_SIZE[0]
            y = pos[1]
            #y = pos[1] + ind*CARD_SIZE[1]
            card.draw(canvas, (x,y))
            ind += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))
                

    def shuffle(self):
        # shuffle the deck 
       random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        deckStr = "Deck contains "
        for card in self.cards:
            deckStr += (str(card) + " ")
            
        return deckStr



#define event handlers for buttons
def deal():
    global outcome, in_play

    # your code goes here
    global deck, player_hand, dealer_hand, score
    
    if in_play == True:
        score -= 1
        outcome = "You have quit and lost"
        in_play = False
        
    else:
        deck = Deck()
        deck.shuffle()
        
        player_hand = Hand()
        dealer_hand = Hand()
        
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        
        print "Deal"
        print "Player hand:", str(player_hand)
        print "Dealer hand:", str(dealer_hand)
        print
        
        outcome = ""
        in_play = True

def hit():
    global outcome, in_play
    global deck, player_hand, dealer_hand, score
    
    if in_play:
        # if the hand is in play, hit the player
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
              
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            print "You have busted"
            outcome = "You have busted and lost"
            score -= 1
            in_play = False
        
        print "Hit"    
        print "Player hand:", str(player_hand)
        print "Dealer hand:", str(dealer_hand)
        print
               
def stand():
    global outcome, in_play
    global deck, player_hand, dealer_hand, score
    
    if in_play:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more        
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            
        #if dealer_hand.get_value() > 21:
        #    print "Dealer has busted"
        #    outcome = "Dealer has busted so you win"
     
        # assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            print "You are busted"
            outcome = "You have busted and lost"
        elif dealer_hand.get_value() > 21:
            print "Dealer has busted"
            score += 1
            outcome = "Dealer has busted so you win"
        elif player_hand.get_value() > dealer_hand.get_value():
            print "Player wins"
            score += 1
            outcome = "You win."
        else:
            print "Dealer wins"
            score -= 1
            outcome = "Dealer wins."
            
        in_play = False
        
        print "Stand"
        print "Player hand:", str(player_hand)
        print "Dealer hand:", str(dealer_hand)
        print
    

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand, dealer_hand
    
    canvas.draw_text('Blackjack', (230, 40), 40, 'White')
    canvas.draw_text('Dealer', (100, 80), 20, 'White')
    canvas.draw_text('Player', (100, 100 + 2*CARD_SIZE[1] - 20), 20, 'White')
    canvas.draw_text('Score: ' + str(score), (500, 20), 20, 'White')
    
    dealer_hand.draw(canvas, (100, 100))
    player_hand.draw(canvas, (100, 100 + 2*CARD_SIZE[1]))
    
    canvas.draw_text(outcome, (200, 80), 20, 'White')
        
        
    if in_play == True:        
        canvas.draw_text("Hit or Stand?", (200, 100 + 2*CARD_SIZE[1] - 20), 20, 'White')
        src_center = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        dest_center = (100 + CARD_BACK_CENTER[0], 100 + CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, src_center, CARD_BACK_SIZE, dest_center, CARD_BACK_SIZE)
    else:
        canvas.draw_text("New Deal?", (200, 100 + 2*CARD_SIZE[1] - 20), 20, 'White')
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric