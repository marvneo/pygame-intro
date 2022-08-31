import pygame
from sys import exit
from random import randint

def display_score():

    curr_time = pygame.time.get_ticks() - start_time
    score = curr_time // 100
    score_surface = test_font.render('Score: '+ f'{score}', False, (64,64,64)).convert()
    score_rect = score_surface.get_rect(topleft = (30,30))
    screen.blit(score_surface, score_rect)

    return score

def enemy_movement(obstacle_list):

    new_obstacle_list = []

    if obstacle_list:
        for obstacle_rect in obstacle_list:


            if obstacle_rect.bottom == 300:
                obstacle_rect.x -= 4.5
                screen.blit(snail_surface, obstacle_rect)
            else:
                obstacle_rect.x -= 5
                screen.blit(fly_surface, obstacle_rect)

            if obstacle_rect.x > -100:
                new_obstacle_list.append(obstacle_rect)

        return new_obstacle_list

    else: return obstacle_list


def check_collision(player, obstacle_list):

    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player.colliderect(obstacle_rect): return True

    else: return False

def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump

    else:
        player_index += 0.1

        if player_index > 2:
            player_index = 0

        player_surface = player_walk[int(player_index)]

pygame.init()

screen_width, screen_length = 800,400
screen = pygame.display.set_mode((screen_width,screen_length))
pygame.display.set_caption('Snail Hunter')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

# font type
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
# intro screen
intro_text = test_font.render('SNAIL HUNTER', False, 'yellow').convert()
intro_text_rect = intro_text.get_rect(center = (400, 60))
instruction_text = test_font.render('Press spacebar to start jumping', False, 'yellow').convert()
instruction_text_rect = instruction_text.get_rect(center = (400, 350))
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400,200))
# creates surface
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
# enemies
snail_surface_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_surface_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frame = [snail_surface_1, snail_surface_2]
snail_frame_index = 0
snail_surface = snail_frame[snail_frame_index]

fly_surface_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_surface_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frame = [fly_surface_1, fly_surface_2]
fly_frame_index = 0
fly_surface = fly_frame[fly_frame_index]
obstacle_rect_list = []
# player
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0
# pause
pause = False
pause_time = 0
pause_text = test_font.render('PAUSED', False, 'yellow').convert()
pause_text_rect = intro_text.get_rect(center = (400, 200))
# game over
game_over = False
game_over_text = test_font.render('GAME OVER', False, 'red').convert()
game_over_rect = game_over_text.get_rect(center =(400,150))
game_over_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
game_over_stand = pygame.transform.scale(game_over_stand,(800,800))
game_over_stand_rect = game_over_stand.get_rect(center = (500,200))
# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1800)
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 300)
# runs game
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN: # jumping
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity -= 11

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300: # jumping
                    player_gravity -= 11
                elif event.key == pygame.K_ESCAPE:
                    pause_time = pygame.time.get_ticks()
                    pause = True
                    game_active = False

            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(800,1400),300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(800,1400), 180)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 1:
                    snail_frame_index = 0
                else:
                    snail_frame_index = 1
                snail_surface = snail_frame[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 1:
                    fly_frame_index = 0
                else:
                    fly_frame_index = 1
                fly_surface = fly_frame[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not pause:  # restarts game
                    game_active = True
                    game_over = False
                    start_time = pygame.time.get_ticks()
                    obstacle_rect_list.clear()

                else:
                    # need to figure out the right scored if game is paused
                    # start_time = pause_time
                    game_active = True
                    pause = False


    if game_active: # renders animation
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        # player logic
        player_gravity += .4
        player_rect.y += player_gravity
        # obstacle logic
        obstacle_rect_list = enemy_movement(obstacle_rect_list)

        if player_rect.bottom >= 300: # stops player from falling through ground
            player_rect.bottom = 300
            player_gravity = 0
        player_animation()
        screen.blit(player_surface, player_rect)

        if check_collision(player_rect, obstacle_rect_list):
             game_active = False
             game_over = True


    else:
        if game_over: # game over screen
            screen.blit(game_over_stand, game_over_stand_rect)
            screen.blit(game_over_text, game_over_rect)
            game_over_score_text = test_font.render('Your score is '+ f'{score}', False, 'red').convert()
            game_over_score_rect = game_over_score_text.get_rect(center =(400,200))
            screen.blit(game_over_score_text, game_over_score_rect)

        elif pause: # pause screen
            screen.blit(pause_text, pause_text_rect)

        else: # intro screen
            screen.fill((94, 129, 162))
            screen.blit(player_stand, player_stand_rect)
            screen.blit(intro_text, intro_text_rect)
            screen.blit(instruction_text, instruction_text_rect)



    pygame.display.update()
    clock.tick(60)
