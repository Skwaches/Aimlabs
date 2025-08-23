import pygame
import gamefuncs
import random
import highscoreSDK
import os
from functools import partial
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
back_img_paths = [os.path.join(back_img_dir,back_img_file) for back_img_file in back_img_files]
back_img_paths = list(filter(gamefuncs.is_valid_image,back_img_paths))

background_images_fullscreen = [gamefuncs.fit(pygame.image.load(back_img_path).convert(),ful) for back_img_path in back_img_paths]
background_images_windowed   = [gamefuncs.fit(pygame.image.load(back_img_path).convert(),default) for back_img_path in back_img_paths]

##Sound effects
pop_sound_dir = os.path.join(audio_dir,"sound_effects","pop_effect")
pop_sound_files = os.listdir(pop_sound_dir)
pop_sound_paths = [os.path.join(pop_sound_dir,pop_sound_file) for pop_sound_file in pop_sound_files if pop_sound_file.endswith("mp3")]
pop_sounds = [pygame.mixer.Sound(pop_sound_path) for pop_sound_path in pop_sound_paths]

button_sound_dir = os.path.join(audio_dir,"sound_effects","button_effect")
button_sound_files = os.listdir(button_sound_dir)
button_sound_paths = [os.path.join(button_sound_dir,button_sound_file) for button_sound_file in button_sound_files]
button_sounds = [pygame.mixer.Sound(button_sound_path) for button_sound_path in button_sound_paths]

key_sound_dir = os.path.join(audio_dir,"sound_effects","key_effect")
key_sound_files = os.listdir(key_sound_dir)
key_sound_paths = [os.path.join(key_sound_dir,key_sound_file) for key_sound_file in key_sound_files if key_sound_file.endswith("mp3")]
key_sounds = [pygame.mixer.Sound(key_sound_path) for key_sound_path in key_sound_paths]

# --- State Variables ---
timing = False            # Is the game timer running?
fullscreen = False        # Is the game in fullscreen mode?
running = True            # Main loop control
start_trigger = False    # Start button pressed
typing = False            # Is the user typing their name?
suggestions_button_dicts = dict[str,gamefuncs.Button]() # Dict for suggestion buttons
suggestions_trigger_dict = dict[str,bool]()  # Dict for button triggers
suggestions = list[str]()               # Username suggestions
i = 0                         # Error animation step
def_pos = (0, 0)              # Default position for blitting
text_input = str()           # User input text
ball_radius = 20                   # Ball radius
max_time = 30*1000               # Max time per round (ms)
start_time = 0                # Time when round started
current_time = 0              # Current elapsed time (ms)
points = 0                    # Player score
user_available = False        # Is a user selected?
x = random.randint(ball_radius, default[0] - ball_radius)       # Ball X position
y = random.randint(30 + ball_radius, default[1] - ball_radius)  # Ball Y position
typing_trigger = False        # Enter button pressed
accurate = False              # Mouse is over the ball
time_up = False               # Has the timer run out?
button_color :list[str|tuple[int,int,int]]= [(0,0,50),(0,0,20)]
text_color  :list[str|tuple[int,int,int]]= ["Grey","White"]
ball_color:list[str|tuple[int,int,int]]= [(200, 245, 190),(150, 195, 140)]
exit_sett_cords = (0,0)
show_start_text = False
show_settings   = False
instr_disp_time = 2000
sett_trigger = False
button_radius = 10
sugg_button_color:list[str|tuple[int,int,int]] = ["grey","dark grey"]
sugg_text_color:list[str|tuple[int,int,int]] = [(0,0,0),(10,10,10)]
suggestion_button_radius = 0
def_button = partial(gamefuncs.Button,screen,font,button_dimens,button_color,text_color,button_radius)
def_suggesion = partial(gamefuncs.Button,screen,font,button_dimens,sugg_button_color,sugg_text_color,suggestion_button_radius)
def_circle = partial(gamefuncs.my_circle,screen,ball_radius,ball_color)
##Defaulf in game adjustables
sel_back_img  = 0
sel_pop_sound = 0
sel_button_sound = 0
sel_key_sound = 0
eff_volume = 0.8
music_volume = 1

instr_text = "Click As Many\nCircles As You Can!"
lines = instr_text.split("\n")
clock = pygame.time.Clock()
fps = 100

##### Game Modes Logic
"""_summary_
Main modes: Time is limited, number of dots is limited or BOTH.:::
Sub-modes : Whether the dots disappear after a time delay or not.:::
"""
time_limited = True
dot_limited  = False
exit_sett_trigger = False
button_triggers = [] #game_triggers = [typing_trigger,sett_trigger,exit_sett_trigger,start_trigger] + [trigger for _,trigger in suggestions_trigger_dict]

#TESTS WITHIN LOOP
testing = True
test_delay = 2000
TEST_EVENT = pygame.USEREVENT+1
if testing: 
    pygame.time.set_timer(TEST_EVENT,test_delay)
def test():
    print(suggestions_trigger_dict,typing_trigger)
