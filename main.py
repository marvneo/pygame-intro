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
text_surface = test_font.render('Hello world', False, 'yellow').convert()

# snail
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_pos = 850
snail_accel = 1

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(topleft = (80,200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface, (300,350))
    screen.blit(snail_surface, (snail_pos,260))
    snail_pos -= snail_accel

    # loops snail when it leaves the screen
    if -150 > snail_pos:
        snail_pos = 850

    # player
    screen.blit(player_surface, player_rect)


    pygame.display.update()
    clock.tick(60)
