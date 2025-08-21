import pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,400))
running = True
held = False

width,height = 100,50
r_width,r_height = 70,20
slider_dim   = (20,45)

button       = pygame.Rect(((800-width)//2,(400-height)//2),(width,height))
rail = pygame.Rect((0,0),(r_width,r_height))
slider       = pygame.Rect((0,0),slider_dim)
active = False
rail.center = button.center
activity = False
slide_delay= 2
while running:
    slider.center = (rail.midleft[0]+slider_dim[0]//2,rail.centery) if not active else (rail.midright[0]-slider_dim[0]//2,rail.centery)
    mouse_pos = pygame.mouse.get_pos()
    slider_trigger =slider.collidepoint(mouse_pos)

    button_color = "White"
    rail_color   = "Dark Grey"
    slider_color = ("Green" if not slider_trigger else "Dark green") if not active else ("Red" if not slider_trigger else "Dark red")
    
    # Event-handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and slider_trigger :
            slider_range = (rail.midleft[0]+slider_dim[0]//2,rail.midright[0],1) if not active else (rail.midright[0]-slider_dim[0]//2,rail.midleft[0],-1)
            active = not active
            for i in range(*slider_range):
                print(i)
                slider.center = [i,slider.centery] 
                pygame.draw.rect(screen,button_color,button,border_radius=20)
                pygame.draw.rect(screen,rail_color,rail,border_radius=30)
                pygame.draw.rect(screen,slider_color,slider,border_radius=30)
                pygame.display.flip()
                pygame.time.wait(slide_delay)
        
        
    #Displaying
    pygame.draw.rect(screen,button_color,button,border_radius=20)
    pygame.draw.rect(screen,rail_color,rail,border_radius=30)
    pygame.draw.rect(screen,slider_color,slider,border_radius=30)
    pygame.display.update()
    clock.tick(60)
