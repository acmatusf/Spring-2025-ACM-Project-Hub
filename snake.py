import pygame
import sys
import random

# Initialize constants
CELL_SIZE = 20  # Size of each grid cell in pixels
CELL_COUNT = 20  # Number of cells horizontally and vertically (so 400x400 window)
SCREEN_WIDTH = CELL_SIZE * CELL_COUNT
SCREEN_HEIGHT = CELL_SIZE * CELL_COUNT

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)  # Default snake color

# Load background images
backgrounds = [
    pygame.image.load("forest.png"),
    pygame.image.load("desert2.jpg"),
    pygame.image.load("ocean.jpg"),
    pygame.image.load("mountain.jpg"),
    pygame.image.load("space.jpg")
]
current_background = 0  # Index for current background

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Initialize sound
pygame.mixer.init()
pygame.mixer.music.load("Sound.mp3")  # Load background music
pygame.mixer.music.play(-1)  # Loop the music indefinitely
volume = 0.5
pygame.mixer.music.set_volume(volume)

# Game state
paused = False

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_random_food():
    x = random.randint(0, CELL_COUNT - 1)
    y = random.randint(0, CELL_COUNT - 1)
    color = get_random_color()
    return (x, y, color)

def main():
    global current_background, paused, volume
    
    snake = [(CELL_COUNT // 2, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 1, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 2, CELL_COUNT // 2)]
    dx, dy = 1, 0
    snake_color = GREEN
    food = get_random_food()
    running = True
    
    while running:
        clock.tick(10)  # Adjust frame rate
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx != 1:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx != -1:
                    dx, dy = 1, 0
                elif event.key == pygame.K_UP and dy != 1:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy != -1:
                    dx, dy = 0, 1
                elif event.key == pygame.K_p:  # Pause toggle
                    paused = not paused
                elif event.key == pygame.K_b:  # Change background
                    current_background = (current_background + 1) % len(backgrounds)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Increase volume
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_MINUS:  # Decrease volume
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
        
        if paused:
            continue
        
        # Update snake movement
        head_x, head_y = snake[0]
        new_x = head_x + dx
        new_y = head_y + dy
        new_head = (new_x, new_y)
        
        if (new_x < 0 or new_x >= CELL_COUNT or new_y < 0 or new_y >= CELL_COUNT) or new_head in snake:
            running = False
        
        snake.insert(0, new_head)
        
        if new_head == (food[0], food[1]):
            snake_color = food[2]
            food = get_random_food()
        else:
            snake.pop()
        
        # Draw everything
        screen.blit(pygame.transform.scale(backgrounds[current_background], (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        
        for x, y in snake:
            pygame.draw.rect(screen, snake_color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, food[2], (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
