import sys, os
import pygame
import random
from pygame.locals import K_a, K_d, K_s, KEYDOWN, KEYUP

pygame.init()

# Fonts
font = pygame.font.Font('RubikIso-Regular.ttf', 50)
font2 = pygame.font.Font('Daydream.ttf', 25)

# Load images
winscreen = pygame.image.load('win screen.png')
gold = pygame.image.load('gold.png')
clockimage = pygame.image.load('clock.png')
emptyarrow = pygame.image.load('empty upgrade.png')
upgradearrow = pygame.image.load('filled upgrade.png')
shopgameimage = pygame.image.load('game screen menu.png')
startgameimage = pygame.image.load('game night.png')
stoneblock = pygame.image.load('stoneblock.png')
goldblock = pygame.image.load('goldblock.png')
brokenblock = pygame.image.load('brokenblock.png')
spriteright1 = pygame.image.load('New Piskel-1.png.png')
spriteright2 = pygame.image.load('New Piskel-2.png.png')
spriteright3 = pygame.image.load('New Piskel-3.png.png')
spriteright4 = pygame.image.load('New Piskel-4.png.png')
spriteright5 = pygame.image.load('New Piskel-5.png.png')
spriteleft1 = pygame.image.load('spriteleft1.png')
spriteleft2 = pygame.image.load('spriteleft2.png')
spriteleft3 = pygame.image.load('spriteleft3.png')
spriteleft4 = pygame.image.load('spriteleft4.png')
spriteleft5 = pygame.image.load('spriteleft5.png')
idle1 = pygame.image.load('idle1.png')
idle2 = pygame.image.load('idle2.png')
idle3 = pygame.image.load('idle3.png')
idle4 = pygame.image.load('idle4.png')
idle5 = pygame.image.load('idle5.png')

# Screen setup
width = 700
height = 650
SIZE = (width, height)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Spritesheets')

# Scale images
gold = pygame.transform.scale(gold, (100, 100))
clockimage = pygame.transform.scale(clockimage, (50, 50))
spriteright1 = pygame.transform.scale(spriteright1, (50, 50))
spriteright2 = pygame.transform.scale(spriteright2, (50, 50))
spriteright3 = pygame.transform.scale(spriteright3, (50, 50))
spriteright4 = pygame.transform.scale(spriteright4, (50, 50))
spriteright5 = pygame.transform.scale(spriteright5, (50, 50))
spriteleft1 = pygame.transform.scale(spriteleft1, (50, 50))
spriteleft2 = pygame.transform.scale(spriteleft2, (50, 50))
spriteleft3 = pygame.transform.scale(spriteleft3, (50, 50))
spriteleft4 = pygame.transform.scale(spriteleft4, (50, 50))
spriteleft5 = pygame.transform.scale(spriteleft5, (50, 50))
idle1 = pygame.transform.scale(idle1, (50, 50))
idle2 = pygame.transform.scale(idle2, (50, 50))
idle3 = pygame.transform.scale(idle3, (50, 50))
idle4 = pygame.transform.scale(idle4, (50, 50))
idle5 = pygame.transform.scale(idle5, (50, 50))
stoneblock = pygame.transform.scale(stoneblock, (50, 50))
goldblock = pygame.transform.scale(goldblock, (50, 50))
brokenblock = pygame.transform.scale(brokenblock, (50, 50))

# Game variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
blocksize = 50
imagesright = [spriteright1, spriteright2, spriteright3, spriteright4, spriteright5]
imagesleft = [spriteleft1, spriteleft2, spriteleft3, spriteleft4, spriteleft5]
idle = [idle1, idle2, idle3, idle4, idle5]
frame = 0
char_width = 30
char_height = 30
char_x = 350
char_y = 0
char_speed = 0.25
frame_rate = 200
upgradepickaxe = 0
upgradetimer = 0
facing = "idle"
depth = 0
score = 0
price = 2
price2 = 2
last_frame_time = pygame.time.get_ticks()
# Timer settings
countdown_time = 15 #in seconds
start_ticks = pygame.time.get_ticks()  # Start time in milliseconds

# Map generation
full_map = []
listofblocks = [0, 1]
for _ in range(240):
    full_map.append(random.choices(listofblocks, weights=(100, 20), k=100))

