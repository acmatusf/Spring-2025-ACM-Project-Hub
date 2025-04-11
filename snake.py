import pygame
import sys
import random
import json

# Initialize constants
CELL_SIZE = 25   # Size of each grid cell in pixels
CELL_COUNT = 30  # Number of cells horizontally and vertically (so 600x600 window)

PAUSED_MENU_CELLS = 13 # Width of the paused menu
PAUSED_MENU_HEIGHT = PAUSED_MENU_CELLS * CELL_SIZE # Height of the paused menu
PAUSED_MENU_WIDTH = PAUSED_MENU_CELLS * CELL_SIZE # Width of the paused menu

SCOREBOARD_CELLS = 3 # Number of cells for the scoreboard area
SCOREBOARD_HEIGHT = SCOREBOARD_CELLS * CELL_SIZE # Height of the scoreboard area

SCREEN_WIDTH = CELL_SIZE * CELL_COUNT
SCREEN_HEIGHT = CELL_SIZE * CELL_COUNT + SCOREBOARD_HEIGHT # Extra space for scoreboard section
SCREEN_GAME_ARENA = CELL_SIZE * CELL_COUNT # Game area size

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0) # Default snake color

DIFFICULTY_COLORS = {
    "Easy": (0, 255, 0), # Bright Green
    "Normal": (255, 165, 0), # Orange
    "Hard": (139, 0, 0) # Blood red
}

# BRIGHT_GREEN = (0, 255, 0)
# ORANGE = (255, 165, 0)
# BLOOD_RED = (139, 0, 0)
# IDEA FOR BG: have 0.000000000001% chance of getting random funny bg when changing it (by Tima)

def get_player_name(screen, font):
    name = ""
    input_active = True
    
    while input_active:
        screen.fill(BLACK)
        prompt_text = font.render("Enter your name: " + name, True, WHITE)
        screen.blit(prompt_text, (50, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable():
                    name += event.unicode
    
    return name

# Load background images
backgrounds = [
    pygame.image.load("images/forest.png"),
    pygame.image.load("images/desert2.jpg"),
    pygame.image.load("images/ocean.jpg"),
    pygame.image.load("images/mountain.jpg"),
    pygame.image.load("images/space.jpg")
]
current_background = 0  # Index for current background

# Font settings
font_sellected = "PressStart2P-Regular.ttf" # Font for the game

# Speed settings
SPEED_LEVELS = {"Easy": 5.0, "Normal": 10.0, "Hard": 15.0}
SPEED_CHANGES = {"Easy": 0.25, "Normal": 0.5, "Hard": 0.75}
speed_change = 0

def show_main_menu(screen):
    font = pygame.font.Font(font_sellected, 48)
    option_font = pygame.font.Font(font_sellected, 36)
    options = ["Classic Mode", "Challenge Mode"]
    selected = 0

    while True:
        screen.fill(BLACK)
        title = font.render("snAkeCM", True, GREEN)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            text = option_font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 100))

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

    title_font = pygame.font.Font(font_sellected, 36)
    option_font = pygame.font.Font(font_sellected, 28)

    screen.fill(BLACK)

    title_x = SCREEN_WIDTH // 2 # X position of the title
    title_y = SCREEN_HEIGHT // 8 # Y position of the title

    text_x = SCREEN_WIDTH // 8 # X position of the text
    text_y = SCREEN_HEIGHT // 8 + 100 # Y position of the text
    
    options = ["Easy", "Normal", "Hard"]
    selected = 0
    
    while True:
        title = title_font.render("Classic Mode", True, WHITE)
        title_rect = title.get_rect(center=(title_x, title_y))

        screen.blit(title, title_rect)
        
        for i, option in enumerate(options):
            color = DIFFICULTY_COLORS[option] if i == selected else WHITE
            text = option_font.render(option, True, color)
            text_rect = text.get_rect(topleft=(text_x, text_y + i * 60))

            screen.blit(text, text_rect)
        
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
                
