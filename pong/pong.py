import pygame

from game import *

pygame.init()
clock = pygame.time.Clock()

game = Game()
keys_down = []
running = True
    
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and 'W' not in keys_down:
                keys_down.append('W')
            elif event.key == pygame.K_s and 'S' not in keys_down:
                keys_down.append('S')
            elif event.key == pygame.K_UP and 'UP' not in keys_down:
                keys_down.append('UP')
            elif event.key == pygame.K_DOWN and 'DOWN' not in keys_down:
                keys_down.append('DOWN')
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys_down.remove('W')
            elif event.key == pygame.K_s:
                keys_down.remove('S')
            elif event.key == pygame.K_UP:
                keys_down.remove('UP')
            elif event.key == pygame.K_DOWN:
                keys_down.remove('DOWN')
    
    game.update_paddles(keys_down)
    game.update_ball()
    
    if game.is_score():
        game.reset()
        
    game.draw_screen()
    
    clock.tick(60)
    pygame.display.update()

    