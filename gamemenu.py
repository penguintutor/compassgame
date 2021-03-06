# Handles Menu operations

import pygame
from pygame import Surface, Rect
import pgzero

from timer import Timer
from menuitem import MenuItem


    
# Status values
STATUS_MENU = 0
STATUS_CLICKED = 1
STATUS_PAGE = 2

class GameMenu:
    
    # Menu item details, perhaps consider putting this in a configuration
    # file in future
    
    menu_items = [
        MenuItem('Start game', 'start', 'command'),
        MenuItem('Instructions', 'instructions', 'textpage'),
        MenuItem('Customize character', 'character', 'subcommand'),
        MenuItem('Game controls', 'controls', 'subcommand'),
        MenuItem('View high scores', 'highscore', 'subcommand'),
        MenuItem('Credits', 'credits', 'textpage'),
        MenuItem('Quit', 'quit', 'command')
    ]
    
    # Dictionary of text pages for menu entries 
    # Note currently no word wrapping - needs \n to be added in advance
    menu_pages = {
        'instructions':"INSTRUCTIONS\n\nFollow the direction at the top centre\nof the screen.\n\nMove the character using a joystick (Picade)\n or cursor keys (keyboard).\nPress top button or SPACE to duck\nPress RIGHT SHIFT to view the map\n\nAvoid the obstacles that appear on later levels\n",
        'credits':"CREDITS\n\nCreate by Stewart Watkiss\nMade available under GPL v3 License\nSee: www.penguintutor.com/compassgame"
    }
    
    
    menu_spacing = 50 # distance between menu items
    top_spacing = 20  # distance between top of menu and start of menu
    left_spacing = 20 # distance between left and text for page text / command text
    menu_font_size = 45   # size of font for menu items
    menu_font_page = 32   # size of font for text page display
    status = STATUS_MENU         # Track whether to display menu or in menu etc.


    # Requires width and height - these can be the same as the screen or smaller if need to constrain menu
    # Offset and border determine distance from origin of screen and any fixed area to avoid respectively
    def __init__(self, game_controls, width, height, offset=(0,0), border=100):
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
        
        # Finish setting up MenuItems
        # At the moment this doesn't provide much extra functionality, but by 
        # placing it into the MenuItem object then makes it easier if we load 
        # MenuItems from a configuration file in future
        for i in range (0,len(self.menu_items)):
            if self.menu_items[i].getCommand() in self.menu_pages:
                self.menu_items[i].setPage(self.menu_pages[self.menu_items[i].getCommand()])
                
        
    # Update menu based on keyboard direction
    # If return is 'menu' then still in menu, so don't update anything else
    # If return is 'quit' then quit the application
    # Any other return is next instruction 
    def update(self, keyboard):
        # set status_selected if menu status changed (through mouse click or press)
        selected_command_type = ""
        selected_command = ""
        # check if status is clicked - which means mouse was pressed on a valid entry
        if (self.status == STATUS_CLICKED):
            selected_command_type = self.menu_items[self.menu_pos].getMenuType()
            selected_command = self.menu_items[self.menu_pos].getCommand()
            self.status = STATUS_MENU
        # check if we are in menu timer in which case return until expired
        elif (self.menu_timer.getTimeRemaining() > 0): 
            return 'menu'
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
                selected_command_type =  self.menu_items[self.menu_pos].getMenuType()
                selected_command = self.menu_items[self.menu_pos].getCommand()
            # If click was on text page then return to main menu
            elif (self.status == STATUS_PAGE):
                selected_command_type = 'menu'
                self.status = STATUS_MENU
                self.menu_timer.startCountDown()
        elif (self.game_controls.isPressed(keyboard,'escape')):
            selected_command_type = 'command'
            selected_command = 'quit'
            
        # If a menu object was clicked / chosen then handle
        if (selected_command_type == 'command'):
            # Reset menu to start position
            self.reset()
            return selected_command
        elif (selected_command_type == 'textpage'):
            self.status = STATUS_PAGE
            self.menu_timer.startCountDown()
            return 'menu'
        elif (selected_command_type == 'subcommand'):
            return selected_command
        else:
            return 'menu'

    
    def show(self, screen):
        # Create a rectangle across the area - provides transparancy
        screen.blit(self.menu_surface,self.start_pos)
        # draw directly onto the screen draw surface (transparency doesn't apply)
        if (self.status == STATUS_MENU):
            self.showMenu(screen)
        elif (self.status == STATUS_PAGE):
            self.showPage(screen)
        
        
        
    def showMenu(self, screen):
        for menu_num in range (0,len(self.menu_items)):
            if (menu_num == self.menu_pos):
                background_color = (255,255,255)
            else:
                background_color = None
            screen.draw.text(self.menu_items[menu_num].getText(), fontsize=self.menu_font_size, midtop=(self.width/2,self.offset[1]+self.border+(self.menu_spacing*menu_num)+self.top_spacing), color=(0,0,0), background=background_color)
            
            
    # Shows a page of text
    def showPage(self, screen):
        page_text = self.menu_items[self.menu_pos].getPage()
        screen.draw.text(page_text, fontsize=self.menu_font_page, topleft=(self.offset[0]+self.border+self.left_spacing,self.offset[1]+self.border+self.top_spacing), color=(0,0,0))
        
           

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
    
    def reset(self):
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
