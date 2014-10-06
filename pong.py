# This will be a clone of pong

import time
import math
import pygame

# init game window
pygame.init()
size = (1500, 750)
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 55)
bigfont = pygame.font.SysFont("monospace", 200)
pygame.display.set_caption("Game!")

# Load assets
win = pygame.image.load('win.jpg')
lose = pygame.image.load('lose.jpg')

# Constants
FPS = 60
PE = .002 # How much does where the ball hit effect y velocity

# Color Var Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Boundaries
TOP = 0
BOTTOM = 750
LEFT = 0
RIGHT = 1500

# Initial Ball Coords
BX_START = 725
BY_START = 325

# Initial Object Speeds
P_SPEED = 5
P_2_SPEED = 5
BALL_VELOCITY = -5
BALL_Y_VELOCITY = 0

# Control vars
done = False
up = False
down = False
# winner
p1_won = False
p2_won = False
# Hackery
hcount = 0

#coordinates
##p1 paddle
p1x = 50
p1y = 275 
p1w = 50
p1h = 200 

##p2 paddle
p2x = 1400
p2y = 275
p2w = 50
p2h = 200

##ball
bx = BX_START
by = BY_START
bw = 50
bh = 50

# Scores
p1_score = 0
p2_score = 0

#init clock
clock = pygame.time.Clock()

#--Main Loop--
while not done:

    #--Get Events--
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # Close if user clicks close
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up = True
            if event.key == pygame.K_DOWN:
                down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up = False
            if event.key == pygame.K_DOWN:
                down = False       

    #--Game Logic--
    # Keep Player paddle in bounds
    if up and p1y > TOP:
        p1y -= P_SPEED    
    elif down and p1y < (BOTTOM - p1h):
        p1y += P_SPEED

    # Detect Points
    if bx < (LEFT - bw):
        bx = BX_START
        by = BY_START
        BALL_Y_VELOCITY = 0
        p2_score += 1
    elif bx > RIGHT:
        bx = BX_START
        by = BY_START
        BALL_Y_VELOCITY = 0
        p1_score += 1
 
    # Detect Collision with either paddle
    if (by + bh) > p1y and by < (p1y + p1h) and bx == (p1x + p1w):
        BALL_VELOCITY = -1 * BALL_VELOCITY
        BALL_Y_VELOCITY = PE * (((by - p1y) - (p1h / 2)) ** 2)
    elif (by + bh) > p2y and by < (p2y + p2h) and bx == (p2x - bw):
        BALL_VELOCITY = -1 * BALL_VELOCITY
        BALL_Y_VELOCITY = PE * (((by - p2y) - (p2h / 2)) ** 2)
   
    # Detect Boundry Collision
    if by < TOP or by > (BOTTOM - bh):
        BALL_Y_VELOCITY = -1 * BALL_Y_VELOCITY
        
    # Move the Ball  
    by += BALL_Y_VELOCITY
    bx += BALL_VELOCITY

    # Move Player 2
    if (by < p2y) and p2y > TOP:
        p2y -= P_2_SPEED
    elif (by > p2y) and p2y < (BOTTOM - p2h):
        p2y += P_2_SPEED

    # Detect Endgame
    if p1_score == 3:
        p1_won = True
    elif p2_score == 3:
        p2_won = True

    #--Print console messages--
    print ("P1 x:%d y:%d | P2 x:%d y:%d | BALL x:%d y:%d xv:%d yv:%d" 
           % (p1x, p1y, p2x, p2y, bx, by, BALL_VELOCITY, BALL_Y_VELOCITY))

    #--Draw Screen--
    # Get scores ready to print
    print_p1s = myfont.render(str(p1_score), 1, WHITE)
    print_p2s = myfont.render(str(p2_score), 1, WHITE)

    screen.fill(BLACK) # Clear screen

    # Draw midline
    pygame.draw.line(screen, WHITE, [725, 0], [725, 750])
 
    # Print Scores
    screen.blit(print_p1s, (683, 5))
    screen.blit(print_p2s, (735, 5))

    # Draw characters
    pygame.draw.rect(screen, WHITE, [p1x, p1y, p1w, p1h]) # player 1 paddle
    pygame.draw.rect(screen, WHITE, [p2x, p2y, p2w, p2h]) # player 2 paddle
    pygame.draw.rect(screen, WHITE, [bx, by, bw, bh]) # ball

    # Paint endgame
    if p1_won:
        # Display End Game
        screen.fill(BLACK)
        screen.blit(win, (0, 0))
        win_txt = bigfont.render("YOU WIN!", 1, WHITE)
        score_txt = bigfont.render("%d - %d" % (p1_score, p2_score), 1, WHITE)
        screen.blit(win_txt, (630, 200))
        screen.blit(score_txt, (750, 400))
        # Hackery, above doesn't display first pass
        hcount += 1
        if hcount == 2:
            time.sleep(3)
            # Rest the game
            hcount = 0
            p2_score = 0
            p1_score = 0
            p1_won = False
            p2_won = False


    elif p2_won:
        # Display End Game
        screen.fill(BLACK)
        screen.blit(lose, (750, 0))
        lose_txt = bigfont.render("YOU LOSE!", 1, WHITE)
        score_txt = bigfont.render("%d - %d" % (p1_score, p2_score), 1, WHITE)
        screen.blit(lose_txt, (50, 200))
        screen.blit(score_txt, (50, 400))
        # Hackery, above doesn't display first pass
        hcount += 1
        if hcount == 2:
            time.sleep(3)
            # Rest the game
            hcount = 0
            p2_score = 0
            p1_score = 0
            p1_won = False
            p2_won = False



    pygame.display.flip()
    
    # Set framerate
    clock.tick(FPS)

pygame.quit()

