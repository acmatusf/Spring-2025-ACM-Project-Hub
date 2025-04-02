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

def main():
    # 1. Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    font = pygame.font.Font(None, 30)  # Font for displaying score

    # 2. Set up clock for controlling the frame rate
    clock = pygame.time.Clock()

    # 3. Define a helper function to get a random position for the food
    def get_random_food_position():
        x = random.randint(0, CELL_COUNT - 1)
        y = random.randint(0, CELL_COUNT - 1)
        return (x, y)

    # 4. Initialize the snake
    snake = [(CELL_COUNT // 2, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 1, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 2, CELL_COUNT // 2)]
    
    dx, dy = 1, 0
    food = get_random_food_position()
    next_dx, next_dy = dx, dy
    pygame.mouse.set_visible(False)
    
    score = 0  # Initialize score

    running = True
    while running:
        clock.tick(10)

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and dx != 1:
                    next_dx, next_dy = -1, 0
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dx != -1:
                    next_dx, next_dy = 1, 0
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and dy != 1:
                    next_dx, next_dy = 0, -1
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and dy != -1:
                    next_dx, next_dy = 0, 1
        
        dx, dy = next_dx, next_dy
        head_x, head_y = snake[0]
        new_x = head_x + dx
        new_y = head_y + dy
        new_head = (new_x, new_y)

        if new_x < 0:
            new_head = (CELL_COUNT - 1, new_y)
        elif new_x >= CELL_COUNT:
            new_head = (0, new_y)
        elif new_y < 0:
            new_head = (new_x, CELL_COUNT - 1)
        elif new_y >= CELL_COUNT:
            new_head = (new_x, 0)

        if new_head in snake:
            running = False

        snake.insert(0, new_head)

        if new_head == food:
            temp_food = get_random_food_position()
            while temp_food in snake or temp_food is new_head:
                temp_food = get_random_food_position()
            food = temp_food
            score += 10  # Increase score by 10 when food is eaten
        else:
            snake.pop()

        screen.fill(BLACK)

        for x, y in snake:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect)

        food_rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, food_rect)
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 120, 10))  # Display score at top right

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()