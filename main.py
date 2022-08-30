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

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# creates surface
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# texts
text_surface = test_font.render('Hello world', False, 'yellow').convert()
score_surface = test_font.render('Score:', False, 'yellow').convert()
score_rect = score_surface.get_rect(center = (400,100))

# snail
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_pos = 800
snail_rect = snail_surface.get_rect(midbottom = (snail_pos,300))
snail_accel = 1.5

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEMOTION and player_rect.collidepoint(event.pos):
            print('collision')

    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface, (300,350))
    screen.blit(score_surface, score_rect)

    # snail movement
    screen.blit(snail_surface, snail_rect)
    snail_rect.left -= snail_accel

    # loops snail when it leaves the screen
    if snail_rect.right < -200:
        snail_rect.left = 800

    # player
    screen.blit(player_surface, player_rect)

    # collisions
    #if player_rect.colliderect(snail_rect):



    pygame.display.update()
    clock.tick(60)
