# Compass Game - PyGame Zero
# This is licensed under GNU GENERAL PUBLIC LICENSE Version 3
# See : hhttp://www.penguintutor.com/projects/compass-game

# If running on a computer that doesn't include . in the Python Search Path
# Includes Raspbian on x86
import sys
sys.path.append('.')

import math
import random

from playeractor import PlayerActor
from gameplay import GamePlay
from timer import Timer
from highscore import HighScore

WIDTH = 800
HEIGHT = 600
TITLE = "Compass Game"

# Filename format - uses python format to add appropriate values
# Variables are: theme (eg. boy/girl), character_number (00=default), direction (down=default), seq_num / step count (01 = default)
#Images for player in each direction - does not include final digit which is the image number
#All must have 4 images ending with 1 to 4, except for jump and duck which only ends with 1
# 'down', 'up', 'left', 'right', 'jump', 'duck'
#For this game jump is used, but is represented as reading a map
PLAYER_IMG_FORMAT = "person_{}_{:02d}_{}_{:02d}"
# Same background can be applied for each level or one per level - if only some have backgrounds then the last one is used for all subsequent levels 
# background 00 is used by the menu
# eg. person_default_01_forward_01
BACKGROUND_IMG_FORMAT = "background_{:02d}"
# The number of levels that have background images - if 0 then uses default of 00)
BACKGROUND_NUM_IMGS = 2
# Obstacles - if prefer one to be more common then needs to be duplicated (eg. 2 x identical images more likely than 1)
OBSTACLE_IMG_FORMAT = "obstacle_{:02d}"
# The number of obstacles - starts at 01
OBSTACLE_NUM_IMGS = 6


# File holding high score
HIGH_SCORE_FILENAME = 'compassgame_score.dat'

#Dictionary with messages to show to user for action to carry out
action_text = {'north':'Go north', 'south':'Go south', 
    'east':'Go east', 'west':'Go west',
    'duck':'Quick duck!', 'jump':'Check the map'}


# allows different character looks
theme = "default"
theme_num = 0



# Track Status etc
game_status = GamePlay(action_text)

# Track high score
high_score = HighScore(HIGH_SCORE_FILENAME)

# Player - baseed on PlayActor which inherits from Actor
player = PlayerActor(theme, theme_num, PLAYER_IMG_FORMAT, WIDTH,HEIGHT)


#Obstacles - these are actors, but stationary ones - default positions
obstacles = []
# Positions to place obstacles Tuples: (x,y)
obstacle_positions = [(200,200), (400, 400), (500,500), (80,120), (700, 150), (750,540), (200,550), (60,320), (730, 290), (390,170), (420,500) ]


#Rectangles for compass points for collision detection to ensure player is in correct position
box_size = 50 
north_box = Rect((0, 0), (WIDTH, box_size))
east_box = Rect((WIDTH-box_size, 0), (WIDTH, HEIGHT))
south_box = Rect((0, HEIGHT-box_size), (WIDTH, HEIGHT))
west_box = Rect((0, 0), (box_size, HEIGHT))



