import pygame
import gamefuncs
import random
import highscoreSDK
import os
from functools import partial
#region --- Setup ---
running = True
pygame.init()
pygame.mixer.init()
default = (800, 400)
ful = (1600, 900)
button_dimens = (160, 40)
screen = pygame.display.set_mode(default)
pygame.display.set_caption("Skwaches' Aim Game")
#endregion

#Link directory
game_dir = os.getcwd()
img_dir = os.path.join(game_dir, "Game_images")
font_dir = os.path.join(game_dir,"Game_fonts")
audio_dir = os.path.join(game_dir, "Game_Audio")

#region --- StateAdjustable Variables ---
def_back_img  = 0
def_pop_sound = 0
def_button_sound = 0
def_key_sound = 0
def_font = "MonaspaceRadon-Regular.otf"
muted = False
music_volume = 0.7 if not muted else 0
sfx_volume = 0.8 if not muted else 0
font_size = 25
#endregion

#Loading resources

#region Fonts
font_files = os.listdir(font_dir)
font_paths = [os.path.join(font_dir,font_file) for font_file in font_files]
fonts      = {font_file:pygame.font.Font(font_path,font_size) for font_file,font_path in zip(font_files,font_paths) if gamefuncs.is_font_usable(font_path)}
font = fonts[def_font]
#endregion

#region Songs
music_dir   = os.path.join(audio_dir,"background_music")
music_files = os.listdir(music_dir)
music_paths = [os.path.join(music_dir, music_files[k]) for k in range(len(music_files)) if music_files[k].endswith(".mp3")]
#endregion

#region Images
back_img_dir=os.path.join(img_dir,"background_img")
back_img_files = os.listdir(back_img_dir)
back_img_paths = [os.path.join(back_img_dir,back_img_file) for back_img_file in back_img_files]
back_img_paths = list(filter(gamefuncs.is_valid_image,back_img_paths))
background_images_fullscreen = [gamefuncs.fit(pygame.image.load(back_img_path).convert(),ful) for back_img_path in back_img_paths]
background_images_windowed   = [gamefuncs.fit(pygame.image.load(back_img_path).convert(),default) for back_img_path in back_img_paths]
#end region

#region Sound effects
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
#endregion
#endregion

#Set SFX volume
for button_sound in button_sounds:
    button_sound.set_volume(sfx_volume)
for pop_sound in pop_sounds:
    pop_sound.set_volume(sfx_volume)
#endregion

#Play first song
current_music = random.choice(music_paths)
pygame.mixer_music.load(current_music)
pygame.mixer_music.play(0)
pygame.mixer_music.set_volume(music_volume)
#endregion


###-----SETTINGS------
sett_v_gap =100
sett_h_gap =30

#MUSIC
music_sett = font.render("Music",True,"White")
music_spot = pygame.rect.Rect((0,button_dimens[1]+sett_h_gap),button_dimens)
music_rect = music_sett.get_rect(center = music_spot.center)

music_held = False
music_trigger = False
music_rail = pygame.rect.Rect((music_spot.right+sett_v_gap,music_spot.top),(100,5))
music_start:int  = round(music_volume*(music_rail.width))+music_rail.left
music_rail.centery = music_spot.centery
music_slide_button = pygame.rect.Rect((music_start,music_rail.centery),(15,15))
music_colors:list[str|tuple[int,int,int]] = ["Dark grey","Green","White"]

music_slider = gamefuncs.Slider(music_slide_button,music_rail,music_colors,sld_wid=0,slider_border_radius=100)


#SFX
sfx_sett = font.render("Sfx vol",True,"White")
sfx_spot = pygame.rect.Rect((0,music_spot.bottom+sett_h_gap),button_dimens)
sfx_rect = sfx_sett.get_rect(center = sfx_spot.center)

sfx_held = False
sfx_trigger = False
sfx_rail = pygame.rect.Rect((sfx_spot.right+sett_v_gap,sfx_spot.top),(100,5))
sfx_start:int  = round(sfx_volume*(sfx_rail.width))+music_rail.left
sfx_rail.centery = sfx_spot.centery
sfx_slide_button = pygame.rect.Rect((sfx_start,sfx_rail.centery),(15,15))
sfx_colors:list[str|tuple[int,int,int]] = ["Dark grey","Green","White"]
sfx_slider = gamefuncs.Slider(sfx_slide_button,sfx_rail,sfx_colors,sld_wid=0)

