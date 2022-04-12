#Importing modules
import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

#Setting window parameters
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

#Color hex values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

#Middle partition coordinates
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#Sound variables
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
SB_HIT_SOUND = pygame.mixer.Sound('Assets/samck.mp3')
SB_FIRE_SOUND = pygame.mixer.Sound('Assets/gunshot.mp3')
HP_HIT_SOUND = pygame.mixer.Sound('Assets/hp.mp3')

#Font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
SB_FONT = pygame.font.SysFont('comicsans', 20)

#Game Global variables
FPS = 60
VEL = 5
BULLET_VEL = 7
SB_VEL = 10
MAX_BULLETS = 3
MAX_SB = 1
MAX_HP = 6
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

#Creating separate events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
YELLOW_SB_HIT = pygame.USEREVENT + 3
RED_SB_HIT = pygame.USEREVENT + 4
YELLOW_HP_HIT = pygame.USEREVENT + 5
RED_HP_HIT = pygame.USEREVENT + 6


#Loading images for the spaceship and resizing them
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

#Function to draw the window
def draw_window(red, yellow, red_bullets, yellow_bullets, red_sb, yellow_sb,
                                     red_health, yellow_health, red_sb_count, yellow_sb_count, health_powerup):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    #Health on the screen
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    #SB ammo on the screen
    red_sb_text = SB_FONT.render(
        "Silver Bullets: " + str(red_sb_count), 1, WHITE)
    yellow_sb_text = SB_FONT.render(
        "Silver Bullets: " + str(yellow_sb_count), 1, WHITE)
    WIN.blit(red_sb_text, (WIDTH - red_sb_text.get_width() - 250, 10))
    WIN.blit(yellow_sb_text, (250, 10))

    for hp in health_powerup:
        pygame.draw.rect(WIN, GREEN, hp)
        
    #Spaceship blit
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for sb in red_sb:
        pygame.draw.rect(WIN, WHITE, sb)

    for sb in yellow_sb:
        pygame.draw.rect(WIN, WHITE, sb)

    pygame.display.update()

#Function that handles yellow movement
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL

#Function that handles red movement
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL

#Function that handles bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

#Function that handles silver bullets
def handle_sb(yellow_sb, red_sb, yellow, red):
    
    for sb in yellow_sb:
        sb.x += SB_VEL
        if red.colliderect(sb):
            pygame.event.post(pygame.event.Event(RED_SB_HIT))
            yellow_sb.remove(sb)
        elif sb.x > WIDTH:
            yellow_sb.remove(sb)

    for sb in red_sb:
        sb.x -= SB_VEL
        if yellow.colliderect(sb):
            pygame.event.post(pygame.event.Event(YELLOW_SB_HIT))
            red_sb.remove(sb)
        elif sb.x < 0:
            red_sb.remove(sb)

#Function to handle health powerup
def handle_hp(health_powerup, yellow, red):
    for hp in health_powerup:
        if red.colliderect(hp):
            pygame.event.post(pygame.event.Event(RED_HP_HIT))
            health_powerup.remove(hp)

    for hp in health_powerup:
        if yellow.colliderect(hp):
            pygame.event.post(pygame.event.Event(YELLOW_HP_HIT))
            health_powerup.remove(hp)

#Function for the winner text after game ends
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

#Main game function
def main():
    #Positioning of spaceships
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    red_sb = []
    yellow_sb = []
    health_powerup = []

    count = 0
    while(count < MAX_HP):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        hp = pygame.Rect(x, y, 15, 15)
        health_powerup.append(hp)
        count += 1

    #Setting max health
    red_health = 10
    yellow_health = 10

    #Silver bullet max ammo
    red_sb_count = 3
    yellow_sb_count = 3

    clock = pygame.time.Clock()
    run = True

    #Game Loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LSHIFT and len(yellow_sb) < MAX_SB and yellow_sb_count > 0:
                    sb = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_sb.append(sb)
                    SB_FIRE_SOUND.play()
                    yellow_sb_count -= 1

                if event.key == pygame.K_RSHIFT and len(red_sb) < MAX_SB and red_sb_count > 0:
                    sb = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_sb.append(sb)
                    SB_FIRE_SOUND.play()
                    red_sb_count -= 1

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_SB_HIT:
                red_health -= 3
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_SB_HIT:
                yellow_health -= 3
                BULLET_HIT_SOUND.play()

            if event.type == RED_HP_HIT:
                red_health += 1
                HP_HIT_SOUND.play()

            if event.type == YELLOW_HP_HIT:
                yellow_health += 1
                HP_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        
        #Function Calls
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        handle_sb(yellow_sb, red_sb, yellow, red)
        handle_hp(health_powerup, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_sb, yellow_sb,
                    red_health, yellow_health, red_sb_count, yellow_sb_count, health_powerup)

    main()


if __name__ == "__main__":
    main()