def draw():
    screen.blit(get_background_img(game_status.getLevel()), (0,0))
    if (game_status.isGameOver() or game_status.isShowScore()):
        screen.draw.text("Game Over\nScore "+str(game_status.getScore())+"\nHigh score "+str(high_score.getHighScore())+"\nPress map or duck button to start", fontsize=60, center=(WIDTH/2,HEIGHT/2), shadow=(1,1), color=(89,6,13), scolor="#A0A0A0")
    # If game not running then give instruction
    elif (not game_status.isGameRunning()):
        # Display message on screen
        screen.draw.text("Press map or duck button to start", fontsize=60, center=(WIDTH/2,HEIGHT/2), shadow=(1,1), color=(0,112,37), scolor="#A0A0A0")
    else:
        screen.draw.text('Time: '+str(game_status.getTimeRemaining()), fontsize=60, center=(100,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        screen.draw.text('Score '+str(game_status.getScore()), fontsize=60, center=(WIDTH-130,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        # Only show state if not timer paused
        if (not game_status.isTimerPause()):
            screen.draw.text(game_status.getStateString(), fontsize=60, center=(WIDTH/2,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        player.draw()
        # Draw obstacles
        for i in range (0,len(obstacles)):
            obstacles[i].draw()
        
        # If want a message over the top of the screen then add here (eg. pause / level up)
        if (game_status.getGameMessage() != ""):
            screen.draw.text(game_status.getGameMessage(), fontsize=60, center=(WIDTH/2,HEIGHT/2), shadow=(1,1), color=(255,255,255), scolor="#202020")


def update():
    # Check for pause status if so only look for key press
    if (game_status.isUserPause()):
        # duck or jump to unpause (if want to use p button would need to add delay to prevent rapid toggling)
        if (keyboard.space or keyboard.lshift or keyboard.rshift or keyboard.lctrl):
            game_status.setUserPause(False)
        else:
            return
            
    # Check for timer pause - if so return until expired
    if (game_status.isTimerPause()):
        return
    
    # Reset message after timer finished
    game_status.setGameMessage("")
    
    if (game_status.isGameOver()):
        if (game_status.getScore() > high_score.getHighScore()) :
                high_score.setHighScore(game_status.getScore())
        game_status.setShowScore()
        
    
    # If status is not running then we give option to start or quit
    if (game_status.isNewGame() or game_status.isTitleScreen() or game_status.isScoreShown()):
        # Display instructions (in draw() rather than here)
        # If jump / duck then start game
        if (keyboard.space or keyboard.lshift or keyboard.rshift or keyboard.lctrl):
            
            # Reset player including score
            player.reset()
            game_status.startNewGame()
            # Reset number of obstacles etc.
            set_level_display(game_status.getLevel())
        # If escape then quit the game
        if (keyboard.escape):
            quit()
        return
    

    if (game_status.isGameRunning and game_status.getTimeRemaining() < 1):
        game_status.setGameOver()
        return
        
    
    # Check for direction keys pressed
    # Can have multiple pressed in which case we move in all the directions
    # The last one in the order below is set as the direction to determine the 
    # image to use 
    new_direction = ''
    
    ## Actions based on keyboard press
    # Check for pause button first
    if (keyboard.p):
        game_status.setUserPause()
    
    # Duck or Jump - don't move character, but change image
    # Allow two different keys for both these
    if (keyboard.space or keyboard.lshift):
        new_direction = 'duck'
    elif (keyboard.rshift or keyboard.lctrl):
        new_direction = 'jump'
        # Only handle direction buttons if duck or jump have not been selected (prevent ducking constantly and moving)
    else:
        if (keyboard.up):
            new_direction = 'up'
            player.moveActor(new_direction)
        if (keyboard.down):
            new_direction = 'down'
            player.moveActor(new_direction)
        if (keyboard.left) :
            new_direction = 'left'
            player.moveActor(new_direction)
        if (keyboard.right) :
            new_direction = 'right'
            player.moveActor(new_direction)
            

    # Also check for jump / duck being deselected as we need to move back to a normal position
    if (player.isJumpDuck() and new_direction == ''):
        # move to default down direction
        player.updImage('down')
    # If new direction is not "" then we have a move button pressed
    # so set appropriate image
    if (new_direction != ""):
        # Set image based on new_direction
        player.updImage(new_direction)
        
    # Has player hit an obstacle?
    if (hit_obstacle()):
        game_status.setGameOver()
        return 

    # Determine if player has reached where they should be
    if (reach_target(game_status.getCurrentMove())):
        current_level = game_status.getLevel()
        new_level = game_status.scorePoint()
        
        # If level changed when adding point
        if (current_level != new_level):
            #Move player back to center for level up
            player.setPosition(WIDTH/2,HEIGHT/2)
            player.setDirection('down')
            game_status.setGameMessage("Level Up!\n"+str(new_level))
            game_status.startTimerPause()
            set_level_display(new_level)
            

# Determine if the player has reached target
# Can be either certain position on screen (Rects defined earlier) or duck / map(jump)
def reach_target(target_pos):
    if (target_pos == 'north'):
        if (player.colliderect(north_box)): return True
        else: return False
    elif (target_pos == 'south'):
        if (player.colliderect(south_box)): return True
        else: return False
    elif (target_pos == 'east'):
        if (player.colliderect(east_box)): return True
        else: return False    
    elif (target_pos == 'west'):
        if (player.colliderect(west_box)): return True
        else: return False
    # These are just based on the direction of the player (ie. are they ducking / reading the map (jump))
    elif (target_pos == player.getDirection()):
        return True
    # If none of above met then False
    return False


       
# Set new level by setting correct background and adding appropriate obstacles to list
def set_level_display(level_number):
    global obstacles

    # Delete current obstacles
    obstacles = []    
    
    # Start adding obstacles from level 3
    if (level_number < 3):
        return
        
    # Max we can have is the number of obstacle_positions
    for i in range (0,len(obstacle_positions)):
        # quit when we have reached correct number for this level (equal to the level number -2 so first level with obstacles is level 3 with 2)
        if (i > (level_number - 2)):
            break
        obstacles.append(Actor(OBSTACLE_IMG_FORMAT.format(random.randint(0,OBSTACLE_NUM_IMGS)), obstacle_positions[i]))
    
    
def hit_obstacle():
    for i in range (0,len(obstacles)):
        if player.colliderect(obstacles[i]):
            return True
    return False
    
# Gets background image (filename - excluding ext) based on format (if not enough then return last one)
def get_background_img(game_level):
    # If level higher than num images return last entry
    if game_level > BACKGROUND_NUM_IMGS:
        game_level = BACKGROUND_NUM_IMGS
    return BACKGROUND_IMG_FORMAT.format(game_level)
    

    
    
