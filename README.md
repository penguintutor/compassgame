# Compass Game
Compass Game is a game written in Python Pygame Zero for the Raspberry Pi.

Designed for use with a Picade joystick the game can also be played using the keyboard. 

![Screenshot of the compass game](http://www.penguintutor.com/projects/images/compassgame01.png)

## Install
Requires Pygame Zero to be installed (included on Raspberry Pi). 

Download the current version from: [GitHub Compass Game](https://github.com/penguintutor/compassgame/archive/master.zip)

Extract the files into a directory on you computer


## Play the game

Change to the directory used for install (cd)

Run using:

`pgzero compassgame.py`

Choose Play Game from the menu.

Follow the direction at the top of the screen.

Move the character using a joystick (Picade) or cursor keys. 
Press SPACE to duck
Press RIGHT SHIFT to view the map

Avoid the obstacles that appear on later levels


## Development
This program is currently under development. Further updates will include installation instructions for RetroPie (Picade).

Other plans include
* Reconfigurable keys
* Sound effects
* Alternative game mode (AI players)

# Features / Bugs etc.

## Joystick / keyboard only control
The game is intended to be played with a Joystick on the Picade or a keyboard. The mouse can be used in some of the configuration menus, but cannot be used in the game.

## Custom themes 
Customer themes can be added changing the characters in the game. There is a maximum of 7 themes. Any more will not be shown correctly. There can however be up to 99 variations on each theme.

### No option to delete custom themes
There is currently no way to delete custom characters. They will need to be manually deleted from the images folder (taking care not to remove the default character).

### Mouse does not work in custom character

### Importance of configuration rules
When creating a new theme the configuration rules need to be fully implemented as specified. This includes the default entry and that all colour options are of the same length.

### Ordering of customization colours
The order of the label options in the theme configuration file is ignored. This is a feature of the YAML parser used. As this is for a configuration and the option is clearly labelled on the configuration page this is not considered a bug. To fix this would either need a different YAML parser or an additional list that preserves ordering.

### Unique custom colours
All the colours used that can be customized have to be unique. These can be very similar (eg. just one differences in any of the red, green, blue values).

## User pause
The user pause option is not currently working

# More details

The project home page is at: [PenguinTutor Compass Game](http://www.penguintutor.com/projects/compass-game)