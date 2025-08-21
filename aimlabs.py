import pygame
import gamefuncs
import random
import highscoreSDK
import os
from enum import Enum
# --- Setup ---
pygame.init()
pygame.mixer.init()
game_dir = os.getcwd()
img_dir = os.path.join(game_dir, "Game_images")
audio_dir = os.path.join(game_dir, "Game_Audio")
default = (800, 400)
ful = (1600, 900)
button_dimens = (160, 40)
font_size = 25
font = pygame.font.SysFont("Monaspace Radon", font_size)
screen = pygame.display.set_mode(default)
pygame.display.set_caption("Aim Game")

# Load resources
##Songs
music_dir   = os.path.join(audio_dir,"background_music")
music_files = os.listdir(music_dir)
music_paths = [os.path.join(music_dir, music_files[k]) for k in range(len(music_files)) if music_files[k].endswith(".mp3")]

##Images
back_img_dir=os.path.join(img_dir,"background_img")
back_img_files = os.listdir(back_img_dir)
back_img_paths = [os.path.join(back_img_dir,back_img_files[k]) for k in range(len(back_img_files)) if gamefuncs.is_valid_image(os.path.join(back_img_dir,back_img_files[k]))]
background_images_fullscreen = [gamefuncs.fit(pygame.image.load(back_img_paths[k]).convert(),ful) for k in range(len(back_img_paths))]
background_images_windowed  = [gamefuncs.fit(background_images_fullscreen[k],default) for k in range(len(background_images_fullscreen))]
game_over = gamefuncs.fit(pygame.image.load(os.path.join(img_dir, "Game over screen.jpg")).convert(), ful)
res_over = gamefuncs.fit(game_over, default)

##Sound effects
sound_effects_dir = os.path.join(audio_dir,"sound_effects")
sound_effects_files = os.listdir(sound_effects_dir)
sound_effects_paths = [os.path.join(sound_effects_dir,sound_effects_files[k]) for k in range(len(sound_effects_files)) if sound_effects_files[k].endswith("mp3")]
ball_pop_effect = [pygame.mixer.Sound(sound_effects_paths[k]) for k in range(len(sound_effects_paths))]
for k in range(len(ball_pop_effect)):
    ball_pop_effect[k].set_volume(1.0)

def play_random_song():
    """Play a random song from the music directory, excluding bubble pop."""
    if music_paths:
        song = random.choice(music_paths)
        pygame.mixer.music.load(song)
        pygame.mixer.music.set_volume(0.6)  # Lower volume so bubble pop is audible
        pygame.mixer.music.play(-1)

def stop_song():
    pygame.mixer.music.stop()

# Start with a random song (not bubble pop) when not playing
play_random_song()

# --- State Variables ---
timing = False            # Is the game timer running?
fullscreen = False        # Is the game in fullscreen mode?
running = True            # Main loop control
start_trigger = False     # Start button pressed
typing = False            # Is the user typing their name?
error = False             # Is an error message being shown?
forward = True            # Error animation direction
backward = False          # Error animation direction
suggestions_button_dicts = {}  # Dict for suggestion buttons
trigger_dict = {}              # Dict for button triggers
suggestions = []               # Username suggestions
err_delay = 700                # Error animation delay
i = 0                         # Error animation step
def_pos = (0, 0)              # Default position for blitting
text_input = ""               # User input text
error_text = ""               # Error message text
radius = 20                   # Ball radius
max_time = 30*1000               # Max time per round (ms)
start_time = 0                # Time when round started
current_time = 0              # Current elapsed time (ms)
points = 0                    # Player score
increment = 1                 # Error animation increment
ERROR_EVENT = pygame.USEREVENT + 1  # Custom event for error animation
user_available = False        # Is a user selected?
x = random.randint(radius, default[0] - radius)       # Ball X position
y = random.randint(30 + radius, default[1] - radius)  # Ball Y position
typing_trigger = False        # Enter button pressed
accurate = False              # Mouse is over the ball
start_dict = {}               # Start button dict
ball_dict = {}                # Ball dict
enter_dict = {}               # Enter button dict
time_up = False               # Has the timer run out?

show_start_text = False
show_settings = False
instr_disp_time = 2000
sel_back_img  = 0
sel_sound_eff = 0
instr_text = "Click As Many\nCircles As You Can!"
lines = instr_text.split("\n")
pygame.time.set_timer(ERROR_EVENT, err_delay)
clock = pygame.time.Clock()
fps = 100

