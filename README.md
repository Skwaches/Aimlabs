# Intro 
Hello User, this is Skwaches. This is a really bad aimlabs (https://aimlabs.com/) ripoff.
Its also my first game.
For any compliments get to me via email -->kwach.jaduar@gmail.com

# Dependencies
* `Pygame`
  
# Sources
* Images files are sourced from unsplash. (https://unsplash.com/)
* Audio files are from pixabay. (https://pixabay.com/)
* Font files are from monaspace.(https://github.com/githubnext/monaspace)

# How to play
* Build from source with pyinstaller.
* Unzip the Game folder into any location.
* Open the file named "Skwaches' Game" (Application) in the unzipped game folder, this should open the game window.
* If an asset isn't loaded properly, the game will still run without it.
* Pressing F11 toggles fullscreen. 

Once the game window  is open you should first enter your username. You cannot play without selecting a username.
Start button should appear after successfully entering your username.
Change game mode if you want (Time limited, survival)  is the default.

## Game modes
* Time limited mode makes the game end after the selected time elapsed. (DEFAULT Max Time = 30seconds)
* Dot limited mode makes the game end after all the dots have appeared. (DEFAULT dots = 10) 
* Survival mode causes the button position to reset 1 second of the previous on being clicked.

You can change the time limit or dot limit by pressing the displayed button next to it and entering valid value. (Valid values are values >= 10)

## High scores
Clear button erases all registered scores PERMANENTLY.  _Reads `Wipe db` on hover_

## Settings
Feel free to change font's, background images and volume via settings.

## Customizing
* Do not rename any file or folder except the .exe file
* To play your own custom background music move the desired mp3 file into the Game_Audio\background_music folder. _It selects and plays songs in a random order_
* For custom sound effects move the desired mp3 file into sound_effect_folder and delete the default mp3 file      _Only one will play at a time_
* Same thing for background images.

## Restarting
The game sets all modified values to default.
Only scores are stored.
