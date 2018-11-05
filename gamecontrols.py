from pgzero.keyboard import *
# Holds and stores the selected controls
# Works by having a method for each of the controls which tests if any selected
# Allows multiple key options for each key (eg. space and enter for jump / duck)

# Default keys provide a way to restore keys if they are corrupt
# either by deleting the config file, or from the command line
default_keys = {
    'escape' : [keys.ESCAPE],
    'jump': [keys.RETURN, keys.RSHIFT, keys.LCTRL],
    'duck': [keys.SPACE, keys.LSHIFT],
    'up': [keys.UP, keys.W],
    'down': [keys.DOWN, keys.S],
    'left': [keys.LEFT, keys.A],
    'right': [keys.RIGHT, keys.D],
    'pause': [keys.P]
}

#configured_keys 


class GameControls:
    
    def __init__(self):
        self.configured_keys = default_keys.copy()
        
        
    # Returns True if the key is pressed, else false
    def isPressed(self, keyboard, key):
        for this_key in default_keys[key]:
            if keyboard[this_key]:
                return True
        return False
        
    # Same as isPressed, but can test for multiple keys
    # keys must be array
    def isOrPressed(self, keyboard, keys):
        for i in range (0,len(keys)):
            for this_key in default_keys[keys[i]]:
                if keyboard[this_key]:
                    return True
        return False