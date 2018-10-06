# Compass Game - PyGame Zero
# This is licensed under GNU GENERAL PUBLIC LICENSE Version 3
# See : https://github.com/penguintutor/compassgame 

import math
import random

WIDTH = 800
HEIGHT = 600


# Number of actions to complete before moving up to the next level
# Default = 30 (change for debugging)
NEXT_LEVEL_ACTIONS = 30

# File holding high score
high_score_filename = 'compassgame_score.dat'

#Background
BACKGROUND_IMG_FILES = ['compassgame_background_01','compassgame_background_02'] 


#Images for player in each direction - does not include final digit which is the image number
#All must have 4 images ending with 1 to 4, except for jump and duck which only ends with 1
#For this game jump is used, but is represented as reading a map
PLAYER_IMG_DIRECTION = {'down':'compassgame_person_01_towards_', 'up':'compassgame_person_01_away_', 'left':'compassgame_person_01_left_', 'right':'compassgame_person_01_right_', 'duck':'compassgame_person_01_duck_',  'jump':'compassgame_person_01_map_'  }

# Obstacle images
# This has twice as many trees as rocks, although chosen at random most likely more trees than rocks
OBSTACLE_IMG_FILES = ['compassgame_obstacle_01_tree_1', 'compassgame_obstacle_01_tree_2', 'compassgame_obstacle_01_tree_1', 'compassgame_obstacle_01_tree_2', 'compassgame_obstacle_01_rock_1', 'compassgame_obstacle_01_rock_2']

# Direction that player is facing
direction = 'down'
#walking position of player (number from 1 to 4 represent position of feet)
player_step_count = 1

#Player character
player = Actor(PLAYER_IMG_DIRECTION[direction]+str(player_step_count), (WIDTH/2,HEIGHT/2))

#Obstacles - these are actors, but stationary ones
obstacles = []

# Positions to place obstacles Tuples: (x,y)
obstacle_positions = [(200,200), (400, 400), (500,500), (80,120), (700, 150), (750,540), (200,550), (60,320), (730, 290), (390,170), (420,500) ]


#Rectangles for compass points for collision detection to ensure player is in correct position
box_size = 50 
north_box = Rect((0, 0), (WIDTH, box_size))
east_box = Rect((WIDTH-box_size, 0), (WIDTH, HEIGHT))
south_box = Rect((0, HEIGHT-box_size), (WIDTH, HEIGHT))
west_box = Rect((0, 0), (box_size, HEIGHT))

# Where the player needs to move to eg. 'north', 'south' or 'duck'
# If '' then game not started - if 'end' then end of game
game_state = ''
# Difficulty level increment as we start each level (start at 1)
game_level = 1

# Pauses game 
#  if 0 then game is not paused 
#  if positive then pause gamea and decrement until 0 
#  if -1 then user has paused the game and wait until continue
game_pause = 0
# Message to display when paused / level up etc.
game_message = ""
# Track number of actions caught within this level - used to determine decay and next level
level_actions_complete = 0


# Number of seconds when the timer starts 
timer_start = 10.9
# This is the actual timer we use
timer = 0

# Current score for this game
score = 0
# Highest Score previously attained
high_score = 0

#Dictionary with messages to show to user for action to carry out
action_text = {'north':'Go north', 'south':'Go south', 
    'east':'Go east', 'west':'Go west',
    'duck':'Quick duck!', 'jump':'Check the map'}