# Flags
gamerun = True
menuScreen = True
gameScreen = False
shopScreen = False
timer = True


def shop(): 
    screen.blit(shopgameimage, (0, 0))
    #empty upgrade arrows
    for i in range(4 - upgradepickaxe):
        screen.blit(emptyarrow, (420 - (i * 60), 365))
    for i in range(upgradepickaxe):
        screen.blit(upgradearrow, (240 + (i * 60), 365))

    #filled upgrade arrows
    for i in range(4 - upgradetimer):
        screen.blit(emptyarrow, (420 - (i * 60), 560))
    for i in range(upgradetimer):
        screen.blit(upgradearrow, (240 + (i * 60), 560))

    #Score Counter
    score_text = font2.render(f"Points: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def startScreen():
    screen.blit(startgameimage, (0, 0))
    pygame.display.update()


def game():
    global frame, last_frame_time, depth, gameScreen, menuScreen, shopScreen, score
    # Handle sprite animation
    teleport_text = font2.render("Teleporting", True, WHITE)
    screen.blit(teleport_text, (225, 500))
    current_time = pygame.time.get_ticks()
    #slow down animation
    if current_time - last_frame_time >= frame_rate:
        frame += 1
        if frame >= len(imagesright):
            frame = 0
        last_frame_time = current_time

    # Drawing the game screen
    screen.fill(BLACK)
    y = 120 - depth
    for row in full_map:
        x = 0
        for block in row:
            if block == 0:
                screen.blit(stoneblock, (x, y))
            elif block == 1:
                screen.blit(goldblock, (x, y))
            elif block == 2:
                screen.blit(brokenblock, (x, y))
            x += blocksize
        y += blocksize
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, countdown_time - elapsed_seconds)

    # Drawing timer
    timer_text = font2.render(f"{time_left}", True, WHITE)
    screen.blit(timer_text, (60, 10))
    # Drawing Score Counter
    score_text = font2.render(f"{score}", True, WHITE)
    screen.blit(score_text, (60, 55))
    screen.blit(clockimage, (5, 5))
    screen.blit(gold, (-20, 20))

    if depth > 2000 and char_y >= 170:
        gameScreen = False
        menuScreen = False
        shopScreen = False
        win_screen()
        return

    if time_left == 0:
        gameScreen = False
        shopScreen = True


def win_screen():
    screen.blit(winscreen, (0, 0))

    pygame.display.update()


