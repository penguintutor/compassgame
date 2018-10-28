import yaml

CFG_FILE_FORMAT = "person_{}_theme.cfg"


# Loads and provides information on the theme
class ThemeDetails:
    
    # Keys is a list so it is indexed
    keys=[]
    about={}
    default_colours={}
    labels={}
    
    def __init__(self, theme_dir):
        self.theme_dir = theme_dir
        self.theme_loaded = False
    
    
    # Loads colour config file for person
    def loadConfig (self, theme):
        try :
            filename = self.theme_dir+CFG_FILE_FORMAT.format(theme)
            
            with open(filename, 'r') as yaml_file:
                # theme_config is a dictionary
                theme_config = yaml.load(yaml_file)
    
            for about in theme_config['about']:
                for key in about:
                    self.about[key]=about[key]
                    #print ("About key: "+key+" value: "+about[key])
            for labels in theme_config['labels']:
                for key in labels:
                    self.keys.append(key)
                    self.labels[key]=labels[key]
                    #print ("Label key: "+key+" value: "+labels[key])
            for def_colours in theme_config['default_colours']:
                for key in def_colours:
                    this_colour = tuple(map(int, def_colours[key].split(',')))
                    self.default_colours[key]=this_colour
                    #print ("Colour key: "+key+" value: "+str(this_colour))
            # Simple check - if we haven't raised an exception then theme loaded
            # Doesn't check number of entries
            self.theme_loaded = True                                        
        except:
            self.theme_loaded = False
                
                
    def isThemeLoaded(self):
        return self.theme_loaded
                
    # Returns dict of short label = full string
    def getLabels(self):
        return self.labels
                
    def getColour(self,key):
        return self.default_colours[key]
        
    def getKeys(self):
        return self.keys
        
    def getLabel(self, key):
        return self.labels[key]

        