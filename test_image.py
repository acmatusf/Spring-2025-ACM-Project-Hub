import pygame

# Initialize pygame
pygame.init()

# Load the image
try:
    image = pygame.image.load("images/forest.png")
    print("Image loaded successfully!")
except pygame.error as e:
    print(f"Error loading image: {e}")

# Quit pygame
pygame.quit()
