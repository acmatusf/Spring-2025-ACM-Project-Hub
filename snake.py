import pygame
import sys
import random

# Initialize constants
CELL_SIZE = 30   # Size of each grid cell in pixels
CELL_COUNT = 20  # Number of cells horizontally and vertically (so 600x600 window)
SCREEN_WIDTH = CELL_SIZE * CELL_COUNT
SCREEN_HEIGHT = CELL_SIZE * CELL_COUNT

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0) # Default snake color

# Load background images
backgrounds = [
    pygame.image.load("images/forest.png"),
    pygame.image.load("images/desert2.jpg"),
    pygame.image.load("images/ocean.jpg"),
    pygame.image.load("images/mountain.jpg"),
    pygame.image.load("images/space.jpg")
]
current_background = 0  # Index for current background

# Function to play the snake sounds
def play_sound(sound):
    pygame.mixer.Sound.play(sound)

# Speed settings
SPEED_LEVELS = {"Easy": 5.0, "Normal": 10.0, "Hard": 15.0}
SPEED_CHANGES = {"Easy": 0.25, "Normal": 0.5, "Hard": 0.75}
speed_change = 0

def show_main_menu(screen):
    font = pygame.font.Font(None, 48)
    option_font = pygame.font.Font(None, 36)
    options = ["Classic Mode", "Challenge Mode"]
    selected = 0

    while True:
        screen.fill(BLACK)
        title = font.render("snAkeCM", True, GREEN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            text = option_font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150 + i * 50))

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
                    return options[selected]  # For future use if you want different behavior

def show_menu(screen):
    global speed_change
    font = pygame.font.Font(None, 36)
    screen.fill(BLACK)
    
    options = ["Easy", "Normal", "Hard"]
    selected = 0
    
    while True:
        screen.fill(BLACK)
        title = font.render("Select Speed: Use arrow keys, ENTER to select", True, WHITE)
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
                    speed_change = SPEED_CHANGES[options[selected]]
                    return SPEED_LEVELS[options[selected]]

# 1. Initialize Pygame & setup display
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# 2. Set up clock for controlling the frame rate
clock = pygame.time.Clock()

# 3. Show main menu first
selected_mode = show_main_menu(screen)

# 4. Show speed selection menu
speed = show_menu(screen)

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

# 4. Define a helper function to get a random position for the food
def get_random_food_position():
    # Randomly place food within the grid (0 <= x < CELL_COUNT, 0 <= y < CELL_COUNT)
    x = random.randint(0, CELL_COUNT - 1)
    y = random.randint(0, CELL_COUNT - 1)
    color = get_random_color()
    return (x, y, color)

def main():
    global current_background, paused, volume, speed
    # 5. Initialize the snake
    # Snake is a list of (x, y) positions; start in the middle with length 3
    snake = [(CELL_COUNT // 2, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 1, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 2, CELL_COUNT // 2)]
    
    # Initialize snake sounds
    movement_sound = pygame.mixer.Sound("movement.wav")
    eat_sound = pygame.mixer.Sound("eating.wav")
    death_sound = pygame.mixer.Sound("death-sound-pixel.wav")
    move = False
    
    # The snake's direction (dx, dy). Start moving right.
    dx, dy = 1, 0

    # 6. Place initial food and snake color
    snake_color = GREEN
    food = get_random_food_position()

    # 7. Game loop

    # define next directions, AVOID BUG OF SNAKE GOING INTO ITSELF
    next_dx, next_dy = dx, dy
    
    #Set the mouse cursor to invisible
    #pygame.mouse.set_visible(False)

    running = True
    while running:
        clock.tick(speed)  # Adjust speed based on difficulty

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                move = True
                # Prevent snake from going directly backward
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and dx != 1:
                    next_dx, next_dy = -1, 0
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dx != -1:
                    next_dx, next_dy = 1, 0
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and dy != 1:
                    next_dx, next_dy = 0, -1
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and dy != -1:
                    next_dx, next_dy = 0, 1
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
                else:
                    move = False
        
        if paused:
            continue
        
        head_x, head_y = snake[0]
        # New head position
        new_x = head_x + dx
        new_y = head_y + dy
        new_head = (new_x, new_y)

        # No walls, snake goes through borders
        # 1. Check for collisions with walls
        if new_x < 0:
            new_head = (CELL_COUNT - 1, new_y)
        elif new_x >= CELL_COUNT:
            new_head = (0, new_y)
        elif new_y < 0:
            new_head = (new_x, CELL_COUNT - 1)
        elif new_y >= CELL_COUNT:
            new_head = (new_x, 0)

        # 2. Check for collisions with self
        if new_head in snake:
            # Hit itself -> Game Over
            play_sound(death_sound)
            pygame.time.delay(1000)  # Wait for a second to let the sound play
            running = False

        # Walls around the borders
        #if (new_x < 0 or new_x >= CELL_COUNT or new_y < 0 or new_y >= CELL_COUNT) or new_head in snake:
        #    running = False

        # If still safe, insert new head
        snake.insert(0, new_head)
        
        # play movement sounds only when WASD or arrow keys are pressed
        if move:
            play_sound(movement_sound)
            move = False
        
        if new_head == (food[0], food[1]):
            play_sound(eat_sound) # play snake eat food sound
            snake_color = food[2] # changes snake color based on food
            speed += speed_change # increase snake speed after eating food
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

        # --- DRAW EVERYTHING ---
        screen.blit(pygame.transform.scale(backgrounds[current_background], (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        # Draw the snake
        for x, y in snake:
            pygame.draw.rect(screen, snake_color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the food
        pygame.draw.rect(screen, food[2], (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
