import pygame, sys
import random
import colors
import fonts
from pygame import mixer

# Initialize pygame
pygame.init()

# Initialize flags
click = False
run = True
playgame = False
capture = False             # Player has not yet captured diamond. Capture flag set to false.
treasure_located = False    # Player has not yet brought diamond to treasure chest. Treasure flag set to false.

# Specs for game play screen
GRID_SIZE = 32      # Space between grid lines
LINE_WIDTH = 1      # Weight of each grid line
X_AXIS_MAX = 10
X_AXIS_MIN = -10
Y_AXIS_MAX = 10
Y_AXIS_MIN = -10
total_xAxis_length = X_AXIS_MAX - X_AXIS_MIN
total_yAxis_length = Y_AXIS_MAX - Y_AXIS_MIN
move_distance = GRID_SIZE + LINE_WIDTH          # Distance required to move from one coordinate to the next
lattice_point = GRID_SIZE // 2                  # Divide grid size by 2 so object appears on lattice points
WIDTH = move_distance * (total_xAxis_length + 2)        # Width of screen
HEIGHT = move_distance * (total_yAxis_length + 2)       # Height of screen

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

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:    # 0 for left click, 1 for middle click, and 2 for right click
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
player_x = lattice_point
player_y = lattice_point

# Location of the origin and diamond
origin_x = lattice_point + ((total_xAxis_length / 2) * move_distance)
origin_y = lattice_point + ((total_yAxis_length / 2) * move_distance)

# Random coordinates for the treasure
random_x = random.randint(0, X_AXIS_MAX)
random_y = 0
#random_y = random.randint(0, Y_AXIS_MAX)

