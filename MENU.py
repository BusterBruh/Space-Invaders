#%%

import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Screen Switcher")

# Load background image
background = pygame.image.load("Title.png")

# Load a custom font (change the font file path as needed)
custom_font = pygame.font.Font("RACING HARD.ttf", 36)

# Class to manage text objects
class TextObject:
    def __init__(self, text, font, color, position):
        self.text = text
        self.font = font
        self.color = color
        self.position = position

    def render(self, screen):
        rendered_text = self.font.render(self.text, True, self.color)
        screen.blit(rendered_text, self.position)

# Calculate positions for the text lines at the bottom right corner
text1 = TextObject("STORY MODE - Press A", custom_font, WHITE, (WIDTH - 370, HEIGHT - 100))
text2 = TextObject("ENDLESS MODE - Press D", custom_font, WHITE, (WIDTH - 380, HEIGHT - 50))

# Main loop
current_screen = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_a:
                if current_screen != 'screen1':
                    current_screen = 'screen1'
                    exec(open('SD_STAGE1.py').read())
            elif event.key == K_d:
                if current_screen != 'screen2':
                    current_screen = 'screen2'
                    exec(open('screen2.py').read())

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw background image
    screen.blit(background, (0, 0))

    # Render and display text objects
    text1.render(screen)
    text2.render(screen)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


# %%