def main():
    global char_x, char_y, gamerun, menuScreen, gameScreen, facing, depth, counter, text, clock, score, shopScreen, upgradepickaxe, upgradetimer, price, full_map, listofblocks, char_speed, price2, countdown_time
    KEY_LEFT = False
    KEY_RIGHT = False
    KEY_D = False
    max_speed = 0.5  # Set a max speed limit so the player doesn't move too fast

    while gamerun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Move left
                    KEY_LEFT = True
                    KEY_RIGHT = False
                    facing = "left"
                elif event.key == pygame.K_s:  # Move down
                    KEY_D = True
                    facing = "left"
                elif event.key == pygame.K_d:  # Move right
                    KEY_RIGHT = True
                    KEY_LEFT = False
                    facing = "right"
            if KEY_LEFT == False and KEY_RIGHT == False and KEY_D == False:
                facing = "idle"
                # Handle KEYUP events
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    KEY_LEFT = False
                elif event.key == pygame.K_s:
                    KEY_D = False
                elif event.key == pygame.K_d:
                    KEY_RIGHT = False

            char_x = max(0, min(char_x, width - char_width))
            char_y = max(0, min(char_y, height - char_height))

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if menuScreen:
                    if 125 <= mx <= 550 and 380 <= my <= 470:
                        menuScreen = False
                        gameScreen = True
                if shopScreen:
                    if 160 <= mx <= 535 and 260 <= my <= 420 and 2 <= score and score >= price and upgradepickaxe < 4:
                        upgradepickaxe += 1
                        score -= price
                        price += 10  # Increase price by 10 after purchasing the upgrade
                        char_speed += 0.25
                        if char_speed > max_speed:
                            char_speed = max_speed  # Make sure speed doesn't exceed max limit
                    if upgradepickaxe >= 4:
                        upgradepickaxe = 4
                    if 160 <= mx <= 535 and 460 <= my <= 620 and 2 <= score and score >= price2 and upgradetimer < 4:
                        upgradetimer += 1
                        score -= price2
                        price2 += 10  # Increase price by 10 after purchasing the upgrade
                        countdown_time += 20
                    if upgradetimer >= 4:
                        upgradetimer = 4
                    if 600 <= mx <= 700 and 230 <= my <= 485:
                        gameScreen = True
                        menuScreen = False
                        shopScreen = False
                        facing = "idle"
                        depth = 0
                        char_x = 350
                        char_y = 0

                        # Clear and regenerate the map using existing logic
                        full_map = []
                        for _ in range(50):
                            full_map.append(random.choices(listofblocks, weights=(100, 20), k=100))

                        # Reset the timer
                        global start_ticks
                        start_ticks = pygame.time.get_ticks()

        # Control the movement speed and ensure the player doesn't move too fast
        if KEY_LEFT:
            char_x -= char_speed
        if KEY_RIGHT:
            char_x += char_speed
        if KEY_D:
            char_y += char_speed

        if menuScreen:
            startScreen()
        if gameScreen:
            game()
            y = 120
            j = 0
            if char_y > 400: #Character movement + map boundaries
                depth += 400
                char_y = 0
            on_ground = False
            # Display the correct sprite based on the direction

            if facing == "right":
                screen.blit(imagesright[frame], (char_x, char_y))
            elif facing == "left":
                screen.blit(imagesleft[frame], (char_x, char_y))
            else:
                screen.blit(idle[frame], (char_x, char_y))

            for row in full_map:
                i = 0
                x = 0
                for block in row:
                    if (char_x + 25 >= x and char_x + 25 < x + 50 and
                            char_y + 25 + depth < y and char_y + 25 + depth > y - 50 and full_map[j][i] != 2):
                        char_y = y - 50 - depth
                        on_ground = True
                        if KEY_D:
                            if full_map[j][i] == 1:
                                score += 1
                            full_map[j][i] = 2
                            char_y += 1
                            on_ground = False
                        if KEY_LEFT:
                            if full_map[j - 1][i - 1] == 1:
                                score += 1
                            full_map[j - 1][i - 1] = 2
                            char_x -= 1
                            on_ground = True
                        if KEY_RIGHT:
                            if full_map[j - 1][i + 1] == 1:
                                score += 1
                            full_map[j - 1][i + 1] = 2
                            char_x += 1
                            on_ground = True
                    x += blocksize
                    i += 1
                y += blocksize
                j += 1
            if on_ground == False:
                char_y += 1
        elif shopScreen:
            shop()
        elif not gameScreen:
            # Ensure player does not show up on the win screen
            pass

        pygame.display.update()

        if menuScreen:
            startScreen()
        if gameScreen:
            game()
            y = 120
            j = 0
            if char_y > 400:
                depth += 400
                char_y = 0
            on_ground = False
            if facing == "right":
                screen.blit(imagesright[frame], (char_x, char_y))
            elif facing == "left":
                screen.blit(imagesleft[frame], (char_x, char_y))
            else:
                screen.blit(idle[frame], (char_x, char_y))

            for row in full_map:
                i = 0
                x = 0
                for block in row:
                    if (
                            char_x + 25 >= x and char_x + 25 < x + 50 and char_y + 25 + depth < y and char_y + 25 + depth > y - 50 and
                            full_map[j][i] != 2):
                        char_y = y - 50 - depth
                        on_ground = True
                        if KEY_D == True:
                            if full_map[j][i] == 1:
                                score += 1
                            full_map[j][i] = 2
                            char_y += 1
                            on_ground = False
                        if KEY_LEFT == True:
                            if full_map[j - 1][i - 1] == 1:
                                score += 1
                            full_map[j - 1][i - 1] = 2
                            char_x -= 1
                            on_ground = True
                        if KEY_RIGHT == True:
                            if full_map[j - 1][i + 1] == 1:
                                score += 1
                            full_map[j - 1][i + 1] = 2
                            char_x += 1
                            on_ground = True
                    x += blocksize
                    i += 1
                y += blocksize
                j += 1
            if on_ground == False:
                char_y += 1
        elif shopScreen:
            shop()
        elif not gameScreen:
            # Ensure player does not show up on the win screen
            pass

        pygame.display.update()


if __name__ == "__main__":
    main()
