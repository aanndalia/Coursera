# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
FRAMES_PER_SECOND = 60
PADDLE_SPEED = 10
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    hor_mult = 1
    
    if direction == LEFT:
        hor_mult = -1

    hor_vel = random.randrange(120, 240)
    vert_vel = -1 * random.randrange(60, 180)
    
    ball_vel = [hor_mult * hor_vel/FRAMES_PER_SECOND, vert_vel/FRAMES_PER_SECOND]
    


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = 0
    paddle2_pos = 0
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel
 
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if (ball_pos[1] - BALL_RADIUS) <= 0 or (ball_pos[1] + BALL_RADIUS) >= (HEIGHT - 1):
        ball_vel[1] = -ball_vel[1]
    
    # check if ball is at left or right gutter
    if (ball_pos[0] - BALL_RADIUS) < PAD_WIDTH:
        if ((ball_pos[1] + BALL_RADIUS) > paddle1_pos) and ((ball_pos[1] - BALL_RADIUS) < (paddle1_pos + PAD_HEIGHT)):
            # if it hits paddle, bounce
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
            #print "velocity = (" + str(ball_vel[0]) + ", " + str(ball_vel[1]) + ")"
        else:
            # paddle misses in gutter
            score2 += 1
            spawn_ball(RIGHT)
    elif (ball_pos[0] + BALL_RADIUS) > (WIDTH - PAD_WIDTH - 1):
        if ((ball_pos[1] + BALL_RADIUS) > paddle2_pos) and ((ball_pos[1] - BALL_RADIUS) < (paddle2_pos + PAD_HEIGHT)):
            # if it hits paddle, bounce
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
            #print "velocity = (" + str(ball_vel[0]) + ", " + str(ball_vel[1]) + ")"
        else:
            # paddle misses in gutter
            score1 += 1
            spawn_ball(LEFT)
            
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "RED", "WHITE")
    
    # update paddle's vertical position, keep paddle on the screen
    if not((paddle1_pos + paddle1_vel) < 0 or ((paddle1_pos + PAD_HEIGHT + paddle1_vel) > (HEIGHT))):
        paddle1_pos += paddle1_vel
    if not((paddle2_pos + paddle2_vel) < 0 or ((paddle2_pos + PAD_HEIGHT + paddle2_vel) > (HEIGHT))):
        paddle2_pos += paddle2_vel
        
    # draw paddles
    paddle1_rect = [(0, paddle1_pos), (0, PAD_HEIGHT + paddle1_pos), (PAD_WIDTH, PAD_HEIGHT + paddle1_pos), (PAD_WIDTH, paddle1_pos)]
    paddle2_rect = [(WIDTH - PAD_WIDTH - 1, paddle2_pos), (WIDTH - PAD_WIDTH - 1, PAD_HEIGHT + paddle2_pos), (WIDTH, PAD_HEIGHT + paddle2_pos), (WIDTH, paddle2_pos)]
    c.draw_polygon(paddle1_rect, 1, "WHITE", "WHITE")
    c.draw_polygon(paddle2_rect, 1, "WHITE", "WHITE")
    
    # draw scores
    c.draw_text(str(score1), (200, 30), 30, 'White')
    c.draw_text(str(score2), (400, 30), 30, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -PADDLE_SPEED
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = PADDLE_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PADDLE_SPEED
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PADDLE_SPEED
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# create restart button
restart_button = frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
