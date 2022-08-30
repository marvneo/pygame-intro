import pygame
from sys import exit

pygame.init()

# creates display surface
screen_width, screen_length = 800,450
screen = pygame.display.set_mode((screen_width,screen_length))

pygame.display.set_caption('Python Game')

clock = pygame.time.Clock()

# creates surface
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,screen_length-168))

    pygame.display.update()
    clock.tick(60)
