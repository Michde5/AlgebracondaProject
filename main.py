import pygame, sys
import random
from game import colors, fonts
from pygame import mixer

# Initialize pygame
pygame.init()

# Initialize flags
click = False
run = True
playgame = False
capture = False                 # Player has not yet captured diamond. Capture flag set to false.
treasure_located = False        # Player has not yet brought diamond to treasure chest. Treasure flag set to false.
false_treasure = False          # Player has not captured a false treasure

# Specs for game play screen
GRID_SIZE = 32      # Space between grid lines
LINE_WIDTH = 1      # Weight of each grid line
X_AXIS_MAX = 10
X_AXIS_MIN = -10
Y_AXIS_MAX = 10
Y_AXIS_MIN = -10
total_xAxis_length = X_AXIS_MAX - X_AXIS_MIN
total_yAxis_length = Y_AXIS_MAX - Y_AXIS_MIN
move_distance = GRID_SIZE + LINE_WIDTH              # Distance required to move from one coordinate to the next
lattice_point = GRID_SIZE // 2                      # Divide grid size by 2 so object appears on lattice points
WIDTH = move_distance * (total_xAxis_length + 2)    # Width of screen
HEIGHT = move_distance * (total_yAxis_length + 2)   # Height of screen
WIDTHScreen = WIDTH
HEIGHTScreen = HEIGHT

# Background of game play screen
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Screen1 Background Music
mixer.music.load("assets/screen1.ogg")
mixer.music.play(-1, 0.0)

# Title and icon on top window bar
icon = pygame.image.load("assets/snake.png")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("ALGEBRACONDA")
pygame.display.set_icon(icon)

global score_value

# scoreboard Setup
score_value = 0
level_value = 1
scoreTxt_X = move_distance * (total_xAxis_length - 20)
scoreTxt_Y = move_distance * (total_yAxis_length + 1)


def show_score(WIDTH, HEIGHT):
    score = fonts.score_font.render(
        "Score: " + str(score_value) + "/100.  " "Level 1: " + str(100 - score_value) + " coins away from next level!",
        True, colors.dred, colors.white)
    screen.blit(score, (WIDTH, HEIGHT))


# load button images
start_img = pygame.image.load("assets/start_btn.png").convert_alpha()
exit_img = pygame.image.load("assets/exit_btn.png").convert_alpha()


# button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), (int(height * scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):

            if pygame.mouse.get_pressed()[
                0] == 1 and self.clicked == False:  # 0 for left click, 1 for middle click, and 2 for right click
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


# create button instances from the button class
start_button = Button(100, 200, start_img, 0.8)
exit_button = Button(450, 200, exit_img, 0.8)

# Set initial location for Algebraconda
player_x = lattice_point + (6 * move_distance)
player_y = lattice_point + (13 * move_distance)
playerX = player_x
playerY = player_y

# Location of the origin and diamond
origin_x = lattice_point + ((total_xAxis_length / 2) * move_distance)
origin_y = lattice_point + ((total_yAxis_length / 2) * move_distance)

# Random coordinates for the treasure
random_x = random.randint(0, X_AXIS_MAX)
random_y = random.randint(0, Y_AXIS_MAX)

# Create treasure chest location
treasure_x = lattice_point + ((abs(X_AXIS_MIN) + random_x) * move_distance)
treasure_y = lattice_point + ((Y_AXIS_MAX - random_y) * move_distance)

# Create false treasure locations
# False Treasure Location 1 - Quadrant II (-x, y) sandy brown
false_x1 = lattice_point + ((abs(X_AXIS_MIN) - random_x) * move_distance)
false_y1 = lattice_point + ((Y_AXIS_MAX - random_y) * move_distance)
wrong_x1 = false_x1
wrong_y1 = false_y1
wrong_x = wrong_x1
wrong_y = wrong_y1

# False Treasure Location 1A - Alternate location if False Treasure 1 is the same as Treasure.
# Flagged when (0, y). Alternate is plotted at (-y, 0)
false_x1A = lattice_point + ((abs(X_AXIS_MIN) - random_y) * move_distance)
false_y1A = origin_y

