# Handles Custom Controller Menu

import pygame
from pygame import Surface, Rect
import pgzero
from pgzero.constants import keys as keycodes

from timer import Timer
from menuitem import MenuItem

    
# Status values
STATUS_MENU = 0
STATUS_CLICKED = 1
STATUS_CUSTOM_KEY = 2

class CustomControls:
    
    
    menu_spacing = 35 # distance between menu items
    top_spacing = 20  # distance between top of menu and start of menu
    left_spacing = 20 # distance between left and text for page text / command text
    menu_font_size = 32   # size of font for menu items
    status = STATUS_MENU         # Track whether to display menu or in menu etc.


    # Requires width and height - these can be the same as the screen or smaller if need to constrain menu
    # Offset and border determine distance from origin of screen and any fixed area to avoid respectively
    def __init__(self, game_controls, width=800, height=600, offset=(0,0), border=100):
        self.game_controls = game_controls
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

        
        # Timer restrict keyboard movements to prevent multiple presses
        self.menu_timer = Timer(0.12)
        
        self.menu_items = []
        # Store keys in an array to fix order and make easier to identify selected key
        for this_key in self.game_controls.getKeys():
            self.menu_items.append(MenuItem(this_key+" ("+str(self.game_controls.getKeyString(this_key))+")", this_key, 'control'))
                
        # Dummy entry - blank line
        self.menu_items.append(MenuItem("","","controls"))
        # Last Menu item is to save and return
        self.menu_items.append(MenuItem("Save settings", 'save', 'menu'))


        
    # Update menu based on keyboard direction
    # If return is 'controls' then still in custon controls, so don't update anything else
    # If return is 'menu' then return to main game menu
    def update(self, keyboard):
        if (self.status == STATUS_CUSTOM_KEY and self.menu_timer.getTimeRemaining() <= 0):
            keycode = self.checkKey(keyboard)
            if (keycode != None):
                self.game_controls.setKey(self.selected_key, keycode)
                self.status = STATUS_MENU
            return 'controls'
        # check if status is clicked - which means mouse was pressed on a valid entry
        if (self.status == STATUS_CLICKED):
            self.selected_key = self.menu_items[self.menu_pos].getCommand()
            self.reset()
            self.status = STATUS_CUSTOM_KEY
        # check if we are in menu timer in which case return until expired
        elif (self.menu_timer.getTimeRemaining() > 0): 
            return 'controls'
        elif (self.game_controls.isPressed(keyboard,'up') and self.menu_pos>0):
            if (self.status == STATUS_MENU):
                self.menu_pos -= 1
                self.menu_timer.startCountDown()
        elif (self.game_controls.isPressed(keyboard,'down') and self.menu_pos<len(self.menu_items)-1):
            if (self.status == STATUS_MENU):
                self.menu_pos += 1
                self.menu_timer.startCountDown()
        elif (self.game_controls.isOrPressed(keyboard,['jump','duck'])):
            if (self.status == STATUS_MENU):
                self.selected_key = self.menu_items[self.menu_pos].getCommand()
                self.reset()
                # special case where selected_key is the save option
                if (self.selected_key == 'save'):
                    ##Todo
                    # Handle save here
                    return 'menu'
                self.status = STATUS_CUSTOM_KEY
        elif (self.game_controls.isPressed(keyboard,'escape')):
            return 'menu'
        return 'controls'            

    # Checks pygame event queue for last key pressed
    def checkKey(self, keyboard):
        # Check all keycodes to see if any are high
        for this_code in keycodes:
            if (keyboard[this_code]):
                    return this_code
        return None


    
    def draw(self, screen):
        # Create a rectangle across the area - provides transparancy
        screen.blit(self.menu_surface,self.start_pos)
        # draw directly onto the screen draw surface (transparency doesn't apply)
        if (self.status == STATUS_MENU):
            self.drawMenu(screen)
        elif (self.status == STATUS_CUSTOM_KEY):
            self.drawCustom(screen)
        
        
    def drawCustom(self, screen):
        screen.draw.text("Press custom key for "+self.selected_key, fontsize=self.menu_font_size, midtop=(self.width/2,self.offset[1]+self.border+(self.menu_spacing)+self.top_spacing), color=(0,0,0))
        
        
    def drawMenu(self, screen):
        for menu_num in range (0,len(self.menu_items)):
            if (menu_num == self.menu_pos):
                background_color = (255,255,255)
            else:
                background_color = None
            screen.draw.text(self.menu_items[menu_num].getText(), fontsize=self.menu_font_size, midtop=(self.width/2,self.offset[1]+self.border+(self.menu_spacing*menu_num)+self.top_spacing), color=(0,0,0), background=background_color)
           

    def mouse_move(self, pos):
        if (self.status == STATUS_MENU): 
            return_val = self.get_mouse_menu_pos(pos)
            if return_val != -1:
                self.menu_pos = return_val


    def mouse_click(self, pos):
        if (self.status == STATUS_MENU): 
            return_val = self.get_mouse_menu_pos(pos)
            if return_val != -1:
                self.menu_pos = return_val
                self.status = STATUS_CLICKED
        # If click from text page then return to menu
        elif (self.status == STATUS_PAGE):
            self.status = STATUS_MENU
    
    def select(self):
        self.menu_timer.startCountDown()
        
    
    def reset(self):
        self.menu_timer.startCountDown()
        self.menu_pos = 0
        self.status = STATUS_MENU
    
    
    # Checks if mouse is over menu and if so returns menu position
    # Otherwise returns -1
    def get_mouse_menu_pos (self, pos):
        if (pos[0] > self.start_pos[0] and pos[1] > self.start_pos[1] + self.top_spacing and pos[0] < self.start_pos[0] + self.size[0] and pos[1] < self.start_pos[1] + self.size[1]):
            start_y = self.start_pos[1] + self.top_spacing
            for this_menu_pos in range(0,len(self.menu_items)):
                if (pos[1] - start_y >= this_menu_pos * self.menu_spacing and pos[1] - start_y <= (this_menu_pos * self.menu_spacing)+self.menu_spacing):
                    return this_menu_pos
        # If not returned then not over menu
        return -1
