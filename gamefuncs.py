import pygame
from enum import Enum
from PIL import Image
def draw_button(screen:pygame.Surface,font:pygame.font.Font, cords:tuple[int] ,dimens:tuple[int],
                text_on:str= "",text_off:str= "",color_off:str|tuple[int,int,int] = "Dark blue",
                color_on:str|tuple[int] = "Navy blue",textcoloron:str|tuple[int,int,int] = "Grey",
                textcoloroff:str|tuple[int,int,int] = "white",my_border_radius:int=10):
    
    off       = font.render(text_off,True,textcoloroff)
    on        = font.render(text_on,True,textcoloron)
    butt_rect = pygame.Rect(cords,dimens)
    teon_rect = on.get_rect(center = butt_rect.center)
    teoff_rect= off.get_rect(center = butt_rect.center)
    mouse_pos = pygame.mouse.get_pos()
    colliding = butt_rect.collidepoint(mouse_pos)
    if colliding:
        pygame.draw.rect(screen,color_on,butt_rect,border_radius=my_border_radius)
        screen.blit(on,teon_rect)
        
            
    else:
        pygame.draw.rect(screen,color_off,butt_rect,border_radius=my_border_radius)
        screen.blit(off,teoff_rect)
    return colliding

def point_in_circle(center:tuple[float,float],radius:float,point:tuple[float,float]):
    return (center[0] - point[0])**2 + (center[1] -point[1])**2 <= radius**2

def fit(image:pygame.Surface,siz:tuple[int,int]):
    return pygame.transform.smoothscale(image,siz)

def is_valid_image(file_path:str):
    try:
        with Image.open(file_path) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False
    
def slider(screen:pygame.Surface,top_left:tuple[int,int]=(0,0),body_dims:tuple[int,int]=(100,50),
           rail_dims:tuple[int,int]=(70,30),slider_dim:tuple[int,int]=(20,30),active:bool=False,
           slider_off_color:str|tuple[int,int,int] = "green",slider_on_color:str|tuple[int,int,int] ="dark green",
           button_color:str|tuple[int,int,int] = "White",rail_color:str|tuple[int,int,int]= "Dark Grey"):
    
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

class button():
    def __init__(self,dimens:tuple[int],text_on:str= "",text_off:str= "",color_off:str|tuple[int,int,int] = "Dark blue",
                color_on:str|tuple[int] = "Navy blue",textcoloron:str|tuple[int,int,int] = "Grey",
                textcoloroff:str|tuple[int,int,int] = "white",my_border_radius:int=10):
        self.dimens = dimens
        self.text_on = text_on
        self.text_off = text_off
        self.text_on  = text_on
        self.color_off = color_off
        self.color_on = color_on
        self.textcoloron = textcoloron
        self.textcoloroff = textcoloroff
        self.my_border_radius = my_border_radius
    def __eq__(self, other):
        tester = [self.dimens==other.dimens,self.text_on==other.text_on,
                 self.text_off==other.text_off,self.text_on ==other.text_on ,
                 self.color_off==other.color_off,self.color_on==other.color_on,
                 self.textcoloron==other.textcoloron,self.textcoloroff==other.textcoloroff,
                 self.my_border_radius==other.my_border_radius]
        return all(tester)
    
class setting(Enum):
    pass

if __name__=="__main__":
    print("Greetings Universe")