def draw():
    global high_score
    high_score = get_high_score()
    screen.blit(get_background_img(), (0,0))
    # If game not running then give instruction
    if (game_state == ''):
        # Display message on screen
        screen.draw.text("Press map or duck button to start", fontsize=60, center=(WIDTH/2,HEIGHT/2), shadow=(1,1), color=(255,255,255), scolor="#202020")
    elif (game_state == 'end'):
        screen.draw.text("Game Over\nScore "+str(score)+"\nHigh score "+str(high_score)+"\nPress map or duck button to start", fontsize=60, center=(WIDTH/2,HEIGHT/2), shadow=(1,1), color=(255,255,255), scolor="#202020")
    else:
        screen.draw.text('Time: '+str(math.floor(timer)), fontsize=60, center=(100,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        screen.draw.text('Score '+str(score), fontsize=60, center=(WIDTH-130,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        screen.draw.text(action_text[game_state], fontsize=60, center=(WIDTH/2,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        player.draw()
        # Draw obstacles
        for i in range (0,len(obstacles)):
            obstacles[i].draw()
        
        # If want a message over the top of the screen then add here (eg. pause / level up)
        if (game_message != ""):
            screen.draw.text(game_message, fontsize=60, center=(WIDTH/2,HEIGHT/2), shadow=(1,1), color=(255,255,255), scolor="#202020")


    
def update(time_interval):
    # Need to be able to update following global variables
    global direction, game_state, game_level, game_pause, game_message, level_actions_complete, score, timer
       
    if (game_pause > 0):
        game_pause -= 1
        # If reach end of the pause then clear any message
        if (game_pause == 0):
            game_message = ''
        return
    elif (game_pause < 0):
        # duck or jump to unpause (if want to use p button would need to add delay to prevent rapid toggling)
        if (keyboard.space or keyboard.lshift or keyboard.rshift or keyboard.lctrl):
            game_pause = 0
        else:
            return
    
    
    # If status is not running then we give option to start or quit
    if (game_state == '' or game_state == 'end'):
        # Display instructions (in draw() rather than here)
        # If jump / duck then start game
        if (keyboard.space or keyboard.lshift or keyboard.rshift or keyboard.lctrl):
            game_state = get_next_move()
            # Reset timer
            timer = timer_start
            if (score > high_score) :
                set_high_score(score)
            # Reset score
            score = 0
            level_actions_complete = 0
            set_level(0)
        # If escape then quit the game
        if (keyboard.escape):
            quit()
        return
    

    # Update timer with difference from previous
    timer -= time_interval
    # Check to see if timer has run out
    if (timer < 0.9): 
        game_state = 'end'
        return
        
    
    # Check for direction keys pressed
    # Can have multiple pressed in which case we move in all the directions
    # The last one in the order below is set as the direction to determine the 
    # image to use 
    new_direction = ''
    
    ## Actions based on keyboard press
    # Check for pause button first
    if (keyboard.p):
        game_pause = -1
    
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
            move_actor(new_direction)
        if (keyboard.down):
            new_direction = 'down'
            move_actor(new_direction)
        if (keyboard.left) :
            new_direction = 'left'
            move_actor(new_direction)
        if (keyboard.right) :
            new_direction = 'right'
            move_actor(new_direction)

    # Also check for jump / duck being deselected as we need to move back to a normal position
    if ((direction == 'jump' or direction == 'duck') and new_direction == ''):
        # move to default down direction
        new_direction = 'down'
    # If new direction is not "" then we have a move button pressed
    # so set appropriate image
    if (new_direction != ""):
        # Set image based on new_direction
        set_actor_image (direction, new_direction)
        direction = new_direction
        
    # Has player hit an obstacle?
    if (hit_obstacle()):
        game_state = 'end'
        return 

    # Determine if player has reached where they should be
    if (reach_target(game_state)):
        # Add some score
        score += 1
        level_actions_complete += 1
        # choose new action
        game_state = get_next_move()
        # Update timer - subtracting timer decrement for each point scored
        timer = timer_start + 1.5 - (timer_start * (level_actions_complete/ (level_actions_complete + 10)))
        
        # Check to see if the user has scored enough to move up a level
        if (level_actions_complete >= NEXT_LEVEL_ACTIONS):
            timer = timer_start
            game_level += 1
            set_level(game_level)
            level_actions_complete = 0
            # Move player back to center for level up
            player.x = WIDTH/2
            player.y = HEIGHT/2
            new_direction = 'down'
            set_actor_image (direction, new_direction)
            direction = new_direction
            game_message = "Level Up!\n"+str(game_level)
            game_pause = 60
            

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
    elif (target_pos == direction):
        return True
    # If none of above met then False
    return False

def move_actor(direction, distance = 5):
    if (direction == 'up'):
        player.y -= distance
    if (direction == 'right'):
        player.x += distance
    if (direction == 'down'):
        player.y += distance
    if (direction == 'left'):
        player.x -= distance
    
    # Check not moved past the edge of the screen
    if (player.y <= 30):
        player.y = 30
    if (player.x <= 12):
        player.x = 12
    if (player.y >= HEIGHT - 30):
        player.y = HEIGHT - 30
    if (player.x >= WIDTH - 12):
        player.x = WIDTH - 12
        


# Sets appropriate image 
# If direction change then change to appropriate initial image for that direction
# If same direction then cycle through images for that direction
def set_actor_image (direction, new_direction):
    global player, player_step_count
    
    step_delay = 5

    # Check for duck and jump as don't increment digit & image - we just have one duck / jump image
    if (direction == new_direction and (direction == 'duck' or direction == 'jump')):
        return

    if (direction != new_direction) :
        player_step_count = 0
    else :
        player_step_count += 1
        
    if (player_step_count >= 4 * step_delay):
        player_step_count = 0
        
    player_step_position = math.floor(player_step_count / step_delay) +1
    player.image = PLAYER_IMG_DIRECTION[new_direction]+str(player_step_position)
    
    
#Get next direction / jump / duck 
def get_next_move():
    move_choices = ['north', 'south', 'east', 'west', 'jump', 'duck']
    return random.choice(move_choices)
    
    
# Set new level by setting correct background and adding appropriate obstacles to list
def set_level(level_number):
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
        obstacles.append(Actor(random.choice(OBSTACLE_IMG_FILES), obstacle_positions[i]))
    
    
def hit_obstacle():
    for i in range (0,len(obstacles)):
        if player.colliderect(obstacles[i]):
            return True
    return False
    
# Gets background image from list (if not enough then return last one)
def get_background_img():
    # If level higher than num images return last entry
    if game_level > len (BACKGROUND_IMG_FILES):
        return BACKGROUND_IMG_FILES[-1]
    else:
        return BACKGROUND_IMG_FILES[game_level - 1]
    
# Reads high score from file and returns as a number
def get_high_score():
    # Open file if it already exists
    try:
        file = open(high_score_filename, 'r')
        entry = file.readline()
        file.close()
        high_score = int(entry)
        file_exists = True
    except:
        # If either doesn't exist or is corrupt
        high_score = 0       
    return high_score
    
    
# Writes a high score to the file
def set_high_score(new_score):
    global high_score
    high_score = new_score
    try:
        with open(high_score_filename, 'w') as file:
            file.write(str(high_score))
    except:
            # Unable to write to file - warn to console
            print ("Unable to write to file "+high_score_filename+" high scores will not be saved")