import pygame
import sys
import random
import json

# Initialize constants
CELL_SIZE = 30  # Size of each grid cell in pixels
CELL_COUNT = 20  # Number of cells horizontally and vertically (so 600x600 window)

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
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)

DIFFICULTY_COLORS = {
    "Easy": (0, 255, 0), # Bright Green
    "Normal": (255, 165, 0), # Orange
    "Hard": (139, 0, 0) # Blood red
}

# --- IMPORTANT VARIABLES ---

# Initialize Pygame & setup display
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("snAkeCM")

# Set up clock for controlling the frame rate
clock = pygame.time.Clock()

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

hard_mode_unlocked = False

best_score = 0

'''
IDEAS / WHAT TO DO 

(In addition to main tasks like toggle function or main menu )

Change bacground images: more 8-bit images that would fit the vibe 
8-bit music (Change music to hard rockish when closer to finish the game)

in pause manu change Quit to Back to MM 
also add sound effect on/off button

eastern egg in backgrounds with chance of 0.0000001% 

'''


# --- UI ---

# Main menu of the game 
def main_menu(screen):
    global font_sellected, hard_mode_unlocked

    title_font = pygame.font.Font(font_sellected, 36)
    option_font = pygame.font.Font(font_sellected, 28)

    screen.fill(BLACK)

    title_x = SCREEN_WIDTH // 2 # X position of the title
    title_y = SCREEN_HEIGHT // 8 # Y position of the title

    text_x = SCREEN_WIDTH // 8 # X position of the text
    text_y = SCREEN_HEIGHT // 8 + 100 # Y position of the text

    options = ["Classic Mode", "Challenge Mode", "Quit"]

    
    selectable_indexes = [
        i for i, option in enumerate(options) if option != 'Challenge Mode' or hard_mode_unlocked
    ]

    selected = selected_index = 0
    selected = selectable_indexes[selected]

    while True:
        title = title_font.render("snAkeCM", True, WHITE)
        title_rect = title.get_rect(center=(title_x, title_y))

        screen.blit(title, title_rect)

        for i, option in enumerate(options):
            if option == 'Challenge Mode' and not hard_mode_unlocked:
                color = GRAY
            elif i == selected:
                color = YELLOW
            else:
                color = WHITE

            text = option_font.render(option, True, color)
            text_rect = text.get_rect(topleft=(text_x, text_y + i * 60))
            screen.blit(text, text_rect)
        
        pygame.display.flip()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_index = (selected_index - 1) % len(selectable_indexes)
                    selected = selectable_indexes[selected_index]
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_index = (selected_index + 1) % len(selectable_indexes)
                    selected = selectable_indexes[selected_index]
                elif event.key == pygame.K_RETURN:
                    if options[selected] == 'Quit':
                        pygame.quit()
                        sys.exit()
                    else:
                        return options[selected]

# Classic Mode screen to select the difficulty
def classic_mode_screen(screen):
    global speed_change, font_sellected

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
                    return options[selected]

# Pause Menu
def pause_menu(screen, mode, difficulty):
    global backgrounds, current_background, font_sellected

    title_font = pygame.font.Font(font_sellected, 25)
    option_font = pygame.font.Font(font_sellected, 20)

    x_paused = (SCREEN_WIDTH - PAUSED_MENU_WIDTH) // 2 # X position of the paused menu
    y_paused = (SCREEN_GAME_ARENA - PAUSED_MENU_HEIGHT) // 2 + SCOREBOARD_HEIGHT # Y position of the paused menu

    title_x = x_paused + PAUSED_MENU_WIDTH // 2 # X position of the title
    title_y = y_paused + PAUSED_MENU_HEIGHT // 8 # Y position of the title

    text_x = x_paused + PAUSED_MENU_WIDTH // 8 # X position of the text
    text_y = y_paused + PAUSED_MENU_HEIGHT // 8 + 50 # Y position of the text


    options = ["Resume", "Restart", "Change BG", "Music On/Off", "Back to MM"]
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
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Resume":
                        return
                    elif options[selected] == "Restart":
                        game(mode, difficulty)
                    elif options[selected] == "Change BG":
                        current_background = (current_background + 1) % len(backgrounds)
                        screen.blit(pygame.transform.scale(backgrounds[current_background], (SCREEN_WIDTH, SCREEN_GAME_ARENA)), (0, SCOREBOARD_HEIGHT))
                    elif options[selected] == "Music On/Off":
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    elif options[selected] == "Back to MM":
                        main()
        
        pygame.display.flip()

