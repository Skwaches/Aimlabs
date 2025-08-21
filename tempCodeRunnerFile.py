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
slider_speed = 2
k = slider_speed
while running:
    slider.center = rail.midleft if not active else rail.midright
    mouse_pos = pygame.mouse.get_pos()

    # if within_range and held:
    #     slider.center = (mouse_pos[0],slider.centery)
    slider_trigger =slider.collidepoint(mouse_pos)

    button_color = "White"
    rail_color   = "Dark Grey"
    slider_color = ("Green" if not slider_trigger else "Dark green") if not active else ("Red" if not slider_trigger else "Dark red")
    
    # Event-handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and slider_trigger :
            active = not active
            activity = True
        
    if activity:
        while slider.center[0] in range (rail.midleft[0],rail.midright[0]):
            slider.center = (slider.center[0]+k,slider.centery)if active else (slider.center[0]-k,slider.centery)
            pygame.display.flip()
            k+=1
        activity = False
        k = slider_speed
    #Displaying
    pygame.draw.rect(screen,button_color,button,border_radius=20)
    pygame.draw.rect(screen,rail_color,rail,border_radius=30)
    pygame.draw.rect(screen,slider_color,slider,border_radius=30)
    pygame.display.update()
    clock.tick(24)
