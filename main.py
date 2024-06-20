import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Draw Rectangle on Surface")

# Create a surface with the specified dimensions and alpha channel
surface_width, surface_height = 200, 100
surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)

# Fill the surface with a black color
black = (0, 0, 0)
surface.fill(black)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen with a white background
    screen.fill((255, 255, 255))

    # Blit the surface onto the screen at position (100, 100)
    screen.blit(surface, (100, 100))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
