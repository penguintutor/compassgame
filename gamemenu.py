# Handles Menu operations
import pygame
from pygame import Surface, Rect
import pgzero

from timer import Timer


class MenuItem:
    
    def __init__ (self, text, command):
        self.text = text                                                                                     
        self.command = command
        
        
    def getText(self):
        return self.text
        
    def getCommand(self):
        return self.command
    


class GameMenu:
    
    menu_items = [
        MenuItem('Start game', 'start'),
        #MenuItem('Instructions', 'instructions'),
        #MenuItem('Customize character', 'character'),
        #MenuItem('Game controls', 'controls'),
        #MenuItem('View high scores', 'highscore'),
        #MenuItem('Credits', 'credits'),
        MenuItem('Quit', 'quit')
    ]
    
    

    menu_spacing = 50 # distance between menu items
    top_spacing = 20  # distance between top of menu and start of menu
    menu_font_size = 45   # size of font for menu items


    # Requires width and height - these can be the same as the screen or smaller if need to constrain menu
    # Offset and border determine distance from origin of screen and any fixed area to avoid respectively
    def __init__(self, width, height, offset=(0,0), border=100):
        self.width = width              # width of screen
        self.height = height            # height of screen
        self.offset = offset            # tuple x,y for offset from start of screen
        self.border = border            # single value same for x and y
        # Start position of the menu area and size
        self.start_pos = (self.offset[0]+self.border, self.offset[1]+self.border)
        self.size = (self.width-2*self.start_pos[0], self.height-2*self.start_pos[1])
        
        # Create a menu surface - this involves using pygame surface feature (rather than through pygame zero)
        # Allows for more advanced features such as alpha adjustment (partial transparency)
        self.menu_surface = Surface(self.size)
        # 75% opacity
        self.menu_surface.set_alpha(192)
        
        # Position of rect is 0,0 relative to the surface, not the screen
        self.menu_box = Rect((0,0),self.size)
        # Uses pygame rect so we can add it to own surface
        self.menu_rect = pygame.draw.rect(self.menu_surface , (200,200,200), self.menu_box)
        self.menu_pos = 0       # Tracks which menu item is selected
        
        # Timer restrict keyboard movements to every 1/2 second (prevent multiple presses)
        self.menu_timer = Timer(1.25)
        
    # Update menu based on keyboard direction
    # If return is 'menu' then still in menu, so don't update anything else
    # If return is 'quit' then quit the application
    # Any other return is next instruction 
    def update(self, keyboard):
        # First check if we are in menu timer in which case return until expired
        if (self.menu_timer.getTimeRemaining() > 0): 
            return 'menu'
        if (keyboard.up and self.menu_pos>0):
            self.menu_pos -= 1
            self.menu_timer.startCountDown()
        elif (keyboard.down and self.menu_pos<len(self.menu_items)-1):
            self.menu_pos += 1
            self.menu_timer.startCountDown()
        elif (keyboard.space or keyboard.lshift or keyboard.rshift or keyboard.lctrl or keyboard.RETURN):
            if (self.menu_items[self.menu_pos].getCommand() == 'quit' or self.menu_items[self.menu_pos].getCommand() == 'start'):
                # Reset menu to start position
                self.reset()
                return self.menu_items[self.menu_pos].getCommand()
        elif (keyboard.escape):
            return 'quit'
        # Reach this point then remain in menu
        return 'menu'
    
    def show(self, screen):
        # Create a rectangle across the area
        screen.blit(self.menu_surface,self.start_pos)
        # Now draw directly onto the screen draw surface (transparency doesn't apply)
        pos_num = 0
        
        for menu_num in range (0,len(self.menu_items)):
            if (pos_num == self.menu_pos):
                background_color = (255,255,255)
            else:
                background_color = None
            screen.draw.text(self.menu_items[menu_num].getText(), fontsize=self.menu_font_size, midtop=(self.width/2,self.offset[1]+self.border+(self.menu_spacing*menu_num)+self.top_spacing), color=(0,0,0), background=background_color)
            pos_num+=1

    
    def reset(self):
        pos_num = 0
    
