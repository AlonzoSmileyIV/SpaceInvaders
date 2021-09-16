import pygame
import os
# Get text
pygame.font.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)

WIDTH , HEIGHT = 900, 500 # Init width and height of game
WIDTH_MIDDLE, HEIGHT_MIDDLE = WIDTH // 2, HEIGHT // 2
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Set width and height of game screen

pygame.display.set_caption("SPACE INVADER") #Set caption of the window on top

pygame.mixer.music.load(os.path.join('Assets','ICare4U.mp3'))
pygame.mixer.music.set_volume(0.7)
# pygame.mixer.music.play()
####  COLORS   ####
BLUE = (28, 167, 236)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Width of your border
BORDER_WIDTH = 10
# Create border x, y, width, height
BORDER = pygame.Rect(WIDTH_MIDDLE - (BORDER_WIDTH // 2), 0, BORDER_WIDTH, HEIGHT)

VEL = 5 #Speed of movement
FPS = 60 #Frames per second, for speeding purposes
BULLET_VEL = 7 #Bullet velocity
MAX_BULLETS = 5 # Number of bullets allowed

SPACESHIP_WIDTH , SPACESHIP_HEIGHT = 55, 40 #Init width and height of spaceship

# Creat new event
YELLOW_HIT = pygame.USEREVENT + 1 
RED_HIT = pygame.USEREVENT + 2

#Get images of both spaceships
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png')) 
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))

# Scaling spaceships to the size wanted and the way you want to rotate it
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),270)


BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets','space.png')), (WIDTH, HEIGHT)) # Add background

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND_IMAGE, (0,0))  #Set background image in window
    pygame.draw.rect(WIN, BLACK, BORDER) #Draw BLACK BORDER in WIN

    # Get the text for healths
    red_health_text = HEALTH_FONT.render("Red's Health: " + str(red_health), 1, RED)
    yellow_health_text = HEALTH_FONT.render("Yellow's Health: " + str(yellow_health), 1, YELLOW)

    #Place healths appropriately
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #Add onto the screen @ location (250, 450)
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) #Add onto the screen @ location (250, 450)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet) #Add each bullet to window
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet) #Add each bullet to window
    pygame.display.update() #Update it


def handle_movements(keys_pressed, red, yellow):
    ## CHECK YELLOW 
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # if 'w' is pressed, UP for YELLOW ship
            yellow.y -= VEL

    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height + 15 < HEIGHT: # if 's' is pressed, DOWN for YELLOW ship
        yellow.y += VEL

    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # if 's' is pressed, LEFT for YELLOW ship
        yellow.x -= VEL
    
    if keys_pressed[pygame.K_d] and yellow.x - VEL + yellow.width  < BORDER.x : # if 's' is pressed, RIGHT for YELLOW ship
        yellow.x += VEL


    ## CHECK RED
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # if 'UP' is pressed, UP for RED ship
        red.y -= VEL

    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height + 15 < HEIGHT: # if 'DOWN' is pressed, DOWN for RED ship
        red.y += VEL
    
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # if 'LEFT' is pressed, LEFT for RED ship
        red.x -= VEL
    
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # if 'RIGHT' is pressed, RIGHT for RED ship
        red.x += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets: #Go through each bullet
        bullet.x += BULLET_VEL #Increment 7 times to the right
        if red.colliderect(bullet): #If red touches bullet
            pygame.event.post(pygame.event.Event(RED_HIT)) #Make new event
            yellow_bullets.remove(bullet) #Remove the bullet
        elif bullet.x > WIDTH: # If off screen, remove bullet
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets: #Go through each bullet
        bullet.x -= BULLET_VEL #Decrement 7 times to the left
        if yellow.colliderect(bullet): #If yellow touches bullet
            pygame.event.post(pygame.event.Event(YELLOW_HIT)) #Make new event
            red_bullets.remove(bullet) #Remove the bullet
        elif bullet.x < 0: # If off screen, remove bullet
            red_bullets.remove(bullet)

def draw_winner(text, winner_color):
    draw_text = WINNER_FONT.render(text, 1, winner_color) #Text
    WIN.blit(draw_text, (WIDTH_MIDDLE - draw_text.get_width() // 2, 
    HEIGHT_MIDDLE - draw_text.get_height() // 2)) #Set text in window
    pygame.mixer.music.stop()
    pygame.display.update() #Update
    pygame.time.delay(5000) #Pause the game

def main():
    pygame.mixer.music.play()
    #Create rectangles tied to spaceships
    red = pygame.Rect(700, HEIGHT_MIDDLE, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, HEIGHT_MIDDLE, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    red_health = 10
    yellow_bullets = []
    yellow_health = 10

    clock = pygame.time.Clock() #create an object to help track time
    running = True
    while running: #Keep running
        clock.tick(FPS) #controls speed of while loop
        for event in pygame.event.get(): #Go through each event
            if event.type == pygame.QUIT:# If you quit, stop running
                running = False
                pygame.quit() #Quit the game
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: # if left Ctrl button is pressed, get bullet
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS: # if right Ctrl button is pressed, get bullet
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT: #When RED_HIT event triggered
                red_health -= 1
                # BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT: #When YELLOW_HIT event triggered
                yellow_health -= 1
                # BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0: #If red dies
            winner_text = "Yellow Wins!"
            winner_color = YELLOW
        if yellow_health <= 0: #If yellow dies
            winner_text = "Red Wins!"
            winner_color = RED
        if winner_text != "": #If there is a winner
            draw_winner(winner_text, winner_color)
            break #break from the while loop, and gave will start over

        keys_pressed = pygame.key.get_pressed() #Let's us know which key is being pressed down
        handle_movements(keys_pressed, red, yellow) #Handle movements based on keypress
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health) #Set window attributes

    main() #Restart the game


if __name__ == "__main__": #Run this main, if we running THIS file directly
    main() #Main loop
