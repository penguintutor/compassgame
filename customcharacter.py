import re
from os import listdir
from pgzero.actor import Actor

from timer import Timer

# Directories relative to the application directory
THEME_DIR = "themes/"
IMAGE_DIR = "images/"             # This is fixed for pgzero files
TEMP_DIR = "tmp/"                 # Use to create svgs before creating the png files

# Track state for the display 
# 'main' is the main page, 'custom' is used to choose custom colours, 'clicked' used to handle mouse click
STATUS_MAIN = 0
STATUS_CUSTOM = 1
STATUS_CLICKED = 2

CONVERT_CMD = "/usr/bin/convert"

class CustomCharacter:
    
    background_img = "background_settings_01"

    # Load default image for each actor to allow character selection
    current_theme_actors = []
    available_theme_actors = []
    
    current_themes = []    # Stores tuple with theme and variation number - eg. (person1,2)
    available_themes = []
    
    
    current_actor_ypos = 220
    custom_actor_ypos = 460
    
    # Are we on top row (0 = current_characters) or bottom row (1 = customize characters) 
    selected_row = 0
    # position of selection on the x axis
    selected_col = 0
    
    # Default theme must be valid
    theme = "person1"
    theme_num = 0
    
    
    status = STATUS_MAIN

    def __init__ (self, img_file_format):
        self.img_file_format = img_file_format
        # Create a regular expression to identify themes
        # does not use \w as do not include _ character
        # Look for image 0 (down 1) - other variants of the first number part is different colours
        # Timer restrict keyboard movements to every 1/2 second (prevent multiple presses)
        self.pause_timer = Timer(0.25)
        
        # Load the themes - only look in the SVG folder
        theme_regexp_string = img_file_format.format("([a-zA-Z0-9]+)", "00", "down", "01")+".svg"
        theme_regexp = re.compile(theme_regexp_string)
        xpos = 100
        for file in listdir(THEME_DIR):
            matches = theme_regexp.match(file)
            if (matches != None):
                # uses group(0) for full filename, group(1) for theme name
                self.available_themes.append(matches.group(1))
                # Add default image (theme 00 down 01) as actor
                self.available_theme_actors.append(Actor(img_file_format.format(matches.group(1), "00", "down", "01"), (xpos,self.custom_actor_ypos)))
                xpos += 100
                
        # Load the different variations on the themes currently available
        png_regexp_string = img_file_format.format("([a-zA-Z0-9]+)", "([0-9][0-9])", "down", "01")+".png"
        png_regexp = re.compile(png_regexp_string)
        xpos = 100
        for file in listdir(IMAGE_DIR):
            matches = png_regexp.match(file)
            if (matches != None):
                # uses group(0) for full filename, group(1) for theme name
                self.current_themes.append((matches.group(1),int(matches.group(2))))
                self.current_theme_actors.append(Actor(img_file_format.format(matches.group(1), matches.group(2), "down", "01"), (xpos,self.current_actor_ypos)))
                xpos += 100
            
        

    def draw(self, screen):
        if (self.status == STATUS_MAIN):
            self.drawMain(screen)
        elif (self.status == STATUS_CUSTOM):
            self.drawCustom(screen)
        
    def drawCustom(self, screen):
        screen.blit(self.background_img, (0,0))
        screen.draw.text('Customize Character', fontsize=60, center=(450,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        self.preview.draw()
        
          
        
    def drawMain(self, screen):
        screen.blit(self.background_img, (0,0))
        screen.draw.text('Custom Character', fontsize=60, center=(400,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        
        screen.draw.text('Existing Character', fontsize=40, center=(400,120), shadow=(1,1), color=(255,255,255), scolor="#202020")      
        for i in range (0,len(self.current_theme_actors)):
            self.current_theme_actors[i].draw()
            
        screen.draw.text('Customize Character', fontsize=40, center=(400,340), shadow=(1,1), color=(255,255,255), scolor="#202020")      
        for i in range (0,len(self.available_theme_actors)):
            self.available_theme_actors[i].draw()
            
        # Draw a box around the current character
        # Get a rect same pos as character
        if (self.selected_row == 0):
            highlight_rect = self.current_theme_actors[self.selected_col].copy()
        elif (self.selected_row == 1):
            highlight_rect = self.available_theme_actors[self.selected_col].copy()
            
        screen.draw.rect(highlight_rect, (255,255,255))
        
    
    def update(self, keyboard):
        if (self.pause_timer.getTimeRemaining() > 0):
            return
        # Control main screen
        if (self.status == STATUS_MAIN):
            # returns whatever updateMain returns - None if still in selection or menu if theme updated
            return self.updateMain(keyboard)
        elif (self.status == STATUS_CUSTOM):
            self.status = self.updateCustom(keyboard)
            if (self.status == STATUS_MAIN):
                self.pause_timer.startCountDown()
            return
        # If mouse clicked
        elif (self.status == STATUS_CLICKED):
            self.status = STATUS_MAIN
            if (self.selected_row == 0):
                (self.theme, self.theme_num) = self.current_themes[self.selected_col]
            return 'menu'
        else:
            return
            
    # Update on customize screen
    def updateCustom(self, keyboard):
        if (keyboard.space or keyboard.lshift or keyboard.rshift or keyboard.lctrl or keyboard.RETURN):
            return STATUS_MAIN
        else:
            return STATUS_CUSTOM
            
    # Update main screen
    def updateMain(self, keyboard):
        if (keyboard.up):
            self.selected_row = 0
            self.selected_col = self.checkColPos(self.selected_col, self.selected_row)
        if (keyboard.down):
            self.selected_row = 1
            self.selected_col = self.checkColPos(self.selected_col, self.selected_row)
        if (keyboard.right):
            self.selected_col = self.checkColPos(self.selected_col + 1, self.selected_row)
        if (keyboard.left):
            self.selected_col = self.checkColPos(self.selected_col - 1, self.selected_row)
        if (keyboard.space or keyboard.lshift or keyboard.rshift or keyboard.lctrl or keyboard.RETURN):
            # If pressed on top row then update theme
            if (self.selected_row == 0):
                (self.theme, self.theme_num) = self.current_themes[self.selected_col]
            elif (self.selected_row == 1):
                self.customize_theme = self.available_themes[self.selected_col]
                self.status = STATUS_CUSTOM
                self.preview = Actor (self.img_file_format.format(self.customize_theme, "00", "down", "01"), (700,150)) 
            return 'menu'
    
    # Checks to see if col is too far left or right and returns nearest safe pos
    def checkColPos (self, col_pos, row_pos):
        # Too far left is same either case return 0
        if (col_pos < 0): 
            return 0
        # Top row
        if (row_pos == 0):
            if (col_pos >= len(self.current_themes)):
                return (len(self.current_themes) -1)
        elif (row_pos == 1):
            if (col_pos >= len(self.available_themes)):
                return (len(self.available_themes) -1)
        return col_pos
    
    def mouse_move (self,pos):
        pass
    
    def mouse_click (self,pos):
        if (self.pause_timer.getTimeRemaining() > 0):
            return
        self.pause_timer.startCountDown()
        if (self.status == STATUS_MAIN):
            # cycle through different images checking for collision
            for i in range (0,len(self.current_theme_actors)):
                if (self.current_theme_actors[i].collidepoint(pos)):
                    self.selected_row = 0
                    self.selected_col = i
                    self.status = STATUS_CLICKED
                    return
            for i in range (0,len(self.available_theme_actors)):
                if (self.available_theme_actors[i].collidepoint(pos)):
                    self.selected_row = 1
                    self.selected_col = i
                    self.status = STATUS_CLICKED
                    return
            
    
   
    
    def select(self):
        self.pause_timer.startCountDown()
        
        
    def getTheme(self):
        return (self.theme, self.theme_num)