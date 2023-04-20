# Floor Jumper
**_Floor Jumper_** is a simple game written as a learning project for Python using the pygame module.  It is **_vaguely_** inspired by the game Ice-Climber for the NES.  I am not new to programming, but I am a neophyte when it comes to python.  This means while I've tried to embrace the python way of doing things, I probably regressed in places due to old habits in other languages.

**Objective:** Reach the top level by breaking blocks from beneath, then jumping on top.  Avoid the green blob enemies which will send you back to the bottom.  The player can kill blobs when they are on blocks destroyed by the player.

*Demo*

![](http://i.imgur.com/6IYe49H.gif)

## Running the Game
You will need the pygame and python 3.6 installed, as well as the images from my repository (e.g. .\\images\\*) wherever you copy the scripts.  Cloning the repository is the easiest method, or download the whole thing.  I don't have a lot of "extra" stuff in the repo

```
python3 main.py
```

## File Descriptions
Each file contains only one class, or a collection of related functions.  The brief overview of each is listed below.

### main.py
This is the main entry point for the game.  It creates the top level objects and contains the main game loop.  Start here if you want to trace through execution via code inspection or the debugger.

### game_functions.py
Inspired by a project in the *Python Crash Course* book, this module holds common game functions you're likely find in the main loop, such as updating all objects, drawing all objects, handling input, etc.

### settings.py
Likewise inspired - this caches common settings for the game, such as the dimensions of a tile, the player sprite attributes, etc

### image_resources.py
Loads images from disk and caches them for later use.  Also has a helper to split images into a list of frames for animated sprites.

### tilemap.py
This is a traditional 2D tilemap.  It takes a list of tiles (loaded via image_resources) and a list of integers representing a layout.  The tilemap also owns all game related objects, such as the player, the enemies, the blocks, etc.

### block.py
The simplest of sprites: it has only 1 image and once placed never moves.  It can only be removed, or used as a platform.

### animation.py
Tracks animation sequences for sprites with multiple sets of frames (walking left vs right vs jumping, etc).  This really boils down to managing a list of integers.  Not exciting, but needed.

### animated_sprite.py
This is a base-class shared by the 3 classic sprites in the game (the player, the enemies, and the blade).  Common physics code (simple gravity) and bounds/collision checking is done here.  There are hooks to allow the derived classes to behave differently on updates or collisions.

### blob_enemy.py
The simplest of animated sprites, it only has 3 modes: walking left, walking right, and falling.  It shares common collision detection for the map boundary and the blocks, but it alone can fall through the lower grate.

### player.py
A more complex animated sprite.  The player has more animations, reacts to input from the user, and must interact with the block objects to both destroy (from the bottom) or stand on (from the top).

### particle.py
A simple class representing a single particle.  For Floor Jumper, this is a filled 2D rect of a given color.

### particle_generator.py
The ParticleGenerator class is responsible for creating and tracking Particle objects.  A calling object may specify a callback to customize the particles generated, e.g. their velocities and color.

### blob_exit.py
This class encapsulates the animated blade and the particle generator when an enemy sprite is dropped into the drain of the tilemap.  When struck, the particle generator will emit particles for a set number of frames, constrained to give it a reaslistic look.  (The behavior can be changed and is by default here in this class).

### flyin_sprite.py
A simple static image sprite that moves to a final position over a number of frames.  Other classes inherit from FlyInSprite and provide the image and the movement data.

### level_sprite.py
Dead simple static flyin sprite with "LEVEL" text.  This is a portion of the level display.

### digit_sprite.py
Slightly more complex flyin sprite which can update its current static image (much like the animated case, but triggered on action and not frame count).  This is used to represent a single digit 0-9.

### level_info.py
Container class for the sprites that fly in for the current level display.  It consists of 2 digit sprites and the level text.  Each sprite flies in on a different path and come together to form the display.  This is triggered on game reset and once the player reaches the top of the map and advances levels.

### level_timer.py
Container class for a frame background image and several digit images (different iamges from the level digits, but same code driving it) which represent the time spent on the current level MM:SS:hh

### time_bonus.py
Text appearing above slain foes showing a time bonus reduction.  It slowly flashes and rises before vanishing.  The bonus is reflected in the level_timer



