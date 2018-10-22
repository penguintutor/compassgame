from timer import Timer


class HighScore():
    
    background_img = "background_settings_01"

    # If set to true then print error message to console if unable to write to high score file
    debug = True
    
    high_score_values = []
    high_score_names = []
    

    def __init__(self, filename):
        self.filename = filename
        # Setup high score when created
        self.loadHighScore()
        # Timer restrict keyboard movements to every 1/2 second (prevent multiple presses)
        self.pause_timer = Timer(0.25)
        
    # indicate we change to this display mode
    # starts timer to prevent next click exit
    def select(self):
        self.pause_timer.startCountDown()
        
    # Reads high scores from file and stores as lists 
    def loadHighScore(self):
        # Open file if it already exists
        try:
            file = open(self.filename, 'r')
            entries = file.readlines()
            file.close()
            for line in entries:
                (this_name, this_score_str) = line.split(',' , 1)  
                this_score_num = int(this_score_str)
                self.high_score_values.append(this_score_num)
                self.high_score_names.append(this_name)
            file_exists = True
        except:
            # If either doesn't exist or is corrupt add single dummy entry
            self.high_score_values.append(0)
            self.high_score_names.append("---")
        
    # Returns current high score
    def getHighScore(self):
        #return self.high_score
        pass
        
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
                    
    def draw(self, screen):
        screen.blit(self.background_img, (0,0))
        screen.draw.text('High Scores', fontsize=60, center=(400,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        self.showScores(screen, (200,120))
        
    # Draws scores directly onto screen. pos is the top left of the scores
    def showScores(self,screen, pos):
        screen.draw.text('Rank', fontsize=30, topleft=(pos[0],pos[1]), color=(0,0,0))
        screen.draw.text('Name', fontsize=30, topleft=(pos[0]+150,pos[1]), color=(0,0,0))
        screen.draw.text('Score', fontsize=30, topleft=(pos[0]+300,pos[1]), color=(0,0,0))
        for i in range (0,len(self.high_score_values)):
            screen.draw.text(str(i+1), fontsize=30, topleft=(pos[0],pos[1]+25+(20*i)), color=(0,0,0))
            screen.draw.text(self.high_score_names[i], fontsize=30, topleft=(pos[0]+150,pos[1]+25+(20*i)), color=(0,0,0))
            screen.draw.text(str(self.high_score_values[i]), fontsize=30, topright=(pos[0]+350,pos[1]+25+(20*i)), color=(0,0,0))
        
    
    def update(self, keyboard):
        if (self.pause_timer.getTimeRemaining() > 0):
            return
        if (keyboard.space or keyboard.lshift or keyboard.rshift or keyboard.lctrl or keyboard.RETURN):
            return 'menu'
    
    def mouse_move (self,po):
        pass
    
    def mouse_click (self,pos):
        pass