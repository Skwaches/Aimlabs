import pygame
import os
import re

def usable_no(text:str):
    new_text = re.search(r'\d+',text)
    if new_text:
        return int(new_text.group())
    return 0
# def draw_button(screen:pygame.Surface,font:pygame.font.Font, cords:tuple[int,int] ,dimens:tuple[int,int],
#                 text_on:str= "",text_off:str= "",color_off:str|tuple[int,int,int] = "Dark blue",
#                 color_on:str|tuple[int,int,int] = "Navy blue",textcoloron:str|tuple[int,int,int] = "Grey",
#                 textcoloroff:str|tuple[int,int,int] = "white",my_border_radius:int=10):
    
#     off       = font.render(text_off,True,textcoloroff)
#     on        = font.render(text_on,True,textcoloron)
#     butt_rect = pygame.Rect(cords,dimens)
#     teon_rect = on.get_rect(center = butt_rect.center)
#     teoff_rect= off.get_rect(center = butt_rect.center)
#     mouse_pos = pygame.mouse.get_pos()
#     colliding = butt_rect.collidepoint(mouse_pos)
#     if colliding:
#         pygame.draw.rect(screen,color_on,butt_rect,border_radius=my_border_radius)
#         screen.blit(on,teon_rect)
        
            
#     else:
#         pygame.draw.rect(screen,color_off,butt_rect,border_radius=my_border_radius)
#         screen.blit(off,teoff_rect)
#     return colliding

def point_in_circle(center:tuple[float,float],radius:float,point:tuple[float,float]):
    return (center[0] - point[0])**2 + (center[1] -point[1])**2 <= radius**2

def fit(image:pygame.Surface,siz:tuple[int,int]):
    return pygame.transform.smoothscale(image,siz)

def is_valid_image(file_path:str)->bool:
    if os.path.exists(file_path):
        try:
            pygame.image.load(file_path)
            return True
        except Exception:
            return False
    else:
        return False
def is_font_usable(path: str) -> bool:
    try:
        pygame.font.Font(path, 16)  # try loading at some size
        return True
    except Exception:
        return False
# def slider(screen:pygame.Surface,top_left:tuple[int,int]=(0,0),body_dims:tuple[int,int]=(100,50),
#            rail_dims:tuple[int,int]=(70,30),slider_dim:tuple[int,int]=(20,30),held:bool=False,
#            slider_off_color:str|tuple[int,int,int] = "green",slider_on_color:str|tuple[int,int,int] ="dark green",
#            button_color:str|tuple[int,int,int] = "White",rail_color:str|tuple[int,int,int]= "Dark Grey"):
    
#     mouse_pos = pygame.mouse.get_pos()
#     button = pygame.Rect(top_left,body_dims)
#     rail   = pygame.Rect((0,0),rail_dims)
#     slider = pygame.Rect((0,0),slider_dim)
#     rail.center = button.center
#     slider.center = (rail.midleft[0]+slider_dim[0]//2,rail.centery) if not held else (rail.midright[0]-slider_dim[0]//2,rail.centery)
    
#     slider_trigger =slider.collidepoint(mouse_pos)
   

#     button_color = "White"
#     rail_color   = "Dark Grey"
#     slider_color = slider_on_color if slider_trigger else slider_off_color
#     #Displaying
#     pygame.draw.rect(screen,button_color,button,border_radius=20)
#     pygame.draw.rect(screen,rail_color,rail,border_radius=30)
#     pygame.draw.rect(screen,slider_color,slider,border_radius=30)

#     return slider_trigger

def key_index(val:str,dic:dict[str,pygame.font.Font]):
    for id,name in enumerate(dic):
        if name == val:
            return id
    return int()