# death menu to show the best score and ask "Try again?"
def death_menu(score, player_name):
    global best_score

    # update the best score
    best_score = max(best_score, score)

    # if player "loged in", save their score
    if player_name:
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

    # font setting
    title_font = pygame.font.Font(font_sellected, 25)
    option_font = pygame.font.Font(font_sellected, 20)

    # menu location
    x_paused = (SCREEN_WIDTH - PAUSED_MENU_WIDTH) // 2 # X position of the paused menu
    y_paused = (SCREEN_GAME_ARENA - PAUSED_MENU_HEIGHT) // 2 + SCOREBOARD_HEIGHT # Y position of the paused menu

    # title position
    title_x = x_paused + PAUSED_MENU_WIDTH // 2 # X position of the title
    title_y = y_paused + PAUSED_MENU_HEIGHT // 8 # Y position of the title
    
    # text postion
    text_x = x_paused + PAUSED_MENU_WIDTH // 8 # X position of the text
    text_y = y_paused + PAUSED_MENU_HEIGHT // 8 + 90 # Y position of the text

    options = ["Yes", "No"]
    selected = 0
    
    while True:
        pygame.draw.rect(screen, BLACK, (x_paused, y_paused, PAUSED_MENU_WIDTH, PAUSED_MENU_HEIGHT))
        
        # Print title
        title = title_font.render("YOU DIED!", True, WHITE)
        title_rect = title.get_rect(center=(title_x, title_y))
        screen.blit(title, title_rect)

        # print the best score
        best_score_show = option_font.render(f"Best Score: {best_score}", True, WHITE)
        score_rect = best_score_show.get_rect(center=(title_x, title_y + 40))
        screen.blit(best_score_show, score_rect)

        # print the question
        again = option_font.render("Try again?", True, WHITE)
        again_rect = again.get_rect(topleft=(text_x, text_y))
        screen.blit(again, again_rect)

        
        for i, option in enumerate(options):
            color = WHITE if i == selected else YELLOW

            text = option_font.render(option, True, color)
            text_rect = text.get_rect(topleft=(text_x, text_y + (i + 1) * 40))
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
                    if options[selected] == "Yes":
                        return True
                    elif options[selected] == "No":
                        return False
                    
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

# Register player's name and score (Only in hard difficulty of classic mode)
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

# --- GAME ---

