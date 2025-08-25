import pygame

# Initialize Pygame
pygame.init()

# Set up screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrolling Example")

# Define a scroll offset
scroll_y = 0
scroll_speed = 10  # Adjust as needed

# Example content to scroll (e.g., a long list of text)
content_lines = [f"Line {i}" for i in range(50)]
font = pygame.font.Font(None, 30)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                scroll_y += scroll_speed
            elif event.button == 5:  # Scroll down
                scroll_y -= scroll_speed

    # Clear the screen
    screen.fill((255, 255, 255)) # White background

    # Draw content with scroll offset
    for i, line in enumerate(content_lines):
        text_surface = font.render(line, True, (0, 0, 0)) # Black text
        # Adjust y-coordinate by adding scroll_y
        screen.blit(text_surface, (50, 50 + i * 30 + scroll_y))

    # Update the display
    pygame.display.flip()

pygame.quit()