def pause_menu(screen):
    global backgrounds, current_background

    title_font = pygame.font.Font(font_sellected, 25)
    option_font = pygame.font.Font(font_sellected, 20)

    x_paused = (SCREEN_WIDTH - PAUSED_MENU_WIDTH) // 2 # X position of the paused menu
    y_paused = (SCREEN_GAME_ARENA - PAUSED_MENU_HEIGHT) // 2 + SCOREBOARD_HEIGHT # Y position of the paused menu

    title_x = x_paused + PAUSED_MENU_WIDTH // 2 # X position of the title
    title_y = y_paused + PAUSED_MENU_HEIGHT // 8 # Y position of the title

    text_x = x_paused + PAUSED_MENU_WIDTH // 8 # X position of the text
    text_y = y_paused + PAUSED_MENU_HEIGHT // 8 + 50 # Y position of the text


    options = ["Resume", "Restart", "Change BG", "Music On/Off", "Exit"]
    selected = 0
    
    while True:
        pygame.draw.rect(screen, BLACK, (x_paused, y_paused, PAUSED_MENU_WIDTH, PAUSED_MENU_HEIGHT))
        
        title = title_font.render("Paused", True, WHITE)
        title_rect = title.get_rect(center=(title_x, title_y))

        screen.blit(title, title_rect)

        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE

            text = option_font.render(option, True, color)
            text_rect = text.get_rect(topleft=(text_x, text_y + i * 40))
            screen.blit(text, text_rect)

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
                    if options[selected] == "Resume":
                        return
                    elif options[selected] == "Restart":
                        main()
                    elif options[selected] == "Change BG":
                        current_background = (current_background + 1) % len(backgrounds)
                        screen.blit(pygame.transform.scale(backgrounds[current_background], (SCREEN_WIDTH, SCREEN_GAME_ARENA)), (0, SCOREBOARD_HEIGHT))
                    elif options[selected] == "Music On/Off":
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    elif options[selected] == "Exit":
                        pygame.quit()
                        sys.exit()
        
        pygame.display.flip()

# --- HELPER FUNCTIONS ---

# Function to play the snake sounds
def play_sound(sound):
    pygame.mixer.Sound.play(sound)

# Function to get random color
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to get a random position for the food
def get_random_food_position():
    # Randomly place food within the grid (0 <= x < CELL_COUNT, SCOREBOARD_CELLS - 1 <= y < CELL_COUNT + SCOREBOARD_CELLS - 1)
    x = random.randint(0, CELL_COUNT - 1)
    y = random.randint(SCOREBOARD_CELLS + 1, CELL_COUNT + SCOREBOARD_CELLS - 1)
    color = get_random_color()
    return (x, y, color)

# Initialize Pygame & setup display
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("snAkeCM")

# Set up clock for controlling the frame rate
clock = pygame.time.Clock()

# Show main menu first
selected_mode = show_main_menu(screen)

# Show speed selection menu
speed = show_menu(screen)

# Initialize sound
pygame.mixer.init()
pygame.mixer.music.load("Sound/Sound.mp3")  # Load background music
pygame.mixer.music.play(-1)  # Loop the music indefinitely
volume = 0.5
pygame.mixer.music.set_volume(volume)