##### Game Modes Logic
"""_summary_
Main modes: Time is limited or number of dots is limited or BOTH.:::
Sub-modes : Whether the dots disappear after a time delay or not.:::
"""
time_limited = True
dot_limited  = False


while running:
    instr = [font.render(lines[k],True,"White") for k in range(len(lines))]
    instr_centre = [(ful[0]//2,ful[1]//2+instr[k-1].get_height()*k) if fullscreen else (default[0]//2,default[1]//2+instr[k-1].get_height()*k) for k in range(len(lines))]

    instr_rect = [instr[k].get_rect(center = instr_centre[k]) for k in range(len(lines))]
    # --- Timing and State Updates ---
    if timing:
        current_time = pygame.time.get_ticks() - start_time
    # Get all users and suggestions for username input
    suggestions = highscoreSDK.my_searcher(text_input)
    time_up = current_time >= max_time
    accurate = gamefuncs.point_in_circle((x, y), radius, pygame.mouse.get_pos())

    # --- Music Control ---
    if timing:
        # If just started timing, pick a new random song for gameplay
        if not pygame.mixer.music.get_busy():
            play_random_song()
        # Lower music volume so bubble pop is clear
        pygame.mixer.music.set_volume(0.4)
    else:
        # Not playing: ensure music is playing at normal volume
        if not pygame.mixer.music.get_busy():
            play_random_song()
        pygame.mixer.music.set_volume(0.7)

    # --- Button and Ball Dictionaries (for draw_button) ---
    # Calculate button positions based on screen mode
    start_cords = (default[0] - button_dimens[0], default[1] - button_dimens[1]) if not fullscreen else (ful[0] - button_dimens[0], ful[1] - button_dimens[1])
    enter_cords = (0, default[1] - button_dimens[1]) if not fullscreen else (0, ful[1] - button_dimens[1])
    settings_cords=(ful[0]-button_dimens[0],(ful[1]-button_dimens[1])//2) if fullscreen else (default[0]-button_dimens[0],(default[1]-
    button_dimens[1])//2)

    start_dict = {
        "dimens": button_dimens, "screen": screen, "font": font, "cords": start_cords,
        "text_on": "Start?", "text_off": "Start", "color_off": (50, 0, 0), "color_on": (20, 0, 0),
        "textcoloron": "Grey", "textcoloroff": "white"
    }
    ball_dict = {
        "surface": screen, "color": (200, 245, 190) if not accurate else (150, 195, 140),
        "center": (x, y), "radius": radius
    }
    enter_dict = {
        "dimens": button_dimens, "screen": screen, "font": font, "cords": enter_cords,
        "text_on": ("Enter?" if not user_available else "Switch?") if not typing else text_input,
        "text_off": ("Enter" if not user_available else "Switch") if not typing else text_input,
        "color_off": (50, 0, 0), "color_on": (20, 0, 0) if not typing else (50,0,0), "textcoloron": "Grey" if not typing else "white", "textcoloroff": "white"
    }
    settings_dict = {"dimens": button_dimens, "screen": screen, "font": font, "cords": settings_cords,
                 "text_on": "Settings?","text_off": "Settings","color_off": (50, 0, 0), "color_on": (20, 0, 0),
                 "textcoloron": "grey", "textcoloroff": "white"}
   
    # --- Suggestions Buttons ---
    if typing:
        if suggestions:
            suggestions_button_dicts.clear()
            idx = 1
            for a_suggestion in suggestions:
                suggestions_button_dicts[a_suggestion] = {
                    "dimens": button_dimens, "screen": screen, "font": font,
                    "cords": (enter_cords[0], enter_cords[1] - button_dimens[1] * idx),
                    "text_on": f"{a_suggestion}?", "text_off": f"{a_suggestion}",
                    "color_off": (150, 150, 150), "color_on": (70, 70, 70),
                    "textcoloron": (0, 0, 0), "textcoloroff": (10, 10, 10),"my_border_radius":0,
                }
                idx += 1
        else:
            suggestions_button_dicts.clear()

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(default)
            if typing:
                # Handle text input for username
                if event.key == pygame.K_RETURN:
                    user_available = bool(text_input)
                    if not user_available:
                        error = True
                        error_text = "No User entered"
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += (event.unicode).strip()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if typing:
                # Handle suggestion button clicks
                for var in trigger_dict:
                    if trigger_dict[var]:
                        text_input = var
                        user_available = True
                        typing = False
            elif typing_trigger:
                # Enter button pressed to start typing
                typing = True
            elif start_trigger:
                # Start button pressed to begin game
                show_start_text=True
                start_trigger = False
                timing = False
                current_time = 0
                points = 0
            elif sett_trigger:
                show_settings = not show_settings
            elif accurate and timing:
                # Ball clicked during game
                ball_pop_effect[sel_sound_eff].play()
                if fullscreen:
                    x = random.randint(radius, ful[0] - radius)
                    y = random.randint(30 + radius, ful[1] - radius)
                else:
                    x = random.randint(radius, default[0] - radius)
                    y = random.randint(30 + radius, default[1] - radius)
                points += 1
            
        if not forward:
            if event.type == ERROR_EVENT:
                backward = True

    # --- Error Animation ---
    if error:
        err_text = font.render(f"{error_text}", True, "White")
        err_dimens = (err_text.get_width(), err_text.get_height())
        error_box = pygame.Rect(((ful[0] - err_dimens[0]) / 2 if fullscreen else (default[0] - err_dimens[0]) / 2, 0), err_dimens)
        if forward:
            if i < error_box.height:
                error_box.topleft = (error_box.x, i - error_box.height)
                i += increment
            else:
                forward = False
                i = 0
        if backward:
            if i <= error_box.height:
                error_box.topleft = (error_box.x, -i)
                i += increment
            else:
                forward = True
                backward = False
                error = False
                i = 0

    # --- Drawing ---
    # Set background
    if not show_settings: 
        if fullscreen:
            screen.blit(background_images_fullscreen[sel_back_img],def_pos)
        else:
            screen.blit(background_images_windowed[sel_back_img],def_pos)

        # Draw error message if needed
        if error:
            pygame.draw.rect(screen, "Dark grey", error_box)
            screen.blit(err_text, err_text.get_rect(center=error_box.center))

        # Draw start instructions message
        if show_start_text:
            for k in range(len(lines)):
                screen.blit(instr[k],instr_rect[k])
            pygame.display.flip()
            pygame.time.wait(instr_disp_time)
            timing = True
            start_time = pygame.time.get_ticks()
            show_start_text = False

        # Draw score and timer
        if current_time:
            point_text = font.render(f"{points}", True, "White")
            point_box = pygame.Rect(((ful[0] if fullscreen else default[0]) - point_text.get_width(), 0), point_text.get_size())
            point_rect = point_text.get_rect(center=point_box.center)
            pygame.draw.rect(screen, "Black", point_box)
            screen.blit(point_text, point_rect)

            time_text = font.render(f"{current_time/1000:.2f} s", True, "White")
            time_box = pygame.Rect((def_pos), time_text.get_size())
            time_rect = time_text.get_rect(center=time_box.center)
            pygame.draw.rect(screen, "Black", time_box)
            screen.blit(time_text, time_rect)

        # Draw ball and handle game logic
        if timing:
            if not fullscreen:
                if x > default[0] - radius:
                    x = random.randint(radius, default[0] - radius)
                if y > default[1] - radius:
                    y = random.randint(radius, default[1] - radius)
            pygame.draw.circle(screen, (200, 245, 190) if not accurate else (150, 195, 140), (x, y), radius)
            if time_up:
                highscoreSDK.add_scores(text_input, points)
                timing = False
        else:
        # Draw enter button
            typing_trigger = gamefuncs.draw_button(**enter_dict)
        # Draw suggestion buttons if typing
        if typing:
            if suggestions:
                for suggest in suggestions_button_dicts:
                    trigger_dict[suggest] = gamefuncs.draw_button(**suggestions_button_dicts[suggest])
            else:
                suggestions_button_dicts.clear()
                trigger_dict.clear()
        # Draw start button if user is available and not typing
        if user_available and not typing:
                start_trigger = gamefuncs.draw_button(**start_dict)
                sett_trigger  = gamefuncs.draw_button(**settings_dict)
    else:
        screen.blit("Dark grey")
        
        
    pygame.display.update()

