#%%

import pygame
import random
import math
import subprocess
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((1000, 800))

background = pygame.image.load('background.png')

mixer.music.load('HOME.mp3')
mixer.music.play()
# Title & Logo
pygame.display.set_caption("Alf's Epic Space Invaders")
icon = pygame.image.load('Icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 470  # Adjusted starting position for the new screen size
playerY = 700  # Adjusted starting position for the new screen size
playerX_change = 0
playerY_change = 0
player_lives = 3  # Initialize player lives

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 40
enemy_width = 100  # Adjusted enemy width for a single enemy
enemy_height = 100  # Adjusted enemy height for a single enemy

bottom_threshold = 800

# Initialize hit points and state for each enemy
enemy_hit_points = [6] * num_of_enemies
enemy_state = [True] * num_of_enemies

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(100, 935))  # Adjusted enemy spawn range for the new screen size
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 700  # Adjusted starting position for the new screen size
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"
bullet_width = 80  # Adjusted bullet width
bullet_height = 80  # Adjusted bullet height

bullet_rect = pygame.Rect(bulletX, bulletY, bullet_width, bullet_height)

# Score
score_value = 0
font = pygame.font.Font('RACING HARD.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value) + " / 240 enemies defeated", True, (255, 255, 255))
    lives_text = font.render("Lives: " + str(player_lives), True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(lives_text, (x, y + 40))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y): 
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def playerCollision(playerX, playerY, enemyX, enemyY):
    distance = math.sqrt((playerX - enemyX) ** 2 + (playerY - enemyY) ** 2)
    if distance < 27:  # Adjust the collision threshold as needed
        return True
    else:
        return False

def isCollision(enemyX, enemyY, bullet_rect):
    enemy_rect = pygame.Rect(enemyX, enemyY, enemy_width, enemy_height)  # Define enemy dimensions

    # Check for collision
    if bullet_rect.colliderect(enemy_rect):
        return True
    else:
        return False

# Function to update bullet hitbox
def update_bullet_rect():
    global bullet_rect
    bullet_rect = pygame.Rect(bulletX, bulletY, bullet_width, bullet_height)

# Game Loop
running = True
while running:

    screen.fill((0, 0, 128))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -2
            if event.key == pygame.K_d:
                playerX_change = 2
            if event.key == pygame.K_w:
                playerY_change = -2
            if event.key == pygame.K_s:
                playerY_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 935:  # Adjusted value for the new screen size
        playerX = 935

    if playerY <= 0:
        playerY = 0
    elif playerY >= 740:  # Adjusted value for the new screen size
        playerY = 740

    for i in range(num_of_enemies):
        if enemy_state[i]:
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 100:
                enemyX_change[i] = 6 # Change this value to a positive number
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 935:
                enemyX_change[i] = -6 # Change this value to a negative number
                enemyY[i] += enemyY_change[i]

            if enemyY[i] > bottom_threshold:
                enemyX[i] = random.randint(100, 935)
                enemyY[i] = random.randint(50, 150)

            # Check for player-enemy collision
            player_collision = playerCollision(playerX, playerY, enemyX[i], enemyY[i])
            if player_collision:
                player_lives -= 1
                print("Player lives:", player_lives)
                # Reset the enemy position after losing a life
                enemyX[i] = random.randint(100, 935)
                enemyY[i] = random.randint(50, 150)

                # End the game if the player has no lives left
                if player_lives == 0:
                    print("GAME OVER")
                    running = False

            # Collision with bullet
            collision = isCollision(enemyX[i], enemyY[i], bullet_rect)
            if collision:
                bulletY = 700  # Adjusted value for the new screen size
                bullet_state = "ready"
                score_value += 1
                print(score_value)
                enemy_hit_points[i] -= 1  # Decrement enemy hit points

                if enemy_hit_points[i] <= 0:
                    enemy_state[i] = False  # Set enemy state to False
                    print("Enemy", i, "defeated!")

                # Respawn enemy
                enemyX[i] = random.randint(100, 935)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

    # Update bullet hitbox
    update_bullet_rect()

    # Bullet movement
    if bulletY <= 0:
        bulletY = 700  # Adjusted value for the new screen size
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if score_value >= 240: 
        subprocess.Popen(["python", "SD_STAGE3.py"])
        running = False

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

pygame.quit()
          
# %%