while running:
    instr = [font.render(lines[k],True,"White") for k in range(len(lines))]
    instr_centre = [(ful[0]//2,ful[1]//2+instr[k-1].get_height()*k) if fullscreen else (default[0]//2,default[1]//2+instr[k-1].get_height()*k) for k in range(len(lines))]

    instr_rect = [instr[k].get_rect(center = instr_centre[k]) for k in range(len(lines))]
    # --- Timing and State Updates ---
    if timing:
        current_time = pygame.time.get_ticks() - start_time
    # Get all users and suggestions for username input
    time_up = current_time >= max_time
    accurate = gamefuncs.point_in_circle((x, y), ball_radius, pygame.mouse.get_pos())

    # --- Button and Ball Dictionaries (for draw_button) ---
    # Calculate button positions based on screen mode
    start_cords = (default[0] - button_dimens[0], default[1] - button_dimens[1]) if not fullscreen else (ful[0] - button_dimens[0], ful[1] - button_dimens[1])
    enter_cords = (0, default[1] - button_dimens[1]) if not fullscreen else (0, ful[1] - button_dimens[1])
    settings_cords=(0,0)

    button_triggers = [typing_trigger,sett_trigger,exit_sett_trigger,start_trigger] + [suggestions_trigger_dict[trigger] for trigger in suggestions_trigger_dict]

    # Button dictionaries
    start_butt = def_button(start_cords,["Start","Start?"])
    enter_butt = def_button(enter_cords,[("Enter" if not user_available else "Switch") if not typing else text_input,("Enter?" if not user_available else "Switch?") if not typing else text_input]) 
    settings_butt = def_button(settings_cords,["Settings","Settings?"])
    exit_sett_butt = def_button(exit_sett_cords,["Exit","Exit?"])
    ball_butt = def_circle((x,y))
    
    
    ####CLEAR EVERYTHING
    suggestions_button_dicts.clear()
    ### SET NEW VALUES
    if typing:
        suggestions = highscoreSDK.my_searcher(text_input) if typing else list[str]()
        if suggestions:
            idx = 1
            for a_suggestion in suggestions:
                suggestion_button =  def_suggesion((enter_cords[0], enter_cords[1] - button_dimens[1] * idx), [f"{a_suggestion}",f"{a_suggestion}?"]) #Create button object for each suggestion and store it in the dict under the suggestion name
                suggestions_button_dicts[a_suggestion] = suggestion_button
                idx += 1
   

   #Event Handling
    for event in pygame.event.get():
        if testing and event.type == TEST_EVENT:
            test()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not show_settings:
            
            if event.key == pygame.K_F11:
                # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(default)
            if typing:
                key_sounds[sel_key_sound].play()
                # Handle text input for username
                if event.key == pygame.K_RETURN:
                    user_available = bool(text_input)
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += (event.unicode).strip()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if any(button_triggers):
                button_sounds[sel_button_sound].play()
            if typing:
                # Handle suggestion clicks  
                if any(suggestions_trigger_dict.values()):
                    for var in suggestions_trigger_dict:
                        if suggestions_trigger_dict[var]:
                            text_input = var
                            user_available = True
                            typing = False
                            suggestions_trigger_dict.clear()
                            break
                elif not typing_trigger:
                    typing = False
            if typing_trigger:
                # Enter button pressed to start typing
                typing = True
            if start_trigger:
                # Start button pressed to begin game
                show_start_text=True
                start_trigger = False
                timing = False
                current_time = 0
                points = 0
            if sett_trigger:
                show_settings = True
            if exit_sett_trigger:
                print("Exit requested")
                show_settings = False
                exit_sett_trigger = False
            if accurate and timing:
                # Ball clicked during game
                pop_sounds[sel_pop_sound].play()
                if fullscreen:
                    x = random.randint(ball_radius, ful[0] - ball_radius)
                    y = random.randint(30 + ball_radius, ful[1] - ball_radius)
                else:
                    x = random.randint(ball_radius, default[0] - ball_radius)
                    y = random.randint(30 + ball_radius, default[1] - ball_radius)
                points += 1

    
    # --- Drawing ---
    # Set background
    if fullscreen:
        screen.blit(background_images_fullscreen[sel_back_img],def_pos)
    else:
        screen.blit(background_images_windowed[sel_back_img],def_pos)

    if not show_settings: 
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
                if x > default[0] - ball_radius:
                    x = random.randint(ball_radius, default[0] - ball_radius)
                if y > default[1] - ball_radius:
                    y = random.randint(ball_radius, default[1] - ball_radius)
            pygame.draw.circle(screen, (200, 245, 190) if not accurate else (150, 195, 140), (x, y), ball_radius)
            if time_up:
                highscoreSDK.add_scores(text_input, points)
                timing = False
        else:
            # Draw enter and settings button
            typing_trigger = gamefuncs.Button.draw(enter_butt)
            sett_trigger   = gamefuncs.Button.draw(settings_butt)

            
            if typing:# Draw suggestion buttons if typing
                ##CLEAR EVERYTHING
                suggestions_trigger_dict.clear()
                ##SET NEW VALUES
                if suggestions:
                    for a_suggestion in suggestions_button_dicts:
                        suggestions_trigger_dict[a_suggestion] = gamefuncs.Button.draw(suggestions_button_dicts[a_suggestion]) 
                
            
            
            # Draw start button if user is available and not typing and game not runnin
            if user_available and not typing:
                    start_trigger = gamefuncs.Button.draw(start_butt)
                
    else:
        exit_sett_trigger = gamefuncs.Button.draw(exit_sett_butt)
    
     # --- Event Handling ---

    pygame.display.update()

