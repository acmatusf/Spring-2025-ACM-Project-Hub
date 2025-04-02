import pygame
import sys
import random

# Initialize constants
CELL_SIZE = 20   # Size of each grid cell in pixels
CELL_COUNT = 20  # Number of cells horizontally and vertically (so 400x400 window)
SCREEN_WIDTH = CELL_SIZE * CELL_COUNT
SCREEN_HEIGHT = CELL_SIZE * CELL_COUNT

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED   = (200, 0, 0)
BLUE  = (0, 0, 200)  # Death block color

# Speed settings
SPEED_LEVELS = {"Easy": 5, "Normal": 10, "Hard": 15}



def show_menu(screen):
    font = pygame.font.Font(None, 36)
    screen.fill(BLACK)
    
    options = ["Easy", "Normal", "Hard"]
    selected = 0
    
    while True:
        screen.fill(BLACK)
        title = font.render("Select Speed: Use v/^, ENTER to select", True, WHITE)
        screen.blit(title, (20, 50))
        
        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            text = font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 3, 150 + i * 40))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return SPEED_LEVELS[options[selected]]

def get_random_position(exclude_positions):
    corners = {(0, 0), (0, CELL_COUNT - 1), (CELL_COUNT - 1, 0), (CELL_COUNT - 1, CELL_COUNT - 1)}
    while True:
        pos = (random.randint(1, CELL_COUNT - 2), random.randint(1, CELL_COUNT - 2))
        if pos not in exclude_positions and pos not in corners:
            return pos

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    
    speed = show_menu(screen)
    clock = pygame.time.Clock()
    
    snake = [(CELL_COUNT // 2, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 1, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 2, CELL_COUNT // 2)]
    dx, dy = 1, 0
    food = get_random_position(snake)
    
    death_blocks = []
    apples_eaten = 0
    
    running = True
    while running:
        clock.tick(speed)
        
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
        
        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)
        
        if (new_head[0] < 0 or new_head[0] >= CELL_COUNT or
            new_head[1] < 0 or new_head[1] >= CELL_COUNT or
            new_head in snake or new_head in death_blocks):
            running = False
        
        snake.insert(0, new_head)
        
        if new_head == food:
            apples_eaten += 1
            food = get_random_position(snake + death_blocks)
            if apples_eaten % 5 == 0:
                if len(death_blocks) < 5:
                    death_blocks.append(get_random_position(snake + death_blocks + [food]))
                else:
                    death_blocks.pop(0)
                    death_blocks.append(get_random_position(snake + death_blocks + [food]))
        else:
            snake.pop()
        
        screen.fill(BLACK)
        for x, y in snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.draw.rect(screen, RED, pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        for x, y in death_blocks:
            pygame.draw.rect(screen, BLUE, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