# False Treasure Location 2 - Quadrant IV (x, -y) blue
false_x2 = lattice_point + ((abs(X_AXIS_MIN) + random_x) * move_distance)
false_y2 = lattice_point + ((Y_AXIS_MAX + random_y) * move_distance)

# False Treasure Location 2A - Alternate location if False Treasure 2 is the same as Treasure.
# Flagged when (x, 0). Alternate is plotted at (0, -x)
false_x2A = origin_x
false_y2A = lattice_point + ((Y_AXIS_MAX + random_x) * move_distance)

# False Treasure Location 3 - Quadrant I (y, x) black
false_x3 = lattice_point + ((abs(X_AXIS_MIN) + random_y) * move_distance)
false_y3 = lattice_point + ((Y_AXIS_MAX - random_x) * move_distance)

# False Treasure Location 3A - If False treasure location 3 is the same as Treasure. When x = y.
# Flagged when x = y. Alternate is plotted at (-x, -y)
false_x3A = lattice_point + ((abs(X_AXIS_MIN) - random_x) * move_distance)
false_y3A = lattice_point + ((Y_AXIS_MAX + random_y) * move_distance)


# playGame class
class playGame():
    global capture, treasure_found, playerX, playerY, WIDTHScreen, HEIGHTScreen, score_value

    def __init__(self, player_x, player_y, WIDTH, HEIGHT):
        self.x = player_x
        self.y = player_y
        self.width = WIDTH
        self.height = HEIGHT
        self.lattice = lattice_point
        self.score_value = 0
        self.click = False
        self.run = True
        self.playgame = False
        self.capture = False
        self.treasure_located = False
        self.false_treasure = False

    def init_pos(self):  # Set initial location for Algebraconda
        self.x = lattice_point
        self.y = lattice_point

    def draw_plane(self):
        # Background Image
        screen.blit(background, (0, 0))

        # Display Score
        show_score(scoreTxt_X, scoreTxt_Y)

        # Draw vertical grid lines
        for i in range(-1, WIDTH, move_distance):
            pygame.draw.line(screen, colors.black, (i, 0), (i, HEIGHT), LINE_WIDTH)

        # Draw horizontal grid lines
        for j in range(-1, HEIGHT, move_distance):
            pygame.draw.line(screen, colors.black, (0, j), (WIDTH, j), LINE_WIDTH)

        # Create the x- and y-axis
        xAxis = lattice_point + origin_y
        yAxis = lattice_point + origin_x
        pygame.draw.line(background, colors.dred, (0, xAxis), (WIDTH, xAxis), 5 * LINE_WIDTH)
        pygame.draw.line(background, colors.dred, (yAxis, 0), (yAxis, HEIGHT), 5 * LINE_WIDTH)

        # Create right arrow on x-axis
        pygame.draw.line(background, colors.dred, (WIDTH - lattice_point, origin_y), (WIDTH, xAxis), 5 * LINE_WIDTH)
        pygame.draw.line(background, colors.dred, (WIDTH - lattice_point, origin_y + GRID_SIZE), (WIDTH, xAxis),
                         5 * LINE_WIDTH)

        # Create left arrow on x-axis
        pygame.draw.line(background, colors.dred, (0, xAxis), (lattice_point, origin_y), 5 * LINE_WIDTH)
        pygame.draw.line(background, colors.dred, (0, xAxis), (lattice_point, origin_y + GRID_SIZE), 5 * LINE_WIDTH)

        # Create top arrow on y-axis
        pygame.draw.line(background, colors.dred, (yAxis, 0), (origin_x + GRID_SIZE, lattice_point), 5 * LINE_WIDTH)
        pygame.draw.line(background, colors.dred, (yAxis, 0), (origin_x, lattice_point), 5 * LINE_WIDTH)

        # Create bottom arrow on y-axis
        pygame.draw.line(background, colors.dred, (yAxis, HEIGHT), (origin_x + GRID_SIZE, HEIGHT - lattice_point),
                         5 * LINE_WIDTH)
        pygame.draw.line(background, colors.dred, (yAxis, HEIGHT), (origin_x, HEIGHT - lattice_point), 5 * LINE_WIDTH)

        # Create the Tick Mark Numbers
        for xpos in range(10, -11, -1):
            xMark = str(xpos)
            xMark_text = fonts.axisFont.render(xMark, True, colors.nyellow, colors.dred)
            xMark_textRect = xMark_text.get_rect()
            xMark_textRect.center = ((move_distance * xpos) + origin_x + lattice_point, origin_y + GRID_SIZE)
            screen.blit(xMark_text, xMark_textRect)

        for ypos in range(10, -11, -1):
            yMark = str(ypos * -1)
            yMark_text = fonts.axisFont.render(yMark, True, colors.nyellow, colors.dred)
            yMark_textRect = yMark_text.get_rect()
            yMark_textRect.center = (origin_x, (move_distance * ypos) + origin_y + lattice_point)
            screen.blit(yMark_text, yMark_textRect)

    def draw_player(self):
        # Create sprite explorer
        sprite = pygame.image.load('assets/explorer.png')
        sprite = pygame.transform.scale(sprite, (55, 55))
        screen.blit(sprite, (player_x, player_y))

    def draw_diamond(self):
        # Create diamond at origin and display only when player has not captured diamond
        screen.blit(pygame.image.load('assets/diamond_blue_35x35.png'), (origin_x, origin_y))

        # Display diamond instructions
        instruct_msg = str('Your Mission: Capture the diamond at the Origin.')
        instruct_text = fonts.success_font.render(instruct_msg, True, colors.white, colors.sky_blue)
        instruct_textRect = instruct_text.get_rect()
        instruct_textRect.center = (origin_x + lattice_point, GRID_SIZE)
        screen.blit(instruct_text, instruct_textRect)

        instruct_msg2 = str('Beware of the Algebraconda!')
        instruct_text2 = fonts.success_font.render(instruct_msg2, True, colors.green, colors.sky_blue)
        instruct_textRect2 = instruct_text2.get_rect()
        instruct_textRect2.center = (origin_x + lattice_point, 2 * GRID_SIZE)
        screen.blit(instruct_text2, instruct_textRect2)

    # Draw treasure chests
    # Draw True Treasure Chest
    def draw_Tchest(self):
        screen.blit(pygame.image.load('assets/treasure_closed.png'), (treasure_x, treasure_y))

    # Draw False Treasure Chests
    def draw_Fchest1A(self):
        screen.blit(pygame.image.load('assets/treasure_closed.png'), (false_x1A, false_y1A))

    def draw_Fchest1(self):
        screen.blit(pygame.image.load('assets/treasure_closed.png'), (false_x1, false_y1))

    def draw_Fchest2A(self):
        screen.blit(pygame.image.load('assets/treasure_closed.png'), (false_x2A, false_y2A))

    def draw_Fchest2(self):
        screen.blit(pygame.image.load('assets/treasure_closed.png'), (false_x2, false_y2))

    def draw_Fchest3A(self):
        screen.blit(pygame.image.load('assets/treasure_closed.png'), (false_x3A, false_y3A))

    def draw_Fchest3(self):
        screen.blit(pygame.image.load('assets/treasure_closed.png'), (false_x3, false_y3))

    def capture_msg(self):
        # Display instructions message
        instruct_msg = str('NOW BRING THE DIAMOND TO (' + str(random_x) + ', ' + str(random_y) + ').')
        instruct_text = fonts.instruct_font.render(instruct_msg, True, colors.white, colors.sky_blue)
        instruct_textRect = instruct_text.get_rect()
        instruct_textRect.center = (origin_x, GRID_SIZE)
        screen.blit(instruct_text, instruct_textRect)


