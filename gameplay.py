import random
from timer import Timer

# Status is tracked as a number, but to make the code readable constants are used
# Note the actual number isn't important, but the order is as may use > or <
# Those with # * in the comments are used to determine higher state
STATUS_PRE_GAME = 0             # * Used to delimit before game starts
STATUS_TITLE = 1                # Title screen
STATUS_MENU_START = 10          # * Used to delimit the menu
STATUS_MENU_END = 19            # * End of Menu
STATUS_SUBCOMMAND = 21
STATUS_NEW = 30                 # * Game is ready to start, but not running
STATUS_PLAYER1_START = 31
STATUS_END = 50                 # * End of game reached
STATUS_SHOW_SCORE = 51          # End message is displayed ready to restart

# Number of actions to complete before moving up to the next level
# Default = 30 (change for debugging)
NEXT_LEVEL_ACTIONS = 30
#NEXT_LEVEL_ACTIONS = 5

# Number of seconds to display high score before allowing click to continue
TIME_DISPLAY_SCORE = 3

# Number of seconds when the timer starts 
TIMER_START = 10.9
PAUSE_TIME = 1.5

class GamePlay:
    
    # These are what we need to track
    score = 0
    level = 0
    
    # This is the timer we use for counting down time
    game_timer = Timer(TIMER_START)
    # Timer for game pauses 
    timer_pause = Timer(PAUSE_TIME)
    # user pause is pause waiting on user (eg. to click)
    # Can be True (paused) or False (unpaused)
    user_pause = False
    
    # Set a default target (but this will be updated when random direction generated)
    target = 'south'
    
    # Message to display when paused / level up etc.
    game_message = ""
    # Track number of actions caught within this level - used to determine decay and next level
    level_actions_complete = 0
    
    status = STATUS_TITLE
       
    # Must be initialized with a  game_timer timer (of Timer class) and dictionary with action_text instructions
    def __init__(self, action_text):
        self.action_text = action_text
        # Set initial target move
        self.getNextMove()
        
    def setShowScore(self):
        self.status = STATUS_SHOW_SCORE
        self.timer_pause.startCountDown()
        
    def isShowScore(self):
        if (self.status == STATUS_SHOW_SCORE):
            return True
        return False
        
    # Only returns true if STATUS_SHOW_SCORE and timer expired
    def isScoreShown(self):
        if (self.status == STATUS_SHOW_SCORE and self.timer_pause.getTimeRemaining() <= 0):
            return True
        return False
    
    # If game has not yet started
    def isNewGame(self):
        if self.status == STATUS_NEW:
            return True
        return False
        
    def isTitleScreen(self):
        if self.status == STATUS_TITLE:
            return True
        return False
        
    def isGameOver(self):
        if self.status == STATUS_END:
            return True
        return False
        
    def setGameOver(self):
        # Add short timer for game over to ensure
        # player gets to see high score
        self.game_timer.startCountDown(TIME_DISPLAY_SCORE)
        self.status = STATUS_END
        
    def isGameRunning(self):
        if (self.status >= STATUS_PLAYER1_START and self.status < STATUS_END):
            return True
        return False
        
        
    def startNewGame(self):
        self.reset()
        self.status = STATUS_NEW
        self.getNextMove()
        # Resets and start the timer
        self.game_timer.resetToDefault()
        self.status = STATUS_PLAYER1_START
        
        
    # Point scored, so add score and get next move
    # Update level if required then return level number
    def scorePoint(self):
        self.score += 1
        self.getNextMove()
        self.level_actions_complete += 1
        # Update timer - subtracting timer decrement for each point scored
        timer_start = self.game_timer.getSetTime()       # current timer start
        # Timer update to extend a little due to difficulty
        new_timer_time = timer_start + 2.5 - (timer_start * (self.level_actions_complete / (self.level_actions_complete + 10)))
        # Don't want new timer to be larger than previous
        if (new_timer_time > timer_start):
            new_timer_time = timer_start
        self.game_timer.startCountDown(new_timer_time)
        
        # Check to see if the user has scored enough to move up a level
        if (self.level_actions_complete >= NEXT_LEVEL_ACTIONS):
            self.game_timer.resetToDefault()
            self.level += 1
            self.level_actions_complete = 0
        return self.level
        
    def getScore(self):
        return self.score
        
    # Returns level number - or 0 if not in play
    def getLevel(self):
        if (self.isGameRunning()):
            return self.level
        else:
            return 0
        
    # Return status, unless not running
    def getStateString(self):
        if (self.isGameRunning()):
            return self.action_text[self.target]   
        else:
            return ("Not running")
         
    def getGameMessage(self):
        return self.game_message
     
      
    # If game paused normally then decrement
    # If game 0 then return False - no longer paused
    # Otherwise return True
    def isTimerPause(self):
        if (self.timer_pause.getTimeRemaining() > 0):
            return True
        return False
     
    # Specifically looks if the user has paused (ie game_pause = -1)
    def isUserPause(self):
        return self.user_pause
     
    # Set pause to number of updates (approx 60 per second)
    # Or set to 0 for no pause
    # Don't use for user pause (as may change in future)
    def setTimerPause(self, time):
        self.timer_pause.startCountDown(time)

    def startTimerPause(self):
        self.timer_pause.startCountDown()
    
    # Pause waiting on user - True = pause, False = not pause
    def setUserPause(self, status=True):
        self.game_pause = status
        
    def getCurrentMove(self):
        return self.target
        
    # Update to next move and return
    #Get next direction / jump / duck 
    def getNextMove(self):
        move_choices = ['north', 'south', 'east', 'west', 'jump', 'duck']
        self.target = random.choice(move_choices)
        return self.target
        
    def setGameMessage(self, message):
        self.game_message = message
        
    def getGameMessage(self):
        return self.game_message

    def getTimeRemaining(self):
        return self.game_timer.getTimeRemaining()
        
        
    def setMenu(self, first_run = False):
        self.status = STATUS_MENU_START
        # If first run then don't use timer so can move cursor straight away
        if (first_run):
            self.timer_pause.expireCountDown()
        else:
            self.timer_pause.startCountDown()
        
    def isMenu(self):
        if (self.status >= STATUS_MENU_START and self.status <= STATUS_MENU_END):
            return True
        return False
        
        
    def setSubCommand(self, sub_command):
        self.sub_command = sub_command
        self.status = STATUS_SUBCOMMAND
        
    def isSubCommand(self):
        if self.status == STATUS_SUBCOMMAND:
            return True
        return False
        
    def getSubCommand(self):
        if self.status == STATUS_SUBCOMMAND:
            return self.sub_command
        return None
        
        
    # Gets the current status as a number - use for debugging only
    def getStatusNum(self):
        return self.status
        
        
    # Reset game to level 
    def reset(self):
        self.level_actions_complete = 0
        self.score = 0
        self.level = 1