class HighScore():

    # If set to true then print error message to console if unable to write to high score file
    debug = True

    def __init__(self, filename):
        self.filename = filename
        # Setup high score when created
        self.loadHighScore()
        
    # Reads high score from file and returns as a number
    def loadHighScore(self):
        # Open file if it already exists
        try:
            file = open(self.filename, 'r')
            entry = file.readline()
            file.close()
            self.high_score = int(entry)
            file_exists = True
        except:
            # If either doesn't exist or is corrupt
            self.high_score = 0       
        return self.high_score
        
    # Returns current high score
    def getHighScore(self):
        return self.high_score
        
    # Writes a high score to the file
    def setHighScore(self, new_score):
        # Set high score even if unable to save
        self.high_score = new_score
        try:
            with open(self.filename, 'w') as file:
                file.write(str(self.high_score))
        except:
                # Unable to write to file - warn to console
                if (self.debug == True):
                    print ("Unable to write to file "+self.filename+" high scores will not be saved")