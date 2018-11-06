# Used by GameMenu

class MenuItem:
    
    page = ''
    
    # Text is the text label to show to the user
    # command is instruction to run or label of submenu (eg. 'instructions')
    # menu_type is what kind of entry it is eg. 'submenu', 'command'(return string), 'textpage' or 'subcommand' (command run within the menu) 
    def __init__ (self, text, command, menu_type):
        self.text = text                                                                                     
        self.command = command
        self.menu_type = menu_type
        
        
    def getText(self):
        return self.text
        
    def getCommand(self):
        return self.command
        
    def getMenuType(self):
        return self.menu_type
        
    def setPage(self, text):
        self.page = text
        
    # Only available for textpage
    def getPage(self):
        if self.menu_type != 'textpage':
            return ""
        else:
            return self.page