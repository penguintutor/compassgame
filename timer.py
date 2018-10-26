import math
import time

# Simple count down timer, based on system clock

class Timer():
    
    # Debug allows print statements to monitor changes
    # Use for debugging higher level code
    # Only enable for the particular timer that you need to debug
    
    def __init__(self, set_time, debug=False):
        self.default_time = set_time        # default_time is what we revert to when reset
        self.set_time = set_time
        self.start_time = time.time()
        self.debug = debug
        self.printDebug("Init")
        
    # start count down, with optional parameter to replace the start_time value
    # -1 is used as a "magic number", this method should only be called with positive number
    # if it isn't given a number then -1 indicates no new time give
    def startCountDown(self, new_time = -1):
        if (new_time >= 0):
            self.set_time = new_time
        self.start_time = time.time()
        self.printDebug("Timer started")

    # Returns time remaining note full accuracy - if need only seconds use math.floor
    def getTimeRemaining(self):
        # Set time - diff start and current time (as current time is bigger)
        current_time = self.set_time + self.start_time - time.time()
        self.printDebug("Time remaining: "+str(current_time))
        if (current_time <= 0): 
            return 0
        return current_time
        
    def resetToDefault(self):
        self.startCountDown(self.default_time)
        self.printDebug()
    
    # Return the default (ie normal start time)
    def getDefaultTime(self):
        self.printDebug()
        return self.default_time

    
    # Return the current start time
    def getSetTime(self):
        self.printDebug()
        return self.set_time
        
        
    def enableDebug(self):
        self.debug = True
        
    def disableDebug(self):
        self.debug = False
    
    def printDebug(self, extra=""):
        if (not self.debug):
            return
        print ("Timer set = "+str(self.set_time)+" Timer time = "+str(self.start_time)+" "+extra)