def game(mode, difficulty):
    # boolean variables for challenge mode toggle
    flipped_once = False
    speed_up_once = False

    global screen, current_background, best_score, hard_mode_unlocked
    
    # set up the speed according to the difficulty
    speed = SPEED_LEVELS[difficulty]
    speed_change = SPEED_CHANGES[difficulty]

    # Initialize sound
    pygame.mixer.init()
    pygame.mixer.music.load("Sound/Sound.mp3")  # Load background music
    pygame.mixer.music.play(-1)  # Loop the music indefinitely
    volume = 0.5
    pygame.mixer.music.set_volume(volume)

    
    # Initialize the snake
    # Snake is a list of (x, y) positions; start in the middle with length 3
    snake = [(CELL_COUNT // 2, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 1, CELL_COUNT // 2),
             (CELL_COUNT // 2 - 2, CELL_COUNT // 2)]

    font = pygame.font.Font(font_sellected, 30)

    # Ask player's name to store it later, only in hard difficulty
    player_name = None
    if difficulty == 'Hard' and mode == 'Classic Mode':
        font2 = pygame.font.Font(font_sellected, 20)
        player_name = get_player_name(screen, font2)

    
    # Initialize snake sounds
    movement_sound = pygame.mixer.Sound("Sound/movement.wav")
    eat_sound = pygame.mixer.Sound("Sound/eating.wav")
    death_sound = pygame.mixer.Sound("Sound/death-sound-pixel.wav")
    
    # The snake's direction (dx, dy). Start moving right.
    dx, dy = 1, 0

    # Place initial food and snake color
    snake_color = GREEN
    food = get_random_food_position()

    # Initialize teleport timer for the apple (in milliseconds)
    last_teleport_time = pygame.time.get_ticks()

    # define next directions, AVOID BUG OF SNAKE GOING INTO ITSELF
    next_dx, next_dy = dx, dy

    # Initialize score
    score = 0
    score_x = SCREEN_WIDTH // 17 # X position of the score
    score_y = SCOREBOARD_HEIGHT // 2 - 10  # Y position of the score

    # Set invisible mouse
    pygame.mouse.set_visible(False)

    running = True
    while running:
        clock.tick(speed)  # Adjust speed based on difficulty

        # --- CHALLENGE MODE TOGGLE ---
        if mode == "Challenge Mode":
            # only flips direction once every time you eat an apple
            if 5 <= score < 10 and not flipped_once:
                snake.reverse()

                x1, y1 = snake[0]
                x2, y2 = snake[1]

                dx = x1 - x2
                dy = y1 - y2

                next_dx = dx
                next_dy = dy

                flipped_once = True
            # only speeds up once every time you eat an apple
            elif 10 <= score < 15 and not speed_up_once:
                speed *= 1.25
                speed_up_once = True 
                if score == 14: # resets the speed
                    speed /= pow(1.25, 4)
            elif 15 <= score < 20:
                # Teleporting apple: update food position every 10 seconds
                current_time = pygame.time.get_ticks()
                if current_time - last_teleport_time >= 10000:  # 10,000 milliseconds = 10 seconds
                    # Generate a new food position
                    food = get_random_food_position()
                    last_teleport_time = current_time
            elif 20 <= score < 25:
                pass # Call 4th challenge function
            elif 25 <= score < 30:
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
                    pause_menu(screen, mode, difficulty)
                elif event.key == pygame.K_b:  # Change background
                    current_background = (current_background + 1) % len(backgrounds)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # Increase volume
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_MINUS:  # Decrease volume
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
        
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
            pygame.time.delay(700)  # Wait for a second to let the sound play

            # Show death menu 
            if not death_menu(score, player_name):
                game(mode, difficulty) # restart
            else:
                main() # back to mm

        # If still safe, insert new head
        snake.insert(0, new_head)

        # 3. Check if we ate the food
        if new_head == (food[0], food[1]):
            play_sound(eat_sound) # play snake eat food sound
            snake_color = food[2] # changes snake color based on food
            speed += speed_change # increase snake speed after eating food
            score += 1  # Increase score by 1 when food is eaten

            if mode == "Classic Mode" and not hard_mode_unlocked:
                if (score >= 10 and difficulty == 'Hard') or (score >= 20 and difficulty == 'Normal'):
                    hard_mode_unlocked = True

            # Generate a new food position; don't pop the tail (snake grows)
            temp_food = get_random_food_position()
            while temp_food in snake or temp_food is new_head:
                temp_food = get_random_food_position()
            food = temp_food

            # mark these variables as False so that we can flip/speed up again when eating an apple
            flipped_once = False
            speed_up_once = False
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


def main():
    global screen, best_score

    # turn off the music 
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

    # show the main menu and get the mode
    mode = main_menu(screen)

    # set the difficulty that sets the speed according to the mode
    if mode == "Challenge Mode":
        difficulty = 'Hard'
    else:
        difficulty = classic_mode_screen(screen)

    # run the game
    game(mode, difficulty)

if __name__ == "__main__":
    main()