import pygame
from sys import exit

def display_score():
    curr_time = pygame.time.get_ticks() - start_time
    score = curr_time // 100
    score_surface = test_font.render('Score: '+ f'{score}', False, (64,64,64)).convert()
    score_rect = score_surface.get_rect(topleft = (30,30))
    screen.blit(score_surface, score_rect)

    return score

pygame.init()

# creates display surface
screen_width, screen_length = 800,400
screen = pygame.display.set_mode((screen_width,screen_length))
# adds title
pygame.display.set_caption('Python Game')
# necessary for frame rate control
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
game_over = False
# font type
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
# intro screen
intro_text = test_font.render('SNAIL HUNTER', False, 'yellow').convert()
intro_text_rect = intro_text.get_rect(center = (400, 40))
instruction_text = test_font.render('Press spacebar to start jumping', False, 'yellow').convert()
instruction_text_rect = instruction_text.get_rect(center = (400, 350))
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand,(250,250))
player_stand_rect = player_stand.get_rect(center = (400,200))
# creates surface
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
# snail
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_pos = 800
snail_rect = snail_surface.get_rect(midbottom = (snail_pos,300))
snail_accel = 4
# player
player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0
# game over
game_over_text = test_font.render('GAME OVER', False, 'red').convert()

game_over_rect = game_over_text.get_rect(center =(400,150))



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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                game_over = False
                start_time = pygame.time.get_ticks()
                snail_rect.left = 900

    if game_active:
        # renders animation
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
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
            game_over = True


    else:
        if game_over:
            screen.blit(game_over_text, game_over_rect)
            game_over_score_text = test_font.render('Your score is '+ f'{score}', False, 'red').convert()
            game_over_score_rect = game_over_score_text.get_rect(center =(400,200))
            screen.blit(game_over_score_text, game_over_score_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        else:
            screen.fill((94, 129, 162))
            screen.blit(player_stand, player_stand_rect)
            screen.blit(intro_text, intro_text_rect)
            screen.blit(instruction_text, instruction_text_rect)



    pygame.display.update()
    clock.tick(60)
