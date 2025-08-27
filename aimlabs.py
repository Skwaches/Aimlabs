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
default = (1000, 550)
ful = (1600, 900)
button_dimens = (250, 55)
screen = pygame.display.set_mode(default)
pygame.display.set_caption("Skwaches' Aim Game")
#endregion

#Link directory
game_dir = os.getcwd()
img_dir = os.path.join(game_dir, "Game_images") if os.path.exists(os.path.join(game_dir, "Game_images")) else str()
font_dir = os.path.join(game_dir,"Game_fonts") if os.path.exists(os.path.join(game_dir,"Game_fonts")) else str()
audio_dir = os.path.join(game_dir, "Game_Audio") if os.path.exists(os.path.join(game_dir, "Game_Audio")) else str()
#region --- StateAdjustable Variables ---

current_back_img  = 0
def_pop_sound = 0
def_button_sound = 0
def_key_sound = 0
def_font = "consolas"
back_up_font = "msgothic"
sys_fonts = ["Georgia","Times New Roman","Segoe UI","Arial","Impact","Verdana","consolas"]
sys_font_names = list[str]()
sys_font_paths = list[str]()
muted = False
music_volume = 0.7 if not muted else 0
sfx_volume = 0.8 if not muted else 0
font_size = 35
#endregion

dummy_surface = pygame.Surface((0,0),pygame.SRCALPHA)
dummy_surface.fill((0,0,0,0))
#Loading resources

#region Fonts
font_files = os.listdir(font_dir) if font_dir else list[str]()
font_paths = [os.path.join(font_dir,font_file) for font_file in font_files] if font_files else list[str]()
fonts      = {font_file:pygame.font.Font(font_path,font_size) for font_file,font_path in zip(font_files,font_paths) if gamefuncs.is_font_usable(font_path)}
for sys_font in sys_fonts:
    sys_font_path = pygame.font.match_font(sys_font) 
    if sys_font_path:
        sys_font_paths.append(sys_font_path)
        sys_font_names.append(sys_font)
        fonts[sys_font] = pygame.font.Font(sys_font_path,font_size)
font_paths += sys_font_paths
current_font = def_font if def_font in fonts else back_up_font if back_up_font in fonts else random.choice(list(fonts.keys()))
current_font_index = gamefuncs.key_index(current_font,fonts)
font_names = [avail_font for avail_font in fonts] 
font       = fonts[current_font]
#endregion

#region Songs
music_dir   = os.path.join(audio_dir,"background_music") if audio_dir else str()
music_files = os.listdir(music_dir) if music_dir else list[str]()
music_paths = [os.path.join(music_dir, music_files[k]) for k in range(len(music_files)) if music_files[k].endswith(".mp3")] if music_files else list[str]()
#endregion

#region Image
orig_dir = os.path.join(img_dir,"orig_back_img")
orig_files = os.listdir(orig_dir) if os.path.exists(orig_dir) else list[str]()
orig_paths = [os.path.join(orig_dir,orig_file) for orig_file in orig_files]
orig_paths = list(filter(gamefuncs.is_valid_image,orig_paths))

back_img_dir  =os.path.join(img_dir,"background_img") if img_dir and os.path.exists(os.path.join(img_dir,"background_img")) else str()
back_img_files = os.listdir(back_img_dir) if back_img_dir else list[str]()
back_img_paths = [os.path.join(back_img_dir,back_img_file) for back_img_file in back_img_files] if back_img_files else list[str]()
back_img_paths = list(filter(gamefuncs.is_valid_image,back_img_paths))
back_img_paths = orig_paths + back_img_paths

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

if music_paths:
    current_music = random.choice(music_paths)
    pygame.mixer_music.load(current_music) 
    pygame.mixer_music.play(0)
    pygame.mixer_music.set_volume(music_volume)