###  Game Loop  ###

def main(self, coin=None):  # Used to redraw the screen
    global score_value, run, playgame, capture, player_x, player_y, origin_x, \
        origin_y, treasure_x, treasure_y, treasure_located, event, wrong_x1, wrong_y1, \
        wrong_x, wrong_y, false_treasure, wrong_x2, false_x2A, wrong_y2, false_y2A, wrong_x3, \
        false_x3A, wrong_y3, false_y3A

    AlgGame = playGame(playerX, playerY, WIDTHScreen, HEIGHTScreen)

    while run:  # Only include critical code within this loop
        # Game Screen
        screen.fill(colors.sandy_brown)  # Set color of the main menu window

        if start_button.draw():
            playgame = True
            mixer.music.load("assets/catch.WAV")  # Background Sound
            mixer.music.play(-1, 0.0)

        if exit_button.draw():
            run = False

        if playgame:
            AlgGame.init_pos()
            AlgGame.draw_plane()
            AlgGame.draw_player()

            # Diamond Capture
            if capture == False:

                if ((player_x != origin_x) or (player_y != origin_y)):
                    AlgGame.draw_diamond()

                else:
                    capture = True  # Capture flag set to true, so diamond does not draw again after capture
                    diamond_hit = mixer.Sound("assets/diamond_hit.WAV")
                    diamond_hit.play()

            elif (capture == True) and (treasure_located == False) and (
                    false_treasure == False):  # Player has captured the diamond but has not found treasure
                AlgGame.capture_msg()

                # Draw treasure chests
                if ((player_x != treasure_x) or (player_y != treasure_y)):
                    # Draw True Treasure Chest
                    AlgGame.draw_Tchest()

                    # Draw False Treasure Chests

                    # If False Treasure Location 1 is the same as Treasure, draw Alternate location at (-y, 0)
                    if ((treasure_x == false_x1) or (treasure_y != false_y1)):
                        AlgGame.draw_Fchest1A()
                        wrong_x1 = false_x1A
                        wrong_y1 = false_y1A
                    # Else draw False Treasure 1 location - Quadrant II (-x, y)
                    else:
                        AlgGame.draw_Fchest1()
                        wrong_x1 = false_x1
                        wrong_y1 = false_y1

                    # False treasure 1 has been found
                    if ((player_x == wrong_x1) and (player_y == wrong_y1)):
                        wrong_x = wrong_x1
                        wrong_y = wrong_y1
                        false_treasure = True
                        diamond_hit = mixer.Sound("assets/diamond_hit.WAV")
                        diamond_hit.play()
                        # score_value -= 1

                    # If False Treasure Location 2 is the same as Treasure, draw Alternate location at (0, -x)
                    if ((treasure_x != false_x2) or (treasure_y == false_y2)):
                        AlgGame.draw_Fchest2A()
                        wrong_x2 = false_x2A
                        wrong_y2 = false_y2A
                    # Else draw False Treasure 2 location - Quadrant IV (x, -y)
                    else:
                        AlgGame.draw_Fchest2()
                        wrong_x2 = false_x2
                        wrong_y2 = false_y2

                    # False treasure 2 has been found
                    if ((player_x == wrong_x2) and (player_y == wrong_y2)):
                        wrong_x = wrong_x2
                        wrong_y = wrong_y2
                        false_treasure = True
                        diamond_hit = mixer.Sound("assets/diamond_hit.WAV")
                        diamond_hit.play()
                        # score_value -= 1

                    # If False Treasure Location 3 is the same as Treasure, draw Alternate location at (-x, -y)
                    if ((treasure_x == false_x3) or (treasure_y == false_y3)):
                        AlgGame.draw_Fchest3A()
                        wrong_x3 = false_x3A
                        wrong_y3 = false_y3A
                    # Else draw False Treasure 3 location - Quadrant I (y, x)
                    else:
                        AlgGame.draw_Fchest3()
                        wrong_x3 = false_x3
                        wrong_y3 = false_y3

                    # False treasure 3 has been found
                    if ((player_x == wrong_x3) and (player_y == wrong_y3)):
                        wrong_x = wrong_x3
                        wrong_y = wrong_y3
                        false_treasure = True
                        diamond_hit = mixer.Sound("assets/diamond_hit.WAV")
                        diamond_hit.play()
                        # score_value -= 1

                # True treasure has been found
                elif ((player_x == treasure_x) or (player_y == treasure_y)):
                    treasure_located = True
                    diamond_hit = mixer.Sound("assets/diamond_hit.WAV")
                    diamond_hit.play()
                    score_value += 20

            # Player has found the true treasure
            elif (treasure_located == True):
                # Display success message
                success_msg = str('Congratulations!! You have plotted (' + str(random_x) + ', ' + str(random_y) + ').')
                success_text = fonts.success_font.render(success_msg, True, colors.green, colors.sky_blue)
                success_textRect = success_text.get_rect()
                success_textRect.center = (WIDTH // 2, GRID_SIZE)
                screen.blit(success_text, success_textRect)

                # Display practice message #1
                practice_msg1 = str('Press (p) to Practice Again')
                practice_text = fonts.level_font.render(practice_msg1, True, colors.dblue, colors.sandy_brown)
                practice_textRect = practice_text.get_rect()
                practice_textRect.center = (WIDTH // 2, (HEIGHT // 2) + GRID_SIZE)
                screen.blit(practice_text, practice_textRect)

                # Display practice message #2
                practice_msg2 = str('Press (l) to Level Up')
                practice_text = fonts.level_font.render(practice_msg2, True, colors.dblue, colors.sandy_brown)
                practice_textRect = practice_text.get_rect()
                practice_textRect.center = (WIDTH // 2, (HEIGHT // 2 + 50) + GRID_SIZE)
                screen.blit(practice_text, practice_textRect)

                # Display practice message #3
                practice_msg3 = str('Press (q) or (Esc) to Quit')
                practice_text = fonts.level_font.render(practice_msg3, True, colors.dblue, colors.sandy_brown)
                practice_textRect = practice_text.get_rect()
                practice_textRect.center = (WIDTH // 2, (HEIGHT // 2 + 100) + GRID_SIZE)
                screen.blit(practice_text, practice_textRect)

                # Draw correct treasure with gold for player to reflect
                screen.blit(pygame.image.load('assets/treasure_gold.png'), (treasure_x, treasure_y))
                screen.blit(pygame.image.load('assets/coins.png'), (GRID_SIZE, HEIGHT - 3 * GRID_SIZE))

                # Draw sad snake
                sprite = pygame.image.load('assets/snake_sad.png')
                sprite = pygame.transform.scale(sprite, (45, 45))
                screen.blit(sprite, (treasure_x + GRID_SIZE, treasure_y + GRID_SIZE))

            # Player has found false treasure
            elif (false_treasure == True):
                # Display wrong plot message
                failure_msg = str('Sorry!! You did not plot (' + str(random_x) + ', ' + str(random_y) + ').')
                failure_text = fonts.success_font.render(failure_msg, True, colors.dred, colors.sky_blue)
                failure_textRect = failure_text.get_rect()
                failure_textRect.center = (WIDTH // 2, GRID_SIZE)
                screen.blit(failure_text, failure_textRect)

                failure_msg2 = str('The ALGEBRACONDA got you!')
                failure_text2 = fonts.level_font.render(failure_msg2, True, colors.green, colors.lblue)
                failure_textRect2 = failure_text2.get_rect()
                failure_textRect2.center = (WIDTH // 2, GRID_SIZE * 2)
                screen.blit(failure_text2, failure_textRect2)

                # Draw incorrect location for player to understand mistake
                screen.blit(pygame.image.load('assets/treasure_empty.png'), (wrong_x, wrong_y))
                screen.blit(pygame.image.load('assets/conda.png'), (wrong_x + GRID_SIZE, wrong_y + GRID_SIZE))

        ### Pygame Event Handler ###

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:  # Practice again
                    print("Restart here!")

                if event.key == pygame.K_l:  # Move on to the next level
                    print("Level Up here!")

                if event.key == pygame.K_ESCAPE:  # Quit the game option 1
                    print("Quit here!")
                    sys.exit(0)

                if event.key == pygame.K_q:  # Quit the game option 2
                    print("Quit here!")
                    sys.exit(0)

                if event.key == pygame.K_RIGHT:
                    if player_x < (move_distance * total_xAxis_length):
                        player_x = player_x + move_distance

                if event.key == pygame.K_LEFT:
                    if player_x > move_distance:
                        player_x = player_x - move_distance

                if event.key == pygame.K_UP:
                    if player_y > move_distance:
                        player_y = player_y - move_distance

                if event.key == pygame.K_DOWN:
                    if player_y < (move_distance * total_xAxis_length):
                        player_y = player_y + move_distance

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        pygame.display.update()
        clock.tick(60)  # Set the consistency of the speed


if __name__ == '__main__':
    main(playGame)
