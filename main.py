import pygame
import random
import math

# inicialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

running = True

# Titel and icon
pygame.display.set_caption("Space Inverse")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (800, 600))

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480

playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_count = 6
for i in range(enemy_count):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(32)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 0.9
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 40)

textX = 15
textY = 15

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 80)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))

    if distance < 27:
        return True
    else:
        return False


# game loop
while running:
    # RGB color
    screen.fill((0, 0, 0))
    # backgroud
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed chec whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_UP:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN:
                playerY_change = 0.5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # player
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 730:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # enemy
    for i in range(enemy_count):
        enemyX[i] += enemyX_change[i]

        if enemyY[i] > 450:
            for j in range(enemy_count):
                enemyY[j] = 2000
            game_over_text()
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 730)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision

    # RGB color
    # screen.fill((0, 0, 178))
    player(playerX, playerY)

    for i in range(enemy_count):
        enemy(enemyX[i], enemyY[i], i)
    show_score(textX, textY)

    # screen must update evry time
    pygame.display.update()
