from timer import Timer


class HighScore():
    
    background_img = "background_settings_01"

    # If set to true then print error message to console if unable to write to high score file
    debug = True
    
    # Values is score as int and names is name of user (3 initials)
    # Must be ordered high to low
    high_score_values = []
    high_score_names = []
    
    max_entries = 10
    
    # Mode is normally display except when adding new score
    # in which case it is set to edit, then save when updating
    mode = 'display'
    
    

    def __init__(self, game_controls, filename):
        self.game_controls = game_controls
        self.filename = filename
        # Setup high score when created
        self.loadHighScore()
        # Timer restrict keyboard movements to fraction of second (prevent multiple presses)
        self.pause_timer = Timer(0.2)
        
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
        except Exception as e:
            # Unable to write to file - warn to console
            if (self.debug == True):
                print ("Unable to read file "+self.filename+" high scores will not be reset\n"+str(e))
            # If either doesn't exist or is corrupt add single dummy entry
            self.high_score_values.append(0)
            self.high_score_names.append("---")
        
    # Checks if high score is achieved
    def checkHighScore(self, new_score):
        # first make sure we have a score, otherwise don't enter
        if (new_score < 1): 
            return False
        # Check if we have space - if so then always a high score
        if (len(self.high_score_values) < self.max_entries):
            return True
        # Check if high score is higher than last entry 
        if (new_score > self.high_score_values[self.max_entries] - 1):
            return True
        return False
        
    # Initiates enter name mode
    def setHighScore(self, new_score):
        self.mode = 'edit'
        self.new_score = new_score
        # Name is initials - list of 3 characters
        self.new_name = ['-','-','-']
        self.char_selected = 0
        
    def saveHighScore(self):
        try:
            with open(self.filename, 'w') as file:
                for i in range (0,len(self.high_score_values)):
                    file.write(self.high_score_names[i]+","+str(self.high_score_values[i])+"\n")
        except Exception as e:
            # Unable to write to file - warn to console
            if (self.debug == True):
                print ("Unable to write to file "+self.filename+" high scores will not be saved\n"+str(e))

                    
    def draw(self, screen):
        screen.blit(self.background_img, (0,0))
        screen.draw.text('High Scores', fontsize=60, center=(400,50), shadow=(1,1), color=(255,255,255), scolor="#202020")
        y_pos = 120
        if (self.mode == 'edit'):
            screen.draw.text('New High Score '+str(self.new_score), fontsize=40, center=(400,120), color=(255,0,0))
            
            # Set colour for characters (so selected one is different colour)
            # Done using array 
            
            char_colours = [(255,0,0),(255,0,0),(255,0,0)]
            char_colours[self.char_selected] = (0,0,0)
            
            
            # Three characters for new name
            screen.draw.text(self.new_name[0], fontsize=40, center=(380,180), color=char_colours[0])
            # Three characters for new name
            screen.draw.text(self.new_name[1], fontsize=40, center=(400,180), color=char_colours[1])
            # Three characters for new name
            screen.draw.text(self.new_name[2], fontsize=40, center=(420,180), color=char_colours[2])
            
            y_pos = 240
        self.showScores(screen, (200,y_pos))
        
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
            return 'highscore'
        # If mouse clicked then exit to menu
        if (self.mode == 'clicked'):
            self.mode = 'display'
            return 'menu'
        if (self.mode == 'edit'):
            # Editing
            if (self.game_controls.isPressed(keyboard,'up')):
                self.new_name[self.char_selected] = self.charIncrement(self.new_name[self.char_selected])
                self.pause_timer.startCountDown()
            if (self.game_controls.isPressed(keyboard,'down')):
                self.new_name[self.char_selected] = self.charDecrement(self.new_name[self.char_selected])
                self.pause_timer.startCountDown()
            if (self.game_controls.isPressed(keyboard,'left')) :
                if (self.char_selected > 0) :
                    self.char_selected -= 1
                    self.pause_timer.startCountDown()
            if (self.game_controls.isPressed(keyboard,'right')) :
                if (self.char_selected < 2) :
                    self.char_selected += 1
                    self.pause_timer.startCountDown()
            # If save chosen (map / jump / enter)
            if (self.game_controls.isOrPressed(keyboard,['jump','duck'])):
                self.updHighScoreList()
                self.saveHighScore()
                self.mode = 'display'
                return 'menu'
            else:
                return 'highscore'
        if (self.game_controls.isOrPressed(keyboard,['jump','duck'])):
            return 'menu'
        return 'highscore'
    
    def mouse_move (self,pos):
        pass
    
    def mouse_click (self,pos):
        # mouse click returns to main menu
        self.mode = 'clicked'
    
    
    def updHighScoreList(self):
        added = False
        # Go down the list until we find an entry that is smaller and insert there
        for i in range (0,len(self.high_score_values)):
            if (self.high_score_values[i] < self.new_score):
                self.high_score_values.insert(i,self.new_score)
                self.high_score_names.insert(i,self.new_name[0]+self.new_name[1]+self.new_name[2])
                added = True
                break
        # If added is still false then need to add it to the bottom
        if (added == False):
            self.high_score_values.append(self.new_score)
            self.high_score_names.append(self.new_name[0]+self.new_name[1]+self.new_name[2])
        # If have more than max then drop the last entry
        if (len(self.high_score_values) > self.max_entries):
            self.high_score_values.pop()
            self.high_score_names.pop()
        # If last entry is score 0 then drop that as well (dummy entry)
        if (self.high_score_values[-1] == 0):
            self.high_score_values.pop()
            self.high_score_names.pop()
    
    
    #### To keep characters scrolling simple for user we only allow capital letters, numbers and -
    def charIncrement (self, current_char):
        if (current_char == '-') :
            return ('A')
        if (current_char == 'Z') :
            return ('0') 
        if (current_char == '9') :
            return ('-') 
        return chr(ord(current_char) + 1)
        
    def charDecrement (self, current_char):
        if (current_char == '-') :
            return ('9')
        if (current_char == 'A') :
            return ('-') 
        if (current_char == '0') :
            return ('Z') 
        return chr(ord(current_char) - 1)