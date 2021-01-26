print("Falling Blocks Game by Piotr")

import pygame, sys, random

# Global variables
screen_width = 800
screen_height = 600
background_color = (128, 128, 128) # RGB grey
game_over = False
score = 0

#Speed control
clock = pygame.time.Clock()
speed = 10

# Player
player_color = (255, 0, 0) # RGB red
player_size = (50, 50)
player_position = [screen_width/2, screen_height - 2*player_size[1]]

# Enemies
enemy_color = (0, 0, 255) #Blue
enemy_size = (50, 50)
enemy_position = [random.randrange(0,screen_width-enemy_size[0], enemy_size[0]), 0]

enemy_list = [enemy_position]

def drop_enemies(enemy_list):

    delay = random.random()

    if len(enemy_list) < 50 and delay < 0.1:
        x_pos = random.randrange(0, screen_width - enemy_size[0], enemy_size[0])
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_position in enemy_list:
        pygame.draw.rect(screen, enemy_color, (enemy_position[0], enemy_position[1], enemy_size[0], enemy_size[1]))

def update_enemies(enemy_list, score):
    for index, enemy_position in enumerate(enemy_list):
        if enemy_position[1] >= 0 and enemy_position[1] < screen_height:
            enemy_position[1] += speed
        else:
            enemy_list.pop(index)
            score += 1
    return score

def collision_check(enemy_list, player_position):
    for enemy_position in enemy_list:
        if detect_collision(player_position, enemy_position):
            return True
    return False

def set_level(score):

    if score < 20:
        speed = 10
    elif score < 40:
        speed = 12
    elif score < 60:
        speed = 14
    elif score < 80:
        speed = 16
    elif score < 100:
        speed = 18
    elif score < 120:
        speed = 20
    elif score < 140:
        speed = 22
    elif score < 160:
        speed = 24
    elif score < 180:
        speed = 26
    elif score < 200:
        speed = 28
    else:
        speed = 30

    return (speed)

pygame.init()

# Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Falling Blocks Game by Piotr')

# Collisions between blocks
def detect_collision(player_position, enemy_position):

    p_x = player_position[0]
    p_y = player_position[1]

    e_x = enemy_position[0]
    e_y = enemy_position[1]

    if (p_x + player_size[0] > e_x >= p_x) or (e_x+enemy_size[0] > p_x >= e_x):
        if (p_y + player_size[1] > e_y >= p_y) or (e_y+enemy_size[1] > p_y >= e_y):
            print("Collision")
            return True
    else:
        #print("No collision")
        return False

# Main game loop
while not game_over:

    # Event loop
    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:
            pygame.quit() # deactivates pygame library, must be before sys.exit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # Escape key
            if event.key == pygame.K_ESCAPE:
                print("Escape key pressed down.")
                pygame.quit()
                sys.exit()

            x = player_position[0]
            y = player_position[1]

            if event.key == pygame.K_LEFT:
                x -= player_size[0]

            elif event.key == pygame.K_RIGHT:
                x += player_size[0]

            elif event.key == pygame.K_UP:
                y -= player_size[0]

            elif event.key == pygame.K_DOWN:
                y += player_size[0]

            player_position = [x, y]

    screen.fill(background_color)

    drop_enemies(enemy_list)
    score = update_enemies(enemy_list, score)

    speed = set_level(score)

    # Print score and speed in game window
    myfont = pygame.font.SysFont("monospace", 30)
    scoretext = myfont.render("Score: {0}".format(score), 1, (255, 0, 0))
    speedtext = myfont.render("Speed: {0}".format(speed), 1, (255, 255, 0))
    screen.blit(scoretext, (5, 5))
    screen.blit(speedtext, (5, 50))

    if collision_check(enemy_list, player_position):
        game_over = True
        print(f"Your score: {score}.")
        break

    draw_enemies(enemy_list)

    pygame.draw.rect(screen, player_color, (player_position[0], player_position[1], player_size[0], player_size[1]))

    # Speed control as FPS
    clock.tick(30)

    pygame.display.update()