#region
background_sett = font.render("Background img",True,"White")
background_spot = pygame.rect.Rect((0,music_spot.bottom+sett_v_gap),button_dimens)
background_rect = sfx_sett.get_rect(center = sfx_spot.center)
#endregion
#region Game Modes Logic
"""_summary_
Main modes: Time is limited, number of dots is limited or BOTH.:::
Sub-modes : Whether the dots disappear after a time delay or not.:::
"""
time_limited = True
dot_limited  = False


#endregion

#region INSTRUCTIONS
##Time limited instructions
instr_text = "Click As Many\nCircles As You Can!"
lines = instr_text.split("\n")
clock = pygame.time.Clock()
fps = 100
#endregion

#region TESTS WITHIN LOOP
testing = False
test_delay = 2000
TEST_EVENT = pygame.USEREVENT+1
if testing: 
    pygame.time.set_timer(TEST_EVENT,test_delay)
def test():
    pass
#endregion

#region --- State Non Adjustable Variables ---
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
exit_sett_trigger = False
button_triggers = [] #game_triggers = [typing_trigger,sett_trigger,exit_sett_trigger,start_trigger] + [trigger for _,trigger in suggestions_trigger_dict]
exit_sett_cords = (0,0)
show_start_text = False
show_settings   = False
instr_disp_time = 2000
sett_trigger = False
button_radius = 10
sugg_button_color:list[str|tuple[int,int,int]] = ["grey","dark grey"]
sugg_text_color:list[str|tuple[int,int,int]] = [(0,0,0),(10,10,10)]
suggestion_button_radius = 0
#endregion

#region Setting up partial functions for similar values
def_button = partial(gamefuncs.Button,screen,font,button_dimens,button_color,text_color,button_radius)
def_suggesion = partial(gamefuncs.Button,screen,font,button_dimens,sugg_button_color,sugg_text_color,suggestion_button_radius)
def_circle = partial(gamefuncs.Button.my_circle,screen,ball_radius,ball_color)
#endregion

