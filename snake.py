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

def main():
    # 1. Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    # 2. Show speed selection menu
    speed = show_menu(screen)

    # 3. Set up clock for controlling the frame rate
    clock = pygame.time.Clock()

    # 4. Define a helper function to get a random position for the food
    def get_random_food_position():
        # Randomly place food within the grid (0 <= x < CELL_COUNT, 0 <= y < CELL_COUNT)
        x = random.randint(0, CELL_COUNT - 1)
        y = random.randint(0, CELL_COUNT - 1)
        return (x, y)

    # 5. Initialize the snake
    # Snake is a list of (x, y) positions; start in the middle with length 3
    snake = [(CELL_COUNT // 2, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 1, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 2, CELL_COUNT // 2)]
    
    # The snake's direction (dx, dy). Start moving right.
    dx, dy = 1, 0

    # 6. Place initial food
    food = get_random_food_position()

    # 7. Game loop
    running = True
    while running:
        clock.tick(speed)  # Adjust speed based on selection

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Prevent snake from going directly backward
                if event.key == pygame.K_LEFT and dx != 1:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx != -1:
                    dx, dy = 1, 0
                elif event.key == pygame.K_UP and dy != 1:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy != -1:
                    dx, dy = 0, 1

        # --- UPDATE SNAKE ---
        # Current head position
        head_x, head_y = snake[0]
        # New head position
        new_x = head_x + dx
        new_y = head_y + dy
        new_head = (new_x, new_y)

        # 1. Check for collisions with walls
        if (new_x < 0 or new_x >= CELL_COUNT or
            new_y < 0 or new_y >= CELL_COUNT):
            # Hit a wall -> Game Over
            running = False

        # 2. Check for collisions with self
        if new_head in snake:
            # Hit itself -> Game Over
            running = False

        # If still safe, insert new head
        snake.insert(0, new_head)

        # 3. Check if we ate the food
        if new_head == food:
            # Generate a new food position; don't pop the tail (snake grows)
            food = get_random_food_position()
        else:
            # Move forward (remove the tail)
            snake.pop()

        # --- DRAW EVERYTHING ---
        screen.fill(BLACK)  # Clear screen with black

        # Draw the snake
        for x, y in snake:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect)

        # Draw the food
        food_rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)

        pygame.display.flip()

    # Once we exit the loop, the game is over
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()