while run:  # Only include critical code within this loop
    # Set color of the main menu window
    screen.fill(colors.sandy_brown)

    if start_button.draw():
        playgame = True

        # Background Sound
        mixer.music.load("assets/catch.WAV")
        mixer.music.play(-1, 0.0)

    if exit_button.draw():
        run = False

    if playgame:
        # Background Image
        screen.blit(background, (0, 0))

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
        pygame.draw.line(background, colors.dred, (WIDTH - lattice_point, origin_y + GRID_SIZE), (WIDTH, xAxis), 5 * LINE_WIDTH)

        # Create left arrow on x-axis
        pygame.draw.line(background, colors.dred, (0, xAxis), (lattice_point, origin_y), 5 * LINE_WIDTH)
        pygame.draw.line(background, colors.dred, (0, xAxis), (lattice_point, origin_y + GRID_SIZE), 5 * LINE_WIDTH)

        # Create top arrow on y-axis
        pygame.draw.line(background, colors.dred, (yAxis, 0), (origin_x + GRID_SIZE, lattice_point), 5 * LINE_WIDTH)
        pygame.draw.line(background, colors.dred, (yAxis, 0), (origin_x, lattice_point), 5 * LINE_WIDTH)

        # Create bottom arrow on y-axis
        pygame.draw.line(background, colors.dred, (yAxis, HEIGHT), (origin_x + GRID_SIZE, HEIGHT - lattice_point), 5 * LINE_WIDTH)
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

        # Create green square for Algebraconda. Rect Arguments (x-coord, y-coord, width, height)
        pygame.draw.rect(screen, colors.green, pygame.Rect(player_x, player_y, GRID_SIZE, GRID_SIZE))

        # Create diamond at origin and draw when player has not captured diamond
        if capture == False:
            if ((player_x != origin_x) or (player_y != origin_y)):
                pygame.draw.rect(screen, colors.blue, pygame.Rect(origin_x, origin_y, GRID_SIZE, GRID_SIZE))
            else:
                capture = True      # Capture flag set to true, so diamond does not draw again after capture
                diamond_hit = mixer.Sound("assets/diamond_hit.WAV")
                diamond_hit.play()

        # Player has captured the diamond but has not found treasure
        elif (capture == True) and (treasure_located == False):
            # Display capture message
            capture_msg = str('Congratulations! You have captured the DIAMOND!')
            capture_text = fonts.capture_font.render(capture_msg, True, colors.blue, colors.sandy_brown)
            capture_textRect = capture_text.get_rect()
            capture_textRect.center = (origin_x, HEIGHT // 2 + move_distance)
            screen.blit(capture_text, capture_textRect)

            # Display instructions message
            instruct_msg = str('NOW BRING THE DIAMOND TO (' + str(random_x) + ', ' + str(random_y) + ').')
            instruct_text = fonts.instruct_font.render(instruct_msg, True, colors.white, colors.sandy_brown)
            instruct_textRect = instruct_text.get_rect()
            instruct_textRect.center = (origin_x, GRID_SIZE)
            screen.blit(instruct_text, instruct_textRect)

            # Create treasure chest location
            treasure_x = lattice_point + ((abs(X_AXIS_MIN) + random_x) * move_distance)
            treasure_y = lattice_point + ((Y_AXIS_MAX - random_y) * move_distance)
            # print("Treasure:", treasure_x, treasure_y)

            # Create false treasure locations
            # False treasure location 1 - Quadrant II (-x, y) sandy brown
            false_x1 = lattice_point + ((abs(X_AXIS_MIN) - random_x) * move_distance)
            false_y1 = lattice_point + ((Y_AXIS_MAX - random_y) * move_distance)

            # False treasure location 1A - If treasure = false 1. When (0, y)
            false_x1A = lattice_point + ((abs(X_AXIS_MIN) - random_y) * move_distance)
            false_y1A = lattice_point + ((Y_AXIS_MAX - random_x) * move_distance)

            # False treasure location 2 - Quadrant IV (x, -y) blue
            false_x2 = lattice_point + ((abs(X_AXIS_MIN) + random_x) * move_distance)
            false_y2 = lattice_point + ((Y_AXIS_MAX + random_y) * move_distance)

            # False treasure location 2A - If treasure = false 2. When (x, 0)
            false_x2A = origin_x
            false_y2A = lattice_point + ((Y_AXIS_MAX + random_x) * move_distance)

            # False treasure location 3 - Quadrant I (y, x) black
            false_x3 = lattice_point + ((abs(X_AXIS_MIN) + random_y) * move_distance)
            false_y3 = lattice_point + ((Y_AXIS_MAX - random_x) * move_distance)

            # Draw treasure chests
            if ((player_x != treasure_x) or (player_y != treasure_y)):
                # If Treasure = False treasure 1 location
                if ((treasure_x == false_x1) or (treasure_y != false_y1)):
                    pygame.draw.rect(screen, colors.sandy_brown, pygame.Rect(false_x1A, false_y1A, GRID_SIZE, GRID_SIZE))
                else:
                    pygame.draw.rect(screen, colors.sandy_brown, pygame.Rect(false_x1, false_y1, GRID_SIZE, GRID_SIZE))

                # If Treasure = False treasure 2 location
                if ((treasure_x != false_x2) or (treasure_y == false_y2)):
                    pygame.draw.rect(screen, colors.blue, pygame.Rect(false_x2A, false_y2A, GRID_SIZE, GRID_SIZE))
                else:
                    pygame.draw.rect(screen, colors.blue, pygame.Rect(false_x2, false_y2, GRID_SIZE, GRID_SIZE))

                pygame.draw.rect(screen, colors.black, pygame.Rect(false_x3, false_y3, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, colors.red, pygame.Rect(treasure_x, treasure_y, GRID_SIZE, GRID_SIZE))

            else:
                treasure_located = True

        else:       # Treasure has been located
            # Display success message
            success_msg = str('Congratulations!! You have plotted (' + str(random_x) + ', ' + str(random_y) + ').')
            success_text = fonts.success_font.render(success_msg, True, colors.green, colors.sandy_brown)
            success_textRect = success_text.get_rect()
            success_textRect.center = (WIDTH // 2, GRID_SIZE)
            screen.blit(success_text, success_textRect)

            # Display level message
            level_msg = str('Would you like to practice more or go to the next level?')
            level_text = fonts.level_font.render(level_msg, True, colors.blue, colors.sandy_brown)
            level_textRect = level_text.get_rect()
            level_textRect.center = (WIDTH // 2, (HEIGHT // 2) + GRID_SIZE)
            screen.blit(level_text, level_textRect)

    click = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
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
            sys.exit()

    pygame.display.update()
    clock.tick(60)  # Set the consistency of the speed