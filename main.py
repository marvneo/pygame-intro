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
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
text_surface = test_font.render('Hello world', False, 'yellow')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,300))
    screen.blit(text_surface, (300,350))

    pygame.display.update()
    clock.tick(60)
