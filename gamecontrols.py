import pickle
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
    
    def __init__(self, filename):
        self.filename = filename
        self.configured_keys = default_keys.copy()
        self.loadControls()
        
    # Controls (if it exists) is a pickle file  
    def loadControls(self):
        try:
            with open(self.filename, 'rb') as infile:
                self.configured_keys = pickle.load(infile)
        except:
            self.configured_keys = default_keys.copy()
            
        
    # Replaces current file with configured_keys
    def saveControls(self):
        try:
            with open(self.filename, "wb") as outfile:
                pickle.dump (self.configured_keys, outfile, pickle.HIGHEST_PROTOCOL)
        except Exception (e):
            print ("Save custom controls failed")
            print (str(e))
            
        
        
    # Returns True if the key is pressed, else false
    def isPressed(self, keyboard, key):
        for this_key in self.configured_keys[key]:
            if keyboard[this_key]:
                return True
        return False
        
    # Same as isPressed, but can test for multiple keys
    # keys must be array
    def isOrPressed(self, keyboard, keys):
        for i in range (0,len(keys)):
            for this_key in self.configured_keys[keys[i]]:
                if keyboard[this_key]:
                    return True
        return False
        
        
        
    def getKeys(self):
        return self.configured_keys
        
        
                
    def getKeyString(self,index):
        return_string = ""
        for this_entry in self.configured_keys[index]:
            return_string += str(this_entry)+" "
        return return_string
        
    def setKey(self, key, keycode):
        self.configured_keys[key] = [keycode]