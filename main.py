import pygame
from sys import exit

pygame.init()

# creates display surface
screen = pygame.display.set_mode((1920,1080))

pygame.display.set_caption('Python Game')

clock = pygame.time.Clock()

# creates surface
test_surface = pygame.Surface((300,500))
test_surface.fill('white')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(test_surface,(200,100))

    pygame.display.update()
    clock.tick(60)
