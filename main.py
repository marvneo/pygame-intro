import pygame
from sys import exit

pygame.init()

# creates display surface
screen_width, screen_length = 800,400
screen = pygame.display.set_mode((screen_width,screen_length))

# adds title
pygame.display.set_caption('Python Game')

# necessary for frame rate control
clock = pygame.time.Clock()

game_active = True

# font type
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# creates surface
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
# scoreboard
score_surface = test_font.render('Score:', False, (64,64,64)).convert()
score_rect = score_surface.get_rect(center = (80,30))
# snail
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_pos = 800
snail_rect = snail_surface.get_rect(midbottom = (snail_pos,300))
snail_accel = 3
# player
player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0
# game over
game_over_text = test_font.render('GAME OVER', False, 'red').convert()
game_over_rect = game_over_text.get_rect(center =(400,200))

# runs game
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # jumping
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                player_gravity -= 11
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                player_gravity -= 11

        if not game_active:
            # restarts game
            if event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 900

    if game_active:
        # renders animation
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        pygame.draw.rect(screen, '#c0e8ec', score_rect)
        pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        screen.blit(score_surface, score_rect)
        # snail movement
        snail_rect.left -= snail_accel
        # loops snail when it leaves the screen
        if snail_rect.right < -100:
            snail_rect.left = 900
        screen.blit(snail_surface, snail_rect)
        # player movements
        player_gravity += .4
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
            player_gravity = 0
        screen.blit(player_surface, player_rect)

        # handles collisions
        if snail_rect.colliderect(player_rect):
            game_active = False

    else:
        screen.blit(game_over_text, game_over_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()



    pygame.display.update()
    clock.tick(60)
