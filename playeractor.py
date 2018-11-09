import math

from pgzero.actor import Actor

# Card is based on an Actor (uses inheritance)
class PlayerActor(Actor):

    # Status can be normal or hidden
    status = 'normal'
    # Direction that player is facing
    direction = 'down'
    # walking position of player (number from 1 to 4 represent position of feet)
    player_step_position = 1
    # num moves per step (ie don't move feet if less than this)
    # If set too low then legs will move really fast - default 5
    step_delay = 5
    # track number of moves per step
    player_step_count = 0
    
    # theme is image number
    def __init__(self, theme, theme_num, player_image_format, screen_width, screen_height):
        self.theme = theme
        self.theme_num = theme_num
        self.player_image_format = player_image_format
        self.screen_width = screen_width
        self.screen_height = screen_height 
        # Call Actor constructor (center the Actor)
        Actor.__init__(self, self.getImage(), (self.screen_width / 2, self.screen_height / 2))


            
    # Override Actor.draw
    def draw(self):
        if (self.status == 'hidden'):
            return
        Actor.draw(self)

    def hide(self):
        self.status = 'hidden'
        
    # When unhide set it to back image
    def unhide (self):
        self.status = 'normal'
        
    def isHidden (self):
        if self.status == 'hidden':
            return True
        return False

    def reset (self):
        self.unhide()
                            
    def toString(self):
        return self.name
        
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
    # Sets direction and also resets player_step_count
    def setDirection(self, direction):
        self.direction = direction
        self.player_step_count = 0
        self.player_step_position = 1
        self.image = self.getImage()
        
    def getDirection(self):
        return self.direction
        
    def equals (self, othercard):
        if self.name == othercard.toString(): 
            return True
        return False
        
    # Move Actor also handles image change
    def moveActor(self, direction, distance = 5):
        if (direction == 'up'):
            self.y -= distance
        if (direction == 'right'):
            self.x += distance
        if (direction == 'down'):
            self.y += distance
        if (direction == 'left'):
            self.x -= distance
        
        # Check not moved past the edge of the screen
        if (self.y <= 30):
            self.y = 30
        if (self.x <= 12):
            self.x = 12
        if (self.y >= self.screen_height - 30):
            self.y = self.screen_height - 30
        if (self.x >= self.screen_width - 12):
            self.x = self.screen_width - 12
    
    # gets image based on status of player
    def getImage(self):
        return self.player_image_format.format(self.theme, self.theme_num, self.direction, self.player_step_position)
    
    def isJumpDuck(self):
        if (self.direction == 'jump' or self.direction == 'duck'):
            return True
        return False
        
    def updImage(self, new_direction):
        # Check for duck and jump as don't increment digit & image - we just have one duck / jump image
        if (self.direction == new_direction and (self.direction == 'duck' or self.direction == 'jump')):
            return
    
        # If change in direction
        if (self.direction != new_direction) :
            self.player_step_count = 0
        else :
            self.player_step_count += 1
            
        if (self.player_step_count >= 4 * self.step_delay):
            self.player_step_count = 0
            
        # set the direction to be the new direction
        self.direction = new_direction
        self.player_step_position = math.floor(self.player_step_count / self.step_delay) +1
        self.image = self.getImage()
        
    # Theme and theme_num must be a tuple (which is what CustomCharacter.getTheme() returns) 
    def setTheme(self, theme_tuple):
        self.theme = theme_tuple[0]
        self.theme_num = theme_tuple[1]
        self.updImage("down")

    def reset(self):
        self.score = 0
        self.level_actions_complete = 0
        self.direction = 'down'
        self.player_step_position = 1
        self.player_step_count = 0
        