import math
import time

# Simple count down timer, based on system clock

class Timer():
    
    def __init__(self, set_time):
        self.default_time = set_time        # default_time is what we revert to when reset
        self.set_time = set_time
        self.start_time = time.time()
        
    # start count down, with optional parameter to replace the start_time value
    # -1 is used as a "magic number", this method should only be called with positive number
    # if it isn't given a number then -1 indicates no new time give
    def startCountDown(self, new_time = -1):
        if (new_time >= 0):
            self.set_time = new_time
        self.start_time = time.time()

    # Returns time remaining to nearest second
    def getTimeRemaining(self):
        # Set time - diff start and current time (as current time is bigger)
        current_time = self.set_time + self.start_time - time.time()
        if (current_time <= 0): 
            return 0
        #return math.ceil(current_time)
        return math.floor(current_time)
        
    def resetToDefault(self):
        self.startCountDown(self.default_time)
    
    # Return the default (ie normal start time)
    def getDefaultTime(self):
        return self.default_time
    
    # Return the current start time
    def getSetTime(self):
        return self.set_time
    