import yaml

CFG_FILE_FORMAT = "person_{}_theme.cfg"


# Loads and provides information on the theme
class ThemeDetails:
    
    # Keys is a list so it is indexed
    keys=[]
    about={}
    default_colours={}
    labels={}
    
    # colour options is an dictionary with array of tuples
    colour_options={}
    
    # don't change default colours - they belong to the theme
    # instead update current_colours

    
    def __init__(self, theme_dir):
        self.theme_dir = theme_dir
        self.theme_loaded = False
    
    
    # Loads colour config file for person
    def loadConfig (self, theme):
        self.theme = theme
        
        # Reset all these entries to prevent loading alongside existing
        self.keys=[]
        self.about={}
        self.default_colours={}
        self.labels={}
        self.colour_options={}
        
        try :
            filename = self.theme_dir+CFG_FILE_FORMAT.format(theme)
            
            with open(filename, 'r') as yaml_file:
                # theme_config is a dictionary
                theme_config = yaml.load(yaml_file)
    
            for key in theme_config['about']:
                self.about[key]=theme_config['about'][key]

            for key in theme_config['labels']:
                self.keys.append(key)
                self.labels[key]=theme_config['labels'][key]
            for key in theme_config['default_colours']:
                this_colour = tuple(map(int, theme_config['default_colours'][key].split(',')))
                self.default_colours[key]=this_colour
            
            # These are array within a dictionary
            for key in theme_config['colour_options']:
                temp_array = theme_config['colour_options']
                self.colour_options[key]=[]
                for this_colour_str in theme_config['colour_options'][key]:
                    this_colour = tuple(map(int, this_colour_str.split(',')))
                    self.colour_options[key].append(this_colour)

            self.custom_colours = self.default_colours.copy()

            # Simple check - if we haven't raised an exception then theme loaded
            # Doesn't check number of entries
            self.theme_loaded = True                                        
        except Exception as e:
            print ("Error loading theme "+theme)
            print (str(e))
            self.theme_loaded = False
                
    # Return all the CustomColours 
    def getCustomColours(self):
        return self.custom_colours
                
                
    def isThemeLoaded(self):
        return self.theme_loaded
        
        
    def getTheme(self):
        return self.theme
                
    # Returns dict of short label = full string
    def getLabels(self):
        return self.labels
        
    def getDefaultColour(self,key):
        return self.default_colours[key]
                
    # uses custom colours
    def getColour(self,key):
        return self.custom_colours[key]
    
    def setColour(self,key, colour):
        self.custom_colours[key] = colour
    
    def getKeys(self):
        return self.keys
        
    def numKeys(self):
        return len(self.keys)
        
    # This should be the same for any, but no guarentee in future so allows key
    def numColourOptions(self, key='default'):
        return len(self.colour_options[key])
        
    def getLabel(self, key):
        return self.labels[key]

    def getColourOptions(self, key):
        if (key in self.colour_options):
            return self.colour_options[key]
        else:
            return self.colour_options['default']
        