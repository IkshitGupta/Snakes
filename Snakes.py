from collections import deque
import pygame, random, os, sys

pygame.mixer.init() # support music

pygame.init() # to initialise the modules in pygame

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height)) # used to initialize a screen for dislpay

# Background Image
bgimg = pygame.image.load("assets/Images/start_page.jpg") # to load the image
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha() # make it of screen size
# convert_alpha to improve game performance

ant = pygame.image.load("assets/Images/ant.webp")
ant = pygame.transform.scale(ant, (45, 45)).convert_alpha()

# high score file addresses
highscore_easy = "assets/High_scores/highscore_Easy.txt"
highscore_medium = "assets/High_scores/highscore_Medium.txt"
highscore_hard = "assets/High_scores/highscore_Hard.txt"

font1 = "assets/Fonts/SegoeUIVariableStaticTextBold.ttf"

pygame.display.set_caption('Snakes') # Setting Title
# origin is at top-left

def text_screen(text, colour, x, y, size) :
    font = pygame.font.Font(font1, size)
    screen_text = font.render(text, True, colour) # render used to draw text
    gameWindow.blit(screen_text, [x, y]) # to update screen with the given at required place

def text_screen_center(text, colour, x, y, size) :
    font = pygame.font.Font(font1, size)
    text = font.render(text, True, colour) # render used to draw text
    text_rect = text.get_rect(center=(x/2, y/2))
    gameWindow.blit(text, text_rect)

def plot_snake(gameWindow, snk_list, snake_size) :
    for i in range(len(snk_list)) :
        x = snk_list[i][0]
        y = snk_list[i][1]
        if i == len(snk_list) - 1 :
            pygame.draw.ellipse(gameWindow, (237,43,51,1), [x, y, snake_size, snake_size])
            continue
        pygame.draw.ellipse(gameWindow, (0,32,63,1),[x, y, snake_size, snake_size])

clock = pygame.time.Clock() # create an object to help track time

exit_game = False
fps = 60

# Welcome Screen
def welcome() :
    if not pygame.mixer.music.get_busy() :
        pygame.mixer.music.load("assets/Music/Welcome.mp3")  # loads music
        pygame.mixer.music.play()  # to play music
    global exit_game
    gameWindow.blit(bgimg, (0, 0))
    text_screen_center("Welcome To Snakes", (233,7,60,1), screen_width, 350, 41)
    text_screen_center("Press Spacebar to START", (7,83,156,1), screen_width, 460, 41)
    text_screen("Rules: Press 7", (120, 20, 20), 15, screen_height - 30, 22)
    pygame.display.update()

    while not exit_game :

        for event in pygame.event.get() : # any thing you do with mouse or keyboard will be recorded
            if event.type == pygame.QUIT:  # quit means cross button
                exit_game = True

            elif event.type == pygame.KEYDOWN : # if any key presses
                if event.key == pygame.K_SPACE : # .key i.e. if that particular key pressed
                    level()
                elif event.key == pygame.K_7:
                    rules('w')
        clock.tick(fps)

def rules(x) :
    global exit_game
    gameWindow.fill((41, 40, 38))
    colour = (249,211,66,1)
    text_screen("Back: Press 7", (130, 235, 235), 15, screen_height - 30, 22)
    text_screen_center("RULES", (255, 255, 255), screen_width, 200, 41)
    text_screen_center("The goal of the game is to eat ants and earn score.", colour, screen_width, screen_height - 150, 26)
    text_screen_center("Each time on eating an ant the snake grows.", colour, screen_width, screen_height - 75, 26)
    text_screen_center("Use arrow keys to navigate the snake in the four directions.", colour, screen_width, screen_height, 26)
    text_screen_center("If the snake collides with itself or the boundary, the game ends.", colour, screen_width, screen_height + 75, 26)
    text_screen_center("Use the ESC key to pause in-between the game.",colour, screen_width, screen_height + 150, 26)
    pygame.display.update()

    while not exit_game :

        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                exit_game = True

            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_7 :
                    if x == 'w' : welcome()
                    else : level()
        clock.tick(fps)

def level() :
    global exit_game
    gameWindow.fill((40, 50, 40))
    text_screen_center("Easy Mode: Press 1", (169,229,187,1), screen_width, screen_height - 150, 41)
    text_screen_center("Medium Mode: Press 2", (247,179,43,1), screen_width, screen_height, 41)
    text_screen_center("Hard Mode: Press 3", (227,23,10,1), screen_width, screen_height + 150, 41)
    text_screen("Rules: Press 7", (130, 235, 235), 15, screen_height - 30, 22)
    pygame.display.update()

    while not exit_game:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                exit_game = True

            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_1 :
                    game_loop('E')
                elif event.key == pygame.K_2 :
                    game_loop('M')
                elif event.key == pygame.K_3 :
                    game_loop('H')
                elif event.key == pygame.K_7:
                    rules('r')
        clock.tick(fps)

