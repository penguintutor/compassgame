import re
#import yaml
from os import listdir
from pgzero.actor import Actor
from pgzero.rect import Rect

from timer import Timer
from themedetails import ThemeDetails

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
    
    # Which row is selected when creating a custom entry
    selected_row_custom = 0
    # which colour col pos is selected (-1 = none)
    selected_colour_custom = -1
    
    
    # Default theme must be valid
    theme = "person1"
    theme_num = 0
    
    # Class to hold details of theme from config file
    theme_config = ThemeDetails(THEME_DIR)
    
    
    status = STATUS_MAIN

    def __init__ (self, img_file_format):
        self.img_file_format = img_file_format
        # Create a regular expression to identify themes
        # does not use \w as do not include _ character
        # Look for image 0 (down 1) - other variants of the first number part is different colours
        # Timer restrict keyboard movements to fraction of second to prevent multiple presses
        self.pause_timer = Timer(0.15)
        
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
        screen.draw.text('Customize Character', fontsize=60, center=(400,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        if (not self.theme_config.isThemeLoaded):
            screen.draw.text('No config found for this theme, please choose a different theme', fontsize=40, topleft=(100,150), color=(255,0,0))
            return
        ypos = 100
        list_keys = self.theme_config.getKeys()
        for i in range(0,len(list_keys)):
            key = list_keys[i]
            screen.draw.text(self.theme_config.getLabel(key), fontsize=30, topleft=(100,ypos), color=(0,0,0))
            if (i == self.selected_row_custom):
                if (self.selected_colour_custom == -1):
                    self.drawColourBox(screen, True, self.theme_config.getColour(key), 300, ypos)
                else:
                    self.drawColourBox(screen, False, self.theme_config.getColour(key), 300, ypos)
                # If a row selected then show colour options
                self.showColourOptions (screen, key, 350, ypos)
            else:
                self.drawColourBox(screen, False, self.theme_config.getColour(key), 300, ypos)
            ypos += 50
        # Add OK / Cancel buttons
        if (self.selected_row_custom == self.theme_config.numKeys() and self.selected_colour_custom == -1):
            screen.draw.text('Save', fontsize=30, center=(150,500), color=(0,0,0), background=(255,255,255))
        else:
            screen.draw.text('Save', fontsize=30, center=(150,500), color=(0,0,0))
        if (self.selected_row_custom == self.theme_config.numKeys() and self.selected_colour_custom > -1):
            screen.draw.text('Cancel', fontsize=30, center=(300,500), color=(0,0,0), background=(255,255,255))
        else:
            screen.draw.text('Cancel', fontsize=30, center=(300,500), color=(0,0,0))
        self.preview.draw()                                                    
        
    # Draws box, if selected = True includes highlight 
    # x, y pos is the box without highlighting - with highligting it will be -2 from that value
    def drawColourBox(self, screen, selected, colour, xpos, ypos):
        if (selected):
            # If cursor is on this position (-1) then highlight current colour
            # Higlight with black and white so it will contrast with either colour
            screen.draw.filled_rect(Rect((xpos,ypos),(24,24)), (0,0,0))
            screen.draw.filled_rect(Rect((xpos-2,ypos-2),(24,24)), (255,255,255))
        screen.draw.filled_rect(Rect((xpos,ypos),(20,20)), colour )
        
        
    # Shows the available colours - part is what part of body / clothing
    def showColourOptions(self, screen, part, xpos, ypos):
        colour_options = self.theme_config.getColourOptions(part)
        for i in range(0,len(colour_options)):
            if (i == self.selected_colour_custom):
                self.drawColourBox(screen, True, colour_options[i], xpos+(25*i), ypos)
            else:
                self.drawColourBox(screen, False, colour_options[i], xpos+(25*i), ypos)
        
    def drawMain(self, screen):
        screen.blit(self.background_img, (0,0))
   
        # Draw a box around the current character
        # Get a rect same pos as character
        # Done first so that it can be filled to make lines thicker 
        if (self.selected_row == 0):
            highlight_rect = self.current_theme_actors[self.selected_col].copy()
        elif (self.selected_row == 1):
            highlight_rect = self.available_theme_actors[self.selected_col].copy()
        highlight_rect.inflate_ip(6,6)
        screen.draw.filled_rect(highlight_rect, (255,255,255))
        
        screen.draw.text('Custom Character', fontsize=60, center=(400,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        
        screen.draw.text('Existing Character', fontsize=40, center=(400,120), shadow=(1,1), color=(255,255,255), scolor="#202020")      
        for i in range (0,len(self.current_theme_actors)):
            self.current_theme_actors[i].draw()
            
        screen.draw.text('Customize Character', fontsize=40, center=(400,340), shadow=(1,1), color=(255,255,255), scolor="#202020")      
        for i in range (0,len(self.available_theme_actors)):
            self.available_theme_actors[i].draw()
        
    
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
        self.pause_timer.startCountDown()
        if (keyboard.down):
            self.selected_row_custom +=1
            # If already on bottom row (Cancel / OK Button) then stay there and return
            if (self.selected_row_custom > self.theme_config.numKeys()):
                self.selected_row_custom = self.theme_config.numKeys()
                return STATUS_CUSTOM
            # Whenever moving up or down reset to the current colour position  (or OK button for bottom row)
            self.selected_colour_custom = -1
            # Row after colours is Cancel / OK button
            if (self.selected_row_custom >= self.theme_config.numKeys()):
                    self.selected_row_custom = self.theme_config.numKeys()
        if (keyboard.up):
            self.selected_row_custom -=1
            # Whenever moving up or down reset to the current colour position
            self.selected_colour_custom = -1
            # Row after colours is Cancel / OK button
            if (self.selected_row_custom < 0):
                    self.selected_row_custom = 0
        if (keyboard.left):
            self.selected_colour_custom -= 1
            if self.selected_colour_custom < -1:
                self.selected_colour_custom = -1
        if (keyboard.right):
            # Reuse the colour for use by the Cancel button
            if (self.selected_row_custom > self.theme_config.numKeys()):
                self.selected_colour_customer = 0
                return STATUS_CUSTOM
            self.selected_colour_custom += 1
            if self.selected_colour_custom > self.theme_config.numColourOptions() -1:
                self.selected_colour_custom = self.theme_config.numColourOptions() -1
        if (keyboard.space or keyboard.lshift or keyboard.rshift or keyboard.lctrl or keyboard.RETURN):
            if (self.selected_row_custom < self.theme_config.numKeys()):
                all_keys = self.theme_config.getKeys()
                this_key = all_keys[self.selected_row_custom]
                colour_options = self.theme_config.getColourOptions(this_key)
                # update with the selected colour
                self.theme_config.setColour(this_key,colour_options[self.selected_colour_custom])
                return STATUS_CUSTOM
            # Here if it's a select on bottom row = Save or Cancel
            # Cancel button selected
            elif (self.selected_colour_custom > -1):
                return STATUS_MAIN
            else:
                #### Save the entry
                #Todo
                return STATUS_CUSTOM
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
                self.theme_config.loadConfig(self.customize_theme)
                self.pause_timer.startCountDown()
                return 'character'
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