class Button():
    def __init__(self,screen:pygame.Surface,foNt:pygame.font.Font,
                 dimens:tuple[int,int]=(70,30),color:list[str | tuple[int,int,int]] = ["Navy blue","Red"],
                 textcolor:list[str|tuple[int,int,int]] = ["White","Grey"],
                 border_radius:int=0,left_top:tuple[int,int] = (0,0),text:list[str] = ["Off,On"]):
        self.dimens = dimens
        self.text_off = text[0]
        self.text_on = text[1]
        self.color_off = color[0]
        self.color_on = color[1]
        self.textcolor_off = textcolor[0]
        self.textcolor_on = textcolor[1]
        self.border_radius = border_radius
        self.screen = screen
        self.font   = foNt
        self.left_top = left_top
        self.rect = pygame.Rect(self.left_top,self.dimens)
       
    class my_circle():
        def __init__(self,screen:pygame.Surface,radius:float,color:list[str|tuple[int,int,int]],center:tuple[int,int],):
            self.screen =screen
            self.center = center
            self.radius = radius
            self.color_off = color[0]
            self.color_on = color[1]
            
        def draw(self,accurate:bool):
            pygame.draw.circle(self.screen,self.color_on if accurate else self.color_off,self.center,self.radius)
        def __eq__(self, other: object) -> bool:
            return hash(self) == hash(other)
        
    def __eq__(self, other:object)->bool:
        if isinstance(other,Button):
            tester = [self.dimens==other.dimens,self.text_on==other.text_on,
                    self.text_off==other.text_off,self.text_on ==other.text_on ,
                    self.color_off==other.color_off,self.color_on==other.color_on,
                    self.textcolor_on==other.textcolor_on,self.textcolor_off==other.textcolor_off,
                    self.border_radius==other.border_radius]
            return all(tester)
        else:
            return NotImplemented
    def __str__(self)->str:
        return f"This is a button object"
    def draw(self)->bool:
        off       = self.font.render(self.text_off,True,self.textcolor_off)
        on        = self.font.render(self.text_on,True,self.textcolor_on)
        butt_rect = self.rect
        texton_rect = on.get_rect(center = butt_rect.center)
        textoff_rect= off.get_rect(center = butt_rect.center)
        mouse_pos = pygame.mouse.get_pos()
        colliding = butt_rect.collidepoint(mouse_pos)
        if colliding:
            pygame.draw.rect(self.screen,self.color_on,butt_rect,border_radius=self.border_radius)
            self.screen.blit(on,texton_rect)
            
                
        else:
            pygame.draw.rect(self.screen,self.color_off,butt_rect,border_radius=self.border_radius)
            self.screen.blit(off,textoff_rect)
        return colliding
            
class Slider():
    def __init__(self,slider:pygame.Rect,rail:pygame.Rect,colors:list[str|tuple[int,int,int]],slider_border_radius:int=70,border_radius:int= 20,sld_wid:int=7)->None:
        slider.center = (rail.left,rail.centery)
        self.slider = slider
        self.rail = rail
        self.color = colors
        self.border_radius = border_radius
        self.slider_border_radius = slider_border_radius
        self.sld_wid = sld_wid

    def draw_slider(self,screen:pygame.Surface,held:bool,new_x:int,clicked:bool):
        mouse_pos = pygame.mouse.get_pos()
        if held:
            new_x = max(min(mouse_pos[0],self.rail.right),self.rail.left)
        elif clicked:
            new_x = max(min(mouse_pos[0],self.rail.right),self.rail.left)
        self.slider.centerx = new_x
        rail_on   = pygame.Rect(self.rail.topleft,(new_x-self.rail.left,self.rail.height))
        pygame.draw.rect(screen,self.color[0],self.rail,self.border_radius)
        pygame.draw.rect(screen,self.color[1],rail_on,self.border_radius)
        pygame.draw.rect(screen,self.color[2],self.slider,self.sld_wid,self.slider_border_radius)
        volume = rail_on.width/self.rail.width
        return new_x,volume

if __name__=="__main__":
    print("Greetings Universe")