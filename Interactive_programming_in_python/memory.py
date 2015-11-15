# implementation of card game - Memory

import simplegui
import random

deck = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]
HEIGHT = 100
WIDTH = 800
NUM_CARDS = 16
CARD_WIDTH = WIDTH / NUM_CARDS
prev1 = -1
prev2 = -1

# helper function to initialize globals
def new_game():
    global state
    global exposed
    global turns
    state = 0
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    turns = 0
    random.shuffle(deck)
     
# define event handlers
def mouseclick(pos):
    global state
    global exposed
    global prev1
    global prev2
    global turns
    clicked = pos[0] / CARD_WIDTH
    print clicked
    
    if exposed[clicked] == False:
        if state == 0:
            turns += 1
            state = 1
        elif state == 1:
            state = 2
        else:
            if deck[prev1] != deck[prev2]:
                exposed[prev1] = False
                exposed[prev2] = False
                
            turns += 1
            state = 1
        
        exposed[clicked] = True
        prev2 = prev1
        prev1 = clicked
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(NUM_CARDS):
        if exposed[i] == True:
            left_offset = 18 + CARD_WIDTH * i
            canvas.draw_text(str(deck[i]), (left_offset, HEIGHT/ 2 + 10), 30, 'White')
        else:
            left_offset = CARD_WIDTH * i
            canvas.draw_polygon([[left_offset, 0], [left_offset, HEIGHT], [left_offset + CARD_WIDTH, HEIGHT], [left_offset + CARD_WIDTH, 0]], 2, 'White', 'Green')
        
        label.set_text("Turns = " + str(turns))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric