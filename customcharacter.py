import re
from os import listdir
from pgzero.actor import Actor

from timer import Timer

# Directories relative to the application directory
THEME_DIR = "themes/"
IMAGE_DIR = "images/"             # This is fixed for pgzero files

CONVERT_CMD = "/usr/bin/convert"

class CustomCharacter:
    
    background_img = "background_settings_01"

    # Load default image for each actor to allow character selection
    current_theme_actors = []
    available_theme_actors = []
    
    available_themes = []
    current_themes = []    # Stores tuple with theme and variation number - eg. (person1,2)
    
    current_actor_ypos = 160
    custom_actor_ypos = 460

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
        for file in listdir(THEME_DIR):
            matches = theme_regexp.match(file)
            xpos = 100
            if (matches != None):
                # uses group(0) for full filename, group(1) for theme name
                self.available_themes.append(matches.group(1))
                # Add default image (theme 00 down 01) as actor
                self.available_theme_actors.append(Actor(img_file_format.format(matches.group(1), "00", "down", "01")+".png", (xpos,self.custom_actor_ypos)))
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
                self.current_theme_actors.append(Actor(img_file_format.format(matches.group(1), matches.group(2), "down", "01")+".png", (xpos,self.current_actor_ypos)))
                xpos += 100
            
        

    def draw(self, screen):
        screen.blit(self.background_img, (0,0))
        screen.draw.text('Custom Character', fontsize=60, center=(400,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        
        screen.draw.text('Existing Character', fontsize=40, center=(400,120), shadow=(1,1), color=(255,255,255), scolor="#202020")      
        for i in range (0,len(self.current_theme_actors)):
            self.current_theme_actors[i].draw()
            
        screen.draw.text('Customize Character', fontsize=40, center=(400,400), shadow=(1,1), color=(255,255,255), scolor="#202020")      
        for i in range (0,len(self.available_theme_actors)):
            self.available_theme_actors[i].draw()
        
    
    def update(self, keyboard):
        if (self.pause_timer.getTimeRemaining() > 0):
            return
        if (keyboard.space or keyboard.lshift or keyboard.rshift or keyboard.lctrl or keyboard.RETURN):
            return 'menu'
    
    def mouse_move (self,po):
        pass
    
    def mouse_click (self,pos):
        pass
    
    def select(self):
        self.pause_timer.startCountDown()