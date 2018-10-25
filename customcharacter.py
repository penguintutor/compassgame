import re
from os import listdir

from timer import Timer

# Directories relative to the application directory
THEME_DIR = "themes/"
IMAGE_DIR = "images/"             # This is fixed for pgzero files
TMP_DIR = "tmp/"                # Used to hold temporary files used to show the different characters

CONVERT_CMD = "/usr/bin/convert"

class CustomCharacter:

    def __init__ (self, img_file_format):
        self.img_file_format = img_file_format
        # Create a regular expression to identify themes
        # does not use \w as do not include _ character
        # Look for image 0 (down 1) - other variants of the first number part is different colours
        self.available_themes = []
        self.current_themes = []    # Stores tuple with theme and variation number - eg. (person1,2)
        # Timer restrict keyboard movements to every 1/2 second (prevent multiple presses)
        self.pause_timer = Timer(0.25)
        
        # Load the themes - only look in the SVG folder
        theme_regexp_string = img_file_format.format("([a-zA-Z0-9]+)", "00", "down", "01")+".svg"
        theme_regexp = re.compile(theme_regexp_string)
        for file in listdir(THEME_DIR):
            matches = theme_regexp.match(file)
            if (matches != None):
                # uses group(0) for full filename, group(1) for theme name
                self.available_themes.append(matches.group(1))
                
        # Load the different variations on the themes currently available
        png_regexp_string = img_file_format.format("([a-zA-Z0-9]+)", "(\d2)", "down", "01")+".png"
        png_regexp = re.compile(png_regexp_string)
        print (png_regexp_string)
        for file in listdir(IMAGE_DIR):
            matches = png_regexp.match(file)
            if (matches != None):
                # uses group(0) for full filename, group(1) for theme name
                self.current_themes.append((matches.group(1),matches.group(2)))
                print ("Theme loaded {}, {}".format(matches.group(1), matches.group(2)))
            
        

    def draw(self, screen):
        pass
    
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