def main():
    flipped_once = False
    global current_background, volume, speed
    # Initialize the snake
    # Snake is a list of (x, y) positions; start in the middle with length 3
    snake = [(CELL_COUNT // 2, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 1, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 2, CELL_COUNT // 2)]

    font = pygame.font.Font(font_sellected, 30)
    player_name = get_player_name(screen, font)
    
    # Initialize snake sounds
    movement_sound = pygame.mixer.Sound("Sound/movement.wav")
    eat_sound = pygame.mixer.Sound("Sound/eating.wav")
    death_sound = pygame.mixer.Sound("Sound/death-sound-pixel.wav")
    
    # The snake's direction (dx, dy). Start moving right.
    dx, dy = 1, 0

    # Place initial food and snake color
    snake_color = GREEN
    food = get_random_food_position()

    # Game loop

    # define next directions, AVOID BUG OF SNAKE GOING INTO ITSELF
    next_dx, next_dy = dx, dy

    score = 0
    score_x = SCREEN_WIDTH // 17 # X position of the score
    score_y = SCOREBOARD_HEIGHT // 2 - 10  # Y position of the score

    # Set invisible mouse
    pygame.mouse.set_visible(False)
    score = 0  # Initialize score

    running = True
    while running:
        clock.tick(speed)  # Adjust speed based on difficulty

        # --- CHALLENGE MODE TOGGLE ---
        if 5 <= score < 10 and not flipped_once:

            snake.reverse()

                         
            x1, y1 = snake[0]
            x2, y2 = snake[1]

            dx = x1 - x2
            dy = y1 - y2

            next_dx = dx
            next_dy = dy

           

        elif score < 15:
            pass # Call 2nd challenge function
        elif score < 20:
            pass # Call 3rd challenge function
        elif score < 25:
            pass # Call 4th challenge function
        else:
            pass # Call 5th challenge function

        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Prevent snake from going directly backward
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and dx != 1:
                    next_dx, next_dy = -1, 0
                    play_sound(movement_sound)
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dx != -1:
                    next_dx, next_dy = 1, 0
                    play_sound(movement_sound)
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and dy != 1:
                    next_dx, next_dy = 0, -1
                    play_sound(movement_sound)
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and dy != -1:
                    next_dx, next_dy = 0, 1
                    play_sound(movement_sound)
                elif event.key == pygame.K_ESCAPE:  # Pause toggle
                    pause_menu(screen)
                elif event.key == pygame.K_b:  # Change background
                    current_background = (current_background + 1) % len(backgrounds)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Increase volume
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_MINUS:  # Decrease volume
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)

                # elif event.key == pygame.K_f:
                #         snake.reverse()

                         
                #         x1, y1 = snake[0]
                #         x2, y2 = snake[1]

                #         dx = x1 - x2
                #         dy = y1 - y2

                #         next_dx = dx
                #         next_dy = dy

        
        # Apply directions change ONCE PER FRAME
        dx, dy = next_dx, next_dy

        # --- UPDATE SNAKE ---
        # Current head position
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
        elif new_y < SCOREBOARD_CELLS:
            new_head = (new_x, CELL_COUNT + SCOREBOARD_CELLS)
        elif new_y >= CELL_COUNT + SCOREBOARD_CELLS:
            new_head = (new_x, SCOREBOARD_CELLS)

        # 2. Check for collisions with self
        if new_head in snake:
            # Hit itself -> Game Over
            play_sound(death_sound)
            pygame.time.delay(1000)  # Wait for a second to let the sound play
            new_entry = {'user': player_name, 'score': score}
            # Load existing data or start with an empty list
            try:
                with open('user_score.json', 'r') as file:
                    scores = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                scores = []

            # Append the new score
            scores.append(new_entry)

            # Save the updated list
            with open('user_score.json', 'w') as file:
                json.dump(scores, file, indent=4)
            print(new_entry)
            running = False

        # Walls around the borders
        #if (new_x < 0 or new_x >= CELL_COUNT or new_y < 0 or new_y >= CELL_COUNT) or new_head in snake:
        #    running = False

        # If still safe, insert new head
        snake.insert(0, new_head)

        # 3. Check if we ate the food
        if new_head == (food[0], food[1]):
            play_sound(eat_sound) # play snake eat food sound
            snake_color = food[2] # changes snake color based on food
            speed += speed_change # increase snake speed after eating food
            score += 1  # Increase score by 1 when food is eaten
            # Generate a new food position; don't pop the tail (snake grows)
            temp_food = get_random_food_position()
            while temp_food in snake or temp_food is new_head:
                temp_food = get_random_food_position()
            food = temp_food
            flipped_once = False
        else:
            # Move forward (remove the tail)
            snake.pop()

        # --- DRAW EVERYTHING ---
        screen.blit(pygame.transform.scale(backgrounds[current_background], (SCREEN_WIDTH, SCREEN_GAME_ARENA)), (0, SCOREBOARD_HEIGHT))

        # Draw the scoreboard area
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCOREBOARD_HEIGHT))

        # Draw the score
        score_font = pygame.font.Font(font_sellected, 27)
        score_text = score_font.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(topleft=(score_x, score_y))

        screen.blit(score_text, score_rect)

        # Draw the snake
        for x, y in snake:
            pygame.draw.rect(screen, snake_color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the food
        pygame.draw.rect(screen, food[2], (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()

    # Once we exit the loop, the game is over
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()