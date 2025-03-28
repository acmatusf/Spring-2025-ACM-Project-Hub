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

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    clock = pygame.time.Clock()

    # Helper function to generate a random color
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Helper function to generate random food: (x, y, color)
    def get_random_food():
        x = random.randint(0, CELL_COUNT - 1)
        y = random.randint(0, CELL_COUNT - 1)
        color = get_random_color()
        return (x, y, color)

    # Initialize the snake
    snake = [(CELL_COUNT // 2, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 1, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 2, CELL_COUNT // 2)]
    dx, dy = 1, 0

    # Set the initial snake color
    snake_color = GREEN

    # Place the initial food with random color
    food = get_random_food()

    running = True
    global current_background

    while running:
        clock.tick(10)  # Adjust frame rate for game difficulty

        # --- EVENT HANDLING ---
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= event.pos[0] <= 110 and 10 <= event.pos[1] <= 50:
                    current_background = (current_background + 1) % len(backgrounds)

        # --- UPDATE SNAKE ---
        head_x, head_y = snake[0]
        new_x = head_x + dx
        new_y = head_y + dy
        new_head = (new_x, new_y)

        # Check for wall collisions
        if (new_x < 0 or new_x >= CELL_COUNT or new_y < 0 or new_y >= CELL_COUNT):
            running = False

        # Check for self-collision
        if new_head in snake:
            running = False

        # Insert new head
        snake.insert(0, new_head)

        # Check if snake eats the food
        if new_head == (food[0], food[1]):
            snake_color = food[2]  # Change snake color
            food = get_random_food()
        else:
            snake.pop()

        # --- DRAW EVERYTHING ---
        screen.blit(pygame.transform.scale(backgrounds[current_background], (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        # Draw the snake
        for x, y in snake:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, snake_color, rect)

        # Draw the food
        food_rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, food[2], food_rect)

        # Draw the button
        pygame.draw.rect(screen, WHITE, (10, 10, 100, 40))
        font = pygame.font.Font(None, 24)
        text = font.render("Change BG", True, BLACK)
        screen.blit(text, (20, 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
