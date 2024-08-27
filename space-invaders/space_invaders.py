import pygame
import random

from objects import *
from level import Level

pygame.init()

screen_width = 800
screen_height = 600
buffer = 50
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# images
img_map = {
    'player': pygame.image.load('data/player.png'),
    'green': pygame.image.load('data/green.png'),
    'yellow': pygame.image.load('data/yellow.png'),
    'red': pygame.image.load('data/red.png'),
    'extra': pygame.image.load('data/extra.png')
}

# fonts
font = pygame.font.Font('freesansbold.ttf', 20)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
restart_font = pygame.font.Font('freesansbold.ttf', 35)

# colors
color_white = (255, 255, 255)
color_black = (0, 0, 0)

player = Player(img_map['player'], 370, 550)
player_change = 0
score = 0
score_x = 10
score_y = 10
max_level = 3

cooldown_remaining = 0
enemy_cooldown_remaining = 0

enemies = []
bullets = []

restart_box = {
               'x': 300,
               'y': 350,
               'width': 200,
               'height': 50
               }

top_bar_height = 35

def is_collision(object, bullet):
    if bullet.type != object.type:
        if bullet.x > object.x and bullet.x < object.x + object.width:
            if bullet.y > object.y and bullet.y < object.y + object.height:
                return True

def game_over(is_win):
    if is_win:
        display_text = game_over_font.render("YOU WIN", True, (255, 255, 255))
        screen.blit(display_text, (255, 250))
    else:
        display_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(display_text, (190, 250))
            
    pygame.draw.rect(screen, color_white, [restart_box['x'], restart_box['y'], restart_box['width'], restart_box['height']])
    restart_text = restart_font.render("RESTART", True, (0, 0, 0))
    screen.blit(restart_text, (320, 360))

# game loop
running = True
current_level = 1
load_level = True
level = None
is_game_over = False

while running:
    
    if load_level:
        if current_level < max_level:
            level = Level(current_level, screen_width, buffer)
            enemies = level.enemies
            for enemy in enemies:
                enemy.img = img_map[enemy.color]
            load_level = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = -2
            if event.key == pygame.K_RIGHT:
                player_change = 2
            if event.key == pygame.K_SPACE and cooldown_remaining == 0:
                bullets.append(Bullet('player', player.x+player_width/2, player.y))
                cooldown_remaining = player.cooldown
        
        if event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            player_change = 0 
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if mouseX > restart_box['x'] and mouseX < restart_box['x']+restart_box['width']:
                if mouseY > restart_box['height'] and mouseY < restart_box['y']+restart_box['height']:
                    current_level = 0
                    score = 0
    
    # update player
    player.update_position(player_change, 0)
    if player.x < 20 or player.x > 720:
        player.update_position(-player_change, 0)
        
    # update bullets
    for bullet in bullets:
        bullet.update_position(0, bullet.speed)
        
    # update enemies
    level.move_enemies()
    
    # enemies attack
    if enemy_cooldown_remaining == 0 and len(enemies) != 0:
        rand_enemy = random.choice(enemies)
        bullets.append(Bullet('enemy', rand_enemy.x+rand_enemy.width/2, rand_enemy.y+rand_enemy.height))
        enemy_cooldown_remaining = rand_enemy.cooldown
    
    # check for collisions
    for bullet in bullets:
        if bullet.type != player.type:
            if is_collision(player, bullet):
                player.lives -= 1
                bullets.remove(bullet)
        else:
            for enemy in enemies:
                if is_collision(enemy, bullet):
                    score += enemy.points
                    bullets.remove(bullet)
                    enemies.remove(enemy)
        
    # check for game over
    if current_level == max_level:
        game_over(True)
        is_game_over = True
    for enemy in enemies:
        if enemy.y + enemy_height > player.y:
            game_over(False)
            is_game_over = True
    if player.lives == 0:
        game_over(False)
        is_game_over = True
    
    # trigger load next level
    if len(enemies) == 0:
        current_level += 1
        load_level = True
        
    if cooldown_remaining > 0:
        cooldown_remaining -= 1
    if enemy_cooldown_remaining > 0:
        enemy_cooldown_remaining -= 1
    
    # fill screen
    screen.fill((0,0,0))
    screen.blit(img_map['player'], (player.x, player.y))
    
    for bullet in bullets:
        pygame.draw.line(screen, color_white, (bullet.x, bullet.y), (bullet.x, bullet.y+bullet.height), width=bullet.width)
        if bullet.y < 0 or bullet.y >= screen_height:
            bullets.remove(bullet)
    
    for enemy in enemies:
        screen.blit(enemy.img, (enemy.x, enemy.y))

    pygame.draw.rect(screen, color_black, [0, 0, screen_width, top_bar_height])
    score_display = font.render("SCORE: "+ str(score), True, color_white)
    screen.blit(score_display, (score_x, score_y))
    for i in range(player.lives):
        screen.blit(img_map['extra'], (screen_width-(i+1)*player_width, 5))
    
    clock.tick(60)
    pygame.display.update()
    