while running:
    #region PLay new song if other one stopped
    if not pygame.mixer.music.get_busy():
        possible_next_track = list(set(music_paths)-{current_music})
        if possible_next_track:
            current_music = random.choice(possible_next_track)
            pygame.mixer.music.load(current_music)
            pygame.mixer.music.play()
            
        else:
            pygame.mixer.music.play(-1)
    #endregion
    
    #region Design instruction message :::::DEpending on game mode selection --> To be added
    instr = [font.render(lines[k],True,"White") for k in range(len(lines))]
    instr_centre = [(ful[0]//2,ful[1]//2+instr[k-1].get_height()*k) if fullscreen else (default[0]//2,default[1]//2+instr[k-1].get_height()*k) for k in range(len(lines))]
    instr_rect = [instr[k].get_rect(center = instr_centre[k]) for k in range(len(lines))]
    #endregion
    
    #region --- Timing and states and accuracy updater---
    if timing:
        current_time = pygame.time.get_ticks() - start_time
    # Get all users and suggestions for username input
    time_up = current_time >= max_time
    accurate = gamefuncs.point_in_circle((x, y), ball_radius, pygame.mouse.get_pos())
    #endregion
    
    #region --- Creating Button and Sliders ---
    ### Calculate button positions based on screen mode
    start_cords = (default[0] - button_dimens[0], default[1] - button_dimens[1]) if not fullscreen else (ful[0] - button_dimens[0], ful[1] - button_dimens[1])
    enter_cords = (0, default[1] - button_dimens[1]) if not fullscreen else (0, ful[1] - button_dimens[1])
    settings_cords=(0,0)

    button_triggers = [typing_trigger,sett_trigger,exit_sett_trigger,start_trigger] + list(suggestions_trigger_dict.values())
    
    ### Create Button objects from predefined partial functions
    start_butt = def_button(start_cords,["Start","Start?"])
    enter_butt = def_button(enter_cords,[("Enter" if not user_available else "Switch") if not typing else text_input,("Enter?" if not user_available else "Switch?") if not typing else text_input]) 
    settings_butt = def_button(settings_cords,["Settings","Settings?"])
    exit_sett_butt = def_button(exit_sett_cords,["Exit","Exit?"])
    ball_butt = def_circle((x,y))

    ####Remove all existing suggestion buttons
    suggestions_button_dicts.clear()
    ### Set new suggestions buttons
    if typing:
        suggestions = highscoreSDK.my_searcher(text_input) if typing else list[str]()
        if suggestions:
            idx = 1
            for a_suggestion in suggestions:
                suggestion_button =  def_suggesion((enter_cords[0], enter_cords[1] - button_dimens[1] * idx), [f"{a_suggestion}",f"{a_suggestion}?"]) #Create button object for each suggestion and store it in the dict under the suggestion name
                suggestions_button_dicts[a_suggestion] = suggestion_button
                idx += 1
    #endregion

    #region Event Handling
    for event in pygame.event.get():
   
        if testing and event.type == TEST_EVENT:
            test()
       
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
            if typing and not show_settings:
                key_sounds[def_key_sound].play()
                # Handle text input for username
                if event.key == pygame.K_RETURN:
                    user_available = bool(text_input)
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += (event.unicode).strip()
       
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        
            if music_trigger:
                music_held = True
            if sfx_trigger:
                sfx_held = True
            if any(button_triggers):
                button_sounds[def_button_sound].play()
           
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
                sett_trigger = False
            
            if exit_sett_trigger:
                show_settings = False
                exit_sett_trigger = False
            
            if accurate and timing:
                # Ball clicked during game
                pop_sounds[def_pop_sound].play()
                if fullscreen:
                    x = random.randint(ball_radius, ful[0] - ball_radius)
                    y = random.randint(30 + ball_radius, ful[1] - ball_radius)
                else:
                    x = random.randint(ball_radius, default[0] - ball_radius)
                    y = random.randint(30 + ball_radius, default[1] - ball_radius)
                points += 1
    
        elif event.type == pygame.MOUSEBUTTONUP:
            music_held = False
            sfx_held = False
    #endregion
    
    #region  --- Drawing ---
    # Set background
    if fullscreen:
        screen.blit(background_images_fullscreen[def_back_img],def_pos)
    else:
        screen.blit(background_images_windowed[def_back_img],def_pos)

    #region Drawing main page
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
                ##Clear suggestion triggers
                suggestions_trigger_dict.clear()
                ##Set new suggestion triggers
                if suggestions:
                    for a_suggestion in suggestions_button_dicts:
                        suggestions_trigger_dict[a_suggestion] = gamefuncs.Button.draw(suggestions_button_dicts[a_suggestion]) 
                
            
            
            # Draw start button if user is available and not typing and game not runnin
            if user_available and not typing:
                    start_trigger = gamefuncs.Button.draw(start_butt)
    #endregion
    
    #region Drawing Settings page            
    else:
        mouse_pos = pygame.mouse.get_pos()
        exit_sett_trigger = gamefuncs.Button.draw(exit_sett_butt)

        #region Music
        screen.blit(music_sett,music_rect)
        music_trigger = music_slide_button.collidepoint(mouse_pos)
        music_start,music_volume = gamefuncs.Slider.draw_slider(music_slider,screen,music_held,music_start)
        pygame.mixer_music.set_volume(music_volume)
        #endregion

        #region SFX
        screen.blit(sfx_sett,sfx_rect)
        sfx_trigger = sfx_slide_button.collidepoint(mouse_pos)
        sfx_start,sfx_volume = gamefuncs.Slider.draw_slider(sfx_slider,screen,sfx_held,sfx_start)
        pygame.mixer_music.set_volume(music_volume)
        #Set Effects volume
        for button_sound in button_sounds:
            button_sound.set_volume(sfx_volume)
        for pop_sound in pop_sounds:
            pop_sound.set_volume(sfx_volume)
        #endregion

        
    #endregion
    #endregion
    clock.tick(fps)
    pygame.display.update()
    