else:
    current_music = str()
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
ball_radius = 30                   # Ball radius

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
text_color  :list[str|tuple[int,int,int]]= ["White","Grey"]
ball_color:list[str|tuple[int,int,int]]= [(200, 245, 190),(150, 195, 140)]
button_triggers = [] #game_triggers = [typing_trigger,sett_trigger,exit_sett_trigger,start_trigger] + [trigger for _,trigger in suggestions_trigger_dict]
exit_sett_cords = (0,0)
show_start_text = False
show_settings   = False
show_high_scores = False
show_game_modes = False
game_mode_trigger = False

high_score_trigger = False
show_end_text = False
instr_disp_time = 2000
sett_trigger = False
button_radius = 10
sugg_button_color:list[str|tuple[int,int,int]] = ["grey","dark grey"]
sugg_text_color:list[str|tuple[int,int,int]] = [(0,0,0),(10,10,10)]
suggestion_button_radius = 0
max_sugg_display = 4
changing_display_width =400
music_held = False
music_trigger = False
top_users = []
change_width = 70
#endregion

#region -----SETTINGS------
sett_v_gap =100
sett_h_gap =30
music_clicked_trigger = False
sfx_clicked_trigger = False
music_clicked = False
sfx_clicked = False

font_next_trigger = False
font_prev_trigger = False
back_next_trigger =False
back_prev_trigger =False
sfx_test_trigger = False
#region sett MUSIC

music_spot = pygame.rect.Rect((0,button_dimens[1]+sett_h_gap),button_dimens)
music_rail = pygame.rect.Rect((music_spot.right+sett_v_gap,music_spot.top),(100,5))
music_start:int  = round(music_volume*(music_rail.width))+music_rail.left
music_rail.centery = music_spot.centery
music_slide_button = pygame.rect.Rect((music_start,music_rail.centery),(15,15))
music_colors:list[str|tuple[int,int,int]] = ["Dark grey","Green","White"]

music_slider = gamefuncs.Slider(music_slide_button,music_rail,music_colors,sld_wid=0,slider_border_radius=100)
#endregion

#region sett SFX
sfx_spot = pygame.rect.Rect((0,music_spot.bottom+sett_h_gap),button_dimens)


sfx_held = False
sfx_trigger = False
sfx_rail = pygame.rect.Rect((sfx_spot.right+sett_v_gap,sfx_spot.centery),(100,5))
sfx_start:int  = round(sfx_volume*(sfx_rail.width))+music_rail.left
sfx_rail.centery = sfx_spot.centery
sfx_slide_button = pygame.rect.Rect((sfx_start,sfx_rail.centery),(15,15))
sfx_colors:list[str|tuple[int,int,int]] = ["Dark grey","Green","White"]
sfx_slider = gamefuncs.Slider(sfx_slide_button,sfx_rail,sfx_colors,sld_wid=0)
#endregion

#region sett Background
back_spot = pygame.rect.Rect((0,sfx_spot.bottom+sett_h_gap),button_dimens)

back_imgfile_rect = pygame.rect.Rect((back_spot.right+sett_v_gap+change_width,back_spot.top),(changing_display_width,button_dimens[1]))
back_imgfile_rect.centery = back_spot.centery 
back_img_files_color = "Grey"

back_next_trigger = False
#endregion

#region sett Font
font_spot = pygame.rect.Rect((0,back_spot.bottom+sett_h_gap),button_dimens)

font_file_rect = pygame.rect.Rect((font_spot.right+sett_v_gap+change_width,font_spot.top),(changing_display_width,button_dimens[1]))
font_file_rect.centery = font_spot.centery 
font_files_color = "Grey"

font_next_trigger = False
    #endregion

    #endregion


#region TESTS WITHIN LOOP
testing =True
test_delay = 2000
TEST_EVENT = pygame.USEREVENT+1
if testing: 
    pygame.time.set_timer(TEST_EVENT,test_delay)
def test():
    print(changing_time,changing_dots)
#endregion

#region Game Modes Logic
"""_summary_
Main modes: Time is limited, number of dots is limited or BOTH.:::
Sub-modes : Whether the dots disappear after a time delay or not.:::
"""
time_limited = True
dot_limited  = False
survival = True
max_time = 30*1000               # Max time per round (ms)
auto_pop_current_time = 0
auto_pop_start_time = 0 
auto_pop_delay = 1000
no_dots = 10
dots_appeared = 0
time_limited_trigger = False 
dot_limited_trigger = False
survival_trigger = False
dot_change_trigger = False
time_change_trigger = False
changing_time =False
changing_dots = False
time_input = f"{max_time/1000:.0f}"
dot_input = f"{no_dots}"
#endregion
size_change = False
high_score_dy = 0
high_score_velocity = 30

while running:
    font_size = 35 if not fullscreen else 49
    button_dimens =(260,55) if not fullscreen else (390,100)
    change_width = 70 if not fullscreen else 120
    if size_change:

        fonts = {font_name:pygame.font.Font(font_path,font_size) for font_name,font_path in zip(font_names,font_paths)}

        font = fonts[font_names[current_font_index]]
        #region sett MUSIC
        music_spot = pygame.rect.Rect((0,button_dimens[1]+sett_h_gap),button_dimens)
        music_rail = pygame.rect.Rect((music_spot.right+sett_v_gap,music_spot.top),(100,5))
        music_start:int  = round(music_volume*(music_rail.width))+music_rail.left
        music_rail.centery = music_spot.centery
        music_slide_button = pygame.rect.Rect((music_start,music_rail.centery),(15,15))
        music_colors:list[str|tuple[int,int,int]] = ["Dark grey","Green","White"]

        music_slider = gamefuncs.Slider(music_slide_button,music_rail,music_colors,sld_wid=0,slider_border_radius=100)
        #endregion

        #region sett SFX
        sfx_spot = pygame.rect.Rect((0,music_spot.bottom+sett_h_gap),button_dimens)
        sfx_held = False
        sfx_trigger = False
        sfx_rail = pygame.rect.Rect((sfx_spot.right+sett_v_gap,sfx_spot.centery),(100,5))
        sfx_start:int  = round(sfx_volume*(sfx_rail.width))+music_rail.left
        sfx_rail.centery = sfx_spot.centery
        sfx_slide_button = pygame.rect.Rect((sfx_start,sfx_rail.centery),(15,15))
        sfx_colors:list[str|tuple[int,int,int]] = ["Dark grey","Green","White"]
        sfx_slider = gamefuncs.Slider(sfx_slide_button,sfx_rail,sfx_colors,sld_wid=0)
        #endregion

        #region sett Background
        back_spot = pygame.rect.Rect((0,sfx_spot.bottom+sett_h_gap),button_dimens)
        back_imgfile_rect = pygame.rect.Rect((back_spot.right+sett_v_gap+change_width,back_spot.top),(changing_display_width,button_dimens[1]))
        back_imgfile_rect.centery = back_spot.centery 
        back_img_files_color = "Grey"
        back_next_trigger = False
        #endregion

        #region sett Font
        font_spot = pygame.rect.Rect((0,back_spot.bottom+sett_h_gap),button_dimens)
        font_file_rect = pygame.rect.Rect((font_spot.right+sett_v_gap+change_width,font_spot.top),(changing_display_width,button_dimens[1]))
        font_file_rect.centery = font_spot.centery 
        font_files_color = "Grey"
        font_next_trigger = False
            #endregion
        size_change = False
    #region INSTRUCTIONS
    ##Time limited instructions
    instr_text = "Click As Many\nCircles As You Can!" if time_limited else "Click the Circles\nAs FAST as you can!"
    end_text= f"Time's UP!\nYou got {points} points!!" if time_limited else f"You clicked all the circles!!\nYou finished in {current_time/1000:.2f} seconds!"

    lines = instr_text.split("\n")
    end_lines= end_text.split("\n")

    clock = pygame.time.Clock()
    fps = 100
    #endregion

    #region partial functions for similar values
    def_button = partial(gamefuncs.Button,screen,font,button_dimens,button_color,text_color,button_radius)
    def_suggesion = partial(gamefuncs.Button,screen,font,button_dimens,sugg_button_color,sugg_text_color,suggestion_button_radius)
    def_circle = partial(gamefuncs.Button.my_circle,screen,ball_radius,ball_color)
    #endregion

    #region PLay new song if other one stopped
    if not pygame.mixer.music.get_busy() and music_paths:
        possible_next_track = list(set(music_paths)-{current_music})
        if possible_next_track:
            current_music = random.choice(possible_next_track)
            pygame.mixer.music.load(current_music)
            pygame.mixer.music.play()
            
        else:
            pygame.mixer.music.play(-1)
    #endregion
    
   
    #region --- Timing and states and accuracy updater---
    if timing:
        current_time = pygame.time.get_ticks() - start_time
    # Get all users and suggestions for username input
    time_up = current_time >= max_time if time_limited else False

    accurate = gamefuncs.point_in_circle((x, y), ball_radius, pygame.mouse.get_pos())
    #endregion
    
    #region Design instruction message :::::Depending on game mode selection --> To be added
    font.bold =True
    instr_surface = [font.render(lines[k],True,"Red") for k in range(len(lines))]
    instr_centre = [(ful[0]//2,ful[1]//2+instr_surface[k-1].get_height()*k) if fullscreen else (default[0]//2,default[1]//2+instr_surface[k-1].get_height()*k) for k in range(len(lines))]
    instr_rect = [instr_surface[k].get_rect(center = instr_centre[k]) for k in range(len(lines))]

    end_surfaces = [font.render(end_lines[k],True,"Red") for k in range(len(lines))]
    end_center   = [(ful[0]//2,ful[1]//2+end_surfaces[k-1].get_height()*k) if fullscreen else (default[0]//2,default[1]//2+end_surfaces[k-1].get_height()*k) for k in range(len(end_lines))]
    end_rect     = [end_surfaces[k].get_rect(center = end_center[k]) for k in range(len(end_lines))]
    font.bold = False
    #endregion
    
    
    #region Settings renders
    font.bold = True
    font_texts = {my_fonter:(font.render(f"{my_fonter.split()[0]}",True,"Black")) for my_fonter in fonts}
    sfx_sett = font.render("Sfx vol",True,"White")
    sfx_rect = sfx_sett.get_rect(center = sfx_spot.center)
    music_sett = font.render("Music",True,"White")
    music_rect = music_sett.get_rect(center = music_spot.center)
    back_sett = font.render("Background",True,"White")
    back_rect = sfx_sett.get_rect(center =back_spot.center)
    font_sett = font.render("Font",True,"White")
    font_rect = sfx_sett.get_rect(center =font_spot.center)
    back_texts = [(font.render(f"{i}",True,"Black")) for i in range(len(back_img_paths))]
    font.bold =False
    #endregion

    #region --- Creating Button and Sliders ---
    ### Calculate button positions based on screen mode
    start_cords = (default[0] - button_dimens[0], default[1] - button_dimens[1]) if not fullscreen else (ful[0] - button_dimens[0], ful[1] - button_dimens[1])
    enter_cords = (0, default[1] - button_dimens[1]) if not fullscreen else (0, ful[1] - button_dimens[1])
    settings_cords=(0,0)

    button_triggers = [typing_trigger,sett_trigger,start_trigger] + list(suggestions_trigger_dict.values()) +[back_next_trigger,font_next_trigger,back_prev_trigger,font_prev_trigger]+[game_mode_trigger,high_score_trigger,sfx_test_trigger]+[time_change_trigger,dot_change_trigger]
    
    ### Create Button objects from predefined partial functions
    start_butt = def_button(start_cords,["Start","Start?"])
    enter_butt = def_button(enter_cords,[("Enter Username" if not user_available else "Switch") if not typing else text_input,("Enter?" if not user_available else "Switch?") if not typing else text_input]) 
    settings_butt = def_button(settings_cords,["Settings","Settings?"] if not show_settings else ["Exit","Exit?"])
    # exit_sett_butt = def_button(exit_sett_cords,["Exit","Exit?"])
    ball_butt = def_circle((x,y))
    
    font_next_button = def_button(font_file_rect.topright,["Next","Next?"])
    font_prev_button = def_button((font_file_rect.left-change_width,font_file_rect.top),["Prev","Prev?"])
    font_next_button.dimens = ((change_width,button_dimens[1]))
    font_prev_button.dimens = ((change_width,button_dimens[1]))


    font_next_button.dimens = ((change_width,button_dimens[1]))
    back_next_button = def_button(back_imgfile_rect.topright,["Next","Next?"])
    back_prev_button = def_button((back_imgfile_rect.left-change_width,back_imgfile_rect.top),["Prev","Prev?"])
    back_next_button.dimens = (change_width,button_dimens[1])
    back_prev_button.dimens = ((change_width,button_dimens[1]))

    high_score_top_left = ((ful[0] - button_dimens[0])//2,0) if fullscreen else ((default[0]-button_dimens[0])//2,0)
    high_score_button = def_button(high_score_top_left,["Highscores","Highscores?"] if not show_high_scores else ["Exit","Exit?"])
    game_mode_top_left = ((ful[0]-button_dimens[0])//2,(ful[1]-button_dimens[1])//2) if fullscreen else ((default[0]-button_dimens[0])//2,(default[1]-button_dimens[1])//2)
    game_mode_button = def_button(game_mode_top_left if not show_game_modes else (0,0),["Game Mode","Game Mode?"] if not show_game_modes else ["Exit","Exit?"])
   
    time_limited_button = def_button((0,(ful[1]-button_dimens[1])//4) if fullscreen else (0,(default[1]-button_dimens[1])//4),["Time Limited","Time Limited?"])
    time_change_button = def_button(time_limited_button.rect.topright,[f"{max_time/1000} s",f"{max_time/1000} s?"] if not changing_time else [f"{time_input} s",f"{time_input} s"])
    
    dot_limited_button = def_button((0,(ful[1]-button_dimens[1])//2)if fullscreen else (0,(default[1]-button_dimens[1])//2),["Dot limited","Dot limited?"])
    dot_change_button =def_button(dot_limited_button.rect.topright,[f"{no_dots}.0 dots",f"{no_dots}.0 dots ?"] if not changing_dots else [f"{dot_input} dots",f"{dot_input} dots"] )
    
    survival_button       = def_button((0,(ful[1]-button_dimens[1])*3//4) if fullscreen else (0,(default[1]-button_dimens[1])*3//4),["Survival","Survival?"])
    survival_change_delay = def_button(survival_button.rect.topright,["Survival","Survival?"])
    if survival:
        survival_button.color_off,survival_button.color_on = ("green","dark green")
    if dot_limited:
        dot_limited_button.color_off,dot_limited_button.color_on = ("green","dark green")
    if time_limited:
        time_limited_button.color_off,time_limited_button.color_on = ("green","dark green")
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
                size_change =True
                # Toggle fullscreen
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(default)
            if typing:
                key_sounds[def_key_sound].play()
                # Handle text input for username
                if event.key == pygame.K_RETURN:
                    user_available = bool(text_input)
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += (event.unicode).strip()
            if changing_time:
                key_sounds[def_key_sound].play()

                if event.key == pygame.K_RETURN:
                    changing_time = False
                    max_time = gamefuncs.usable_no(time_input)*1000 if gamefuncs.usable_no(time_input)>= 10 else max_time
                elif event.key == pygame.K_BACKSPACE:
                    time_input = time_input[:-1]
                else:
                    time_input += (event.unicode).strip()
            if changing_dots:                    
                key_sounds[def_key_sound].play()
                if event.key == pygame.K_RETURN:
                    changing_dots = False
                    no_dots = gamefuncs.usable_no(dot_input) if gamefuncs.usable_no(dot_input)>= 10 else no_dots
                elif event.key == pygame.K_BACKSPACE:
                    dot_input = dot_input[:-1]
                else:
                    dot_input += (event.unicode).strip()
        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1:
                if music_trigger:
                    music_held = True
                    music_trigger = False
                if music_clicked_trigger:
                    music_clicked = False
                    music_clicked_trigger = False
                elif sfx_trigger:
                    sfx_held = True
                    sfx_trigger = False
                elif sfx_clicked_trigger:
                    sfx_clicked = True
                    sfx_clicked_trigger = False
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
                    typing_trigger = False

                elif high_score_trigger:
                    show_high_scores = not show_high_scores
                    high_score_trigger = False
                
    
                elif game_mode_trigger:
                    show_game_modes = not show_game_modes
                    game_mode_trigger = False
                    if not show_game_modes:
                        no_dots = gamefuncs.usable_no(dot_input) if gamefuncs.usable_no(dot_input)>= 10 else no_dots
                        max_time = gamefuncs.usable_no(time_input) if gamefuncs.usable_no(dot_input)>=10 else max_time

                elif start_trigger:
                    # Start button pressed to begin game
                    show_start_text=True
                    start_trigger = False
                    
                elif sett_trigger:
                    show_settings = not show_settings
                    sett_trigger  = False


                elif back_next_trigger:
                    current_back_img= (current_back_img+1)%(min(len(background_images_fullscreen),len(background_images_windowed)))
                    back_next_trigger = False
                elif back_prev_trigger:
                    current_back_img= (current_back_img-1)%(min(len(background_images_fullscreen),len(background_images_windowed)))
                    back_prev_trigger = False             
                elif font_next_trigger:
                    current_font_index = (current_font_index+1)%len(font_names)
                    font = fonts[font_names[current_font_index]]
                    font_next_trigger = False
                elif font_prev_trigger:
                    current_font_index = (current_font_index-1)%len(font_names)
                    font = fonts[font_names[current_font_index]]  
                    font_prev_trigger =False                  
                elif time_limited_trigger:
                    time_limited = True
                    dot_limited = False
                    time_limited_trigger = False
                elif dot_limited_trigger:
                    dot_limited_trigger =False
                    dot_limited = True
                    time_limited = False
                elif survival_trigger:
                    survival = not survival
                    survival_trigger = False
                elif time_change_trigger:
                    changing_dots = False
                    no_dots = gamefuncs.usable_no(dot_input) if gamefuncs.usable_no(dot_input)>= 10 else no_dots
                    changing_time =True
                    time_input =""
                    time_change_trigger =False
                elif dot_change_trigger:
                    changing_time = False
                    max_time = gamefuncs.usable_no(time_input)*1000 if gamefuncs.usable_no(time_input)>= 10 else max_time

                    changing_dots =True
                    dot_input = ""
                    dot_change_trigger =False
                if accurate and timing:
                    # Ball clicked during game
                    pop_sounds[def_pop_sound].play()
                    auto_pop_start_time = pygame.time.get_ticks()
                    auto_pop_current_time = 0
                    if fullscreen:
                        x = random.randint(ball_radius, ful[0] - ball_radius)
                        y = random.randint(30 + ball_radius, ful[1] - ball_radius)
                    else:
                        x = random.randint(ball_radius, default[0] - ball_radius)
                        y = random.randint(30 + ball_radius, default[1] - ball_radius)
                    points += 1
                    dots_appeared +=1
                    if dot_limited and dots_appeared>=no_dots:
                        timing = False
                        show_end_text = True

        elif event.type == pygame.MOUSEBUTTONUP:
            music_held = False
            sfx_held = False
            sfx_clicked = False
            music_clicked = False
   
        if event.type == pygame.MOUSEWHEEL:
            if show_high_scores:
                if event.y == -1:
                    high_score_dy -= high_score_velocity
                    
                if event.y == 1:
                    high_score_dy += high_score_velocity
                  
    #endregion
    if not show_high_scores:
        high_score_dy = 0
    #region  --- Drawing ---
    # Set background
    if back_img_paths:
        if fullscreen:
            screen.blit(background_images_fullscreen[current_back_img],def_pos)
        else:
            screen.blit(background_images_windowed[current_back_img],def_pos)

    else:
        screen.fill((0,0,0))
    

    ##PAGES

    #Highscores
    if show_high_scores:
        font.underline = True
        font.bold = True
        user_title = font.render("USERNAME:",True,"Black")
        user_rect  = user_title.get_rect(topleft = (70,button_dimens[1]+high_score_dy))
        screen.blit(user_title,user_rect)

        score_title = font.render("SCORES (Dots per second)",True,"Black")
        score_rect  = score_title.get_rect(topleft = ((ful[0] if fullscreen else default[0])//2 , button_dimens[1]+high_score_dy))
        screen.blit(score_title,score_rect)
        font.underline =False
        font.bold =False
        font.italic = True
        game_highscores = highscoreSDK.top(100)
        legend_surfaces = list[pygame.Surface]()
        legend_rects = list[pygame.Rect]()
        high_score_surfaces = list[pygame.Surface]()
        high_scores_rects = list[pygame.Rect]()
        j = 1
        for score in game_highscores:
            for user in game_highscores[score]:
                legend_surfaces.append(font.render(f"{j}. {user}",True,"White"))
                high_score_surfaces.append(font.render(f"{score:.3f}",True,"White"))
                j+=1
            
        for i,(legend_surface,high_score_surface) in enumerate(zip(legend_surfaces,high_score_surfaces)):
            legend_rects.append(legend_surface.get_rect(topleft = (70,(button_dimens[1]+font_size + (legend_surface.get_height()+(10 if not fullscreen else 30))*i) + high_score_dy)))
            high_scores_rects.append(high_score_surface.get_rect(topleft = ( (ful[0] if fullscreen else default[0])//2, legend_rects[i].topleft[1])))
        for (surf,rect),(surf2,rect2) in zip(zip(legend_surfaces,legend_rects),zip(high_score_surfaces,high_scores_rects)):
            screen.blit(surf,rect)
            screen.blit(surf2,rect2)
        high_score_trigger =  gamefuncs.Button.draw(high_score_button)
        font.italic =False
    #Game modes
    
    elif show_game_modes:
        game_mode_trigger = gamefuncs.Button.draw(game_mode_button)
        time_change_trigger = gamefuncs.Button.draw(time_change_button)
        time_limited_trigger = gamefuncs.Button.draw(time_limited_button)
        dot_change_trigger  = gamefuncs.Button.draw(dot_change_button)
        dot_limited_trigger = gamefuncs.Button.draw(dot_limited_button)
        survival_trigger = gamefuncs.Button.draw(survival_button)
    #region Settings           
    elif show_settings:
        mouse_pos = pygame.mouse.get_pos()
        sett_trigger = gamefuncs.Button.draw(settings_butt)

        #region Music
        if music_paths:

            screen.blit(music_sett,music_rect)
            music_clicked_trigger = music_rail.collidepoint(mouse_pos)
            music_trigger = music_slide_button.collidepoint(mouse_pos)
            music_start,music_volume = gamefuncs.Slider.draw_slider(music_slider,screen,music_held,music_start,music_clicked)
            pygame.mixer_music.set_volume(music_volume)
        #endregion

        #region SFX
        if button_sounds or key_sounds or pop_sounds:
            sfx_test_butt = def_button((sfx_rail.right+10,sfx_spot.top),["Test","Test?"])
            sfx_test_butt.dimens = (change_width,button_dimens[1])
            sfx_test_trigger = gamefuncs.Button.draw(sfx_test_butt)
            screen.blit(sfx_sett,sfx_rect)
            sfx_clicked_trigger = sfx_rail.collidepoint(mouse_pos)
            sfx_trigger = sfx_slide_button.collidepoint(mouse_pos)
            sfx_start,sfx_volume = gamefuncs.Slider.draw_slider(sfx_slider,screen,sfx_held,sfx_start,sfx_clicked)
            pygame.mixer_music.set_volume(music_volume)
            #Set Effects volume
            for button_sound in button_sounds:
                button_sound.set_volume(sfx_volume)
            for pop_sound in pop_sounds:
                pop_sound.set_volume(sfx_volume)
            for key_sound in key_sounds:
                key_sound.set_volume(sfx_volume)
        #endregion

        #region Background
        if back_img_paths:
            back_next_button.border_radius = 0 
            back_prev_button.border_radius = 0
            screen.blit(back_sett,back_rect)
            pygame.draw.rect(screen,back_img_files_color,back_imgfile_rect)
            screen.blit(back_texts[current_back_img],back_imgfile_rect)
            back_next_trigger = gamefuncs.Button.draw(back_next_button)
            back_prev_trigger = gamefuncs.Button.draw(back_prev_button)
        #endregion
        
        #region Font
        screen.blit(font_sett,font_rect)
        pygame.draw.rect(screen,font_files_color,font_file_rect)
        screen.blit(font_texts[font_names[current_font_index]],font_file_rect)
        font_next_button.border_radius = 0
        font_prev_button.border_radius = 0
        font_next_trigger = gamefuncs.Button.draw(font_next_button)
        font_prev_trigger = gamefuncs.Button.draw(font_prev_button)
        #endregion
    #endregion

    ## Main Page
    else: 
        # Draw start instructions message
        if show_start_text:
            for k in range(len(lines)):
                screen.blit(instr_surface[k],instr_rect[k])
            pygame.display.flip()
            pygame.time.wait(instr_disp_time)
            timing = True
            current_time = 0
            points = 0
            start_time = pygame.time.get_ticks()
            auto_pop_start_time = pygame.time.get_ticks() if survival else 0
            show_start_text = False
        elif show_end_text:
            for k in range(len(end_lines)):
                screen.blit(end_surfaces[k],end_rect[k])
            pygame.display.flip()
            pygame.time.wait(instr_disp_time//2)
            highscoreSDK.add_scores(text_input, points/current_time*1000) if current_time else None
            dots_appeared = 0
            current_time = 0
            auto_pop_current_time = 0
            show_end_text = False
            

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
            if time_limited and time_up:

                timing = False
                time_up = False
                show_end_text = True
            if survival:
                auto_pop_current_time = pygame.time.get_ticks() - auto_pop_start_time
                if auto_pop_current_time>=auto_pop_delay:
                    auto_pop_start_time = pygame.time.get_ticks()
                    if fullscreen:
                        x = random.randint(ball_radius, ful[0] - ball_radius)
                        y = random.randint(30 + ball_radius, ful[1] - ball_radius)
                    else:
                        x = random.randint(ball_radius, default[0] - ball_radius)
                        y = random.randint(30 + ball_radius, default[1] - ball_radius)
                    dots_appeared+=1
                    if dots_appeared>=no_dots:
                        timing = False
                        show_end_text = True
            if dot_limited:
                dots_remaining_text = font.render(f"Dots remaining:{no_dots - dots_appeared-1}", True, "White")
                dots_remaining_box = pygame.Rect(((ful[0] - button_dimens[0])//2,0) if fullscreen else ((default[0]-button_dimens[0])//2,0), dots_remaining_text.get_size())
                dots_remaining_rect = dots_remaining_text.get_rect(center=dots_remaining_box.center)
                pygame.draw.rect(screen,"Black",dots_remaining_box)
                screen.blit(dots_remaining_text,dots_remaining_rect)
        else:
            # Draw enter and settings button
            enter_butt.dimens = (button_dimens[0]+70,button_dimens[1])
            typing_trigger = gamefuncs.Button.draw(enter_butt)
            sett_trigger   = gamefuncs.Button.draw(settings_butt)
            game_mode_trigger = gamefuncs.Button.draw(game_mode_button)
            high_score_trigger =  gamefuncs.Button.draw(high_score_button)
            if typing:# Draw suggestion buttons if typing
                ##Clear suggestion triggers
                suggestions_trigger_dict.clear()
                ##Set new suggestion 
                if suggestions:
                    for i,a_suggestion in enumerate(suggestions_button_dicts):
                        if i<max_sugg_display:
                            suggestions_button_dicts[a_suggestion].dimens = enter_butt.dimens
                            suggestions_trigger_dict[a_suggestion] = gamefuncs.Button.draw(suggestions_button_dicts[a_suggestion])
            
            # Draw start button if user is available and not typing and game not runnin
            if user_available and not typing:
                    start_trigger = gamefuncs.Button.draw(start_butt)
    #endregion
   
    clock.tick(fps)
    pygame.display.update()
    
