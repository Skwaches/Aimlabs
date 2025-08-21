import pygame
from enum import Enum
from PIL import Image
def draw_button(screen ,font, cords ,dimens ,text_on= "",text_off = "",color_off = "Dark blue",color_on = "Navy blue",textcoloron = "Grey",textcoloroff = "white",my_border_radius=10, img = None,):
    off       = font.render(text_off,True,textcoloroff)
    on        = font.render(text_on,True,textcoloron)
    butt_rect = pygame.Rect(cords,dimens)
    teon_rect = on.get_rect(center = butt_rect.center)
    teoff_rect= off.get_rect(center = butt_rect.center)
    mouse_pos = pygame.mouse.get_pos()
    colliding = butt_rect.collidepoint(mouse_pos)
    if colliding:
        pygame.draw.rect(screen,color_on,butt_rect)
        if img:
            screen.blit(img,cords)
        screen.blit(on,teon_rect)
        
            
    else:
        pygame.draw.rect(screen,color_off,butt_rect,border_radius=my_border_radius)
        if img:
            screen.blit(img,cords)
        screen.blit(off,teoff_rect)
    return colliding

def point_in_circle(center,radius,point):
    return (center[0] - point[0])**2 + (center[1] -point[1])**2 <= radius**2

def fit(image,siz):
    return pygame.transform.smoothscale(image,siz)

def is_valid_image(file_name):
    try:
        with Image.open(file_name) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False
    
def slider(screen,top_left=(0,0),body_dims=(100,50),rail_dims=(70,30),slider_dim=(20,30),active=False,slider_off_color = "green",slider_on_color = "dark green",button_color = "White",rail_color   = "Dark Grey"):
    button = pygame.Rect(top_left,body_dims)
    rail   = pygame.Rect((0,0),rail_dims)
    slider = pygame.Rect((0,0),slider_dim)
    

    rail.center = button.center
    slider.center = (rail.midleft[0]+slider_dim[0]//2,rail.centery) if not active else (rail.midright[0]-slider_dim[0]//2,rail.centery)
    mouse_pos = pygame.mouse.get_pos()
    slider_trigger =slider.collidepoint(mouse_pos)

    button_color = "White"
    rail_color   = "Dark Grey"
    slider_color = slider_on_color if slider_trigger else slider_off_color
    #Displaying
    pygame.draw.rect(screen,button_color,button,border_radius=20)
    pygame.draw.rect(screen,rail_color,rail,border_radius=30)
    pygame.draw.rect(screen,slider_color,slider,border_radius=30)

    return slider_trigger

class game_mode(Enum):
    pass
class setting(Enum):
    pass

if __name__=="__main__":
    print("Greetings Universe")