# Creating Game loop
def game_loop(mode) :
    # Game variables
    global exit_game
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    if mode == 'E' : v = 5
    elif mode == 'M' : v = 7
    else : v = 10
    snake_size = 30
    score = 0
    snk_list = deque()
    snk_set = set()
    snk_list_length = 1
    food_x = random.randint(30, screen_width - 30)
    food_y = random.randint(70, screen_height - 30)
    paused = False
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("assets/Music/playground.mp3")  # loads music
    pygame.mixer.music.play()  # to play music

    # reading highscore
    if mode == 'E' :
        if not os.path.exists(highscore_easy) :
            with open(highscore_easy, 'w') as f :
                f.write('0')
        with open(highscore_easy, "r") as f:
            highscore = f.read()

    elif mode == 'M' :
        if not os.path.exists(highscore_medium) :
            with open(highscore_medium, 'w') as f :
                f.write('0')
        with open(highscore_medium, "r") as f:
            highscore = f.read()
    else :
        if not os.path.exists(highscore_hard) :
            with open(highscore_hard, 'w') as f :
                f.write('0')
        with open(highscore_hard, "r") as f:
            highscore = f.read()

    while not exit_game :
        
        if game_over :
            # updating highscore
            if mode == 'E' :
                with open(highscore_easy, "w") as f:
                    f.write(str(highscore))
            elif mode == 'M' :
                with open(highscore_medium, "w") as f:
                    f.write(str(highscore))
            else:
                with open(highscore_hard, "w") as f:
                    f.write(str(highscore))

            gameWindow.fill((40, 50, 40))
            text_screen_center('Score :  ' + str(score), (169,229,187,1), screen_width, screen_height - 200, 49)
            text_screen_center("GAME OVER !!", (227,23,10,1), screen_width, screen_height, 100)
            text_screen_center('Press Enter to Play Again', (247,179,43,1), screen_width, screen_height + 200, 56)

            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    exit_game = True

                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RETURN :
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        welcome()

        else:
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    exit_game = True

                elif event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RIGHT :
                        velocity_x = v
                        velocity_y = 0

                    elif event.key == pygame.K_LEFT :
                        velocity_x = -v
                        velocity_y = 0

                    elif event.key == pygame.K_UP :
                        velocity_y = -v
                        velocity_x = 0

                    elif event.key == pygame.K_DOWN :
                        velocity_y = v
                        velocity_x = 0
                    
                    elif event.key == pygame.K_ESCAPE :
                        paused ^= 1
                        
            if paused:
                continue

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 25 and abs(snake_y - food_y) < 25 : # in this case change food coordinate
                food_x = random.randint(45, screen_width - 45)
                food_y = random.randint(85, screen_height - 45)
                score += 10
                snk_list_length += 5
                if score > int(highscore):
                    highscore = score
                v += 0.05   # gradual increment in speed on eating an ant

            gameWindow.fill((125,200,108,1))
            text_screen('Score: ' + str(score), (133,16,43,1), 10, 5, 33) # first argument takes string
            if mode == 'E' : text_screen_center('EASY', (53,20,43,50), screen_width, 45, 33)
            elif mode == 'M' : text_screen_center('MEDIUM', (53,20,43,50), screen_width, 45, 33)
            else : text_screen_center('HARD', (53,20,43,50), screen_width, 45, 33)
            text_screen('High Score: ' + str(highscore), (86,16,20,1), screen_width - 200, 10, 26)

            head = (snake_x, snake_y)
            # snk_list.append(head)

            if len(snk_list) + 1 > snk_list_length: # in the list the coordinates gets updated; so if snake is not eating
                snk_set.remove(snk_list.popleft())  # added new co-ordinate and removed old

            # collision with boundary
            if snake_y < 10 or snake_y + 10 > screen_height or snake_x < 10 or snake_x + 10 > screen_width :
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('assets/Music/Game_Over.mp3')
                pygame.mixer.music.play() 
                game_over = True
            # collision with itself
            if head in snk_set :
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('assets/Music/Game_Over.mp3')
                pygame.mixer.music.play() 
                game_over = True
            
            snk_list.append(head)
            snk_set.add(head)

            plot_snake(gameWindow, snk_list, snake_size)
            gameWindow.blit(ant, (food_x, food_y))

        pygame.display.update()  # nothing will happen if not updating, to update game
        clock.tick(fps) # update the clock in given frame per seconds
        # if less fps then fast updation, more speed

    pygame.quit()
    sys.exit()

welcome()