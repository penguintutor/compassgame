from timer import Timer

class CustomControls:
    
    def __init__(self):
        # Timer restrict keyboard movements to fraction of second to prevent multiple presses
        self.pause_timer = Timer(0.15)


    def draw(self, screen):
        pass
    
    def update(self, keyboard):
        return 'menu'
    
    def mouse_move (self,po):
        pass
    
    def mouse_click (self,pos):
        pass
    

    def select(self):
        self.pause_timer.startCountDown()