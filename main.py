import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.05)

        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,300))
        self.gravity = 0



    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity -= 12

    def apply_gravity(self):
        if self.rect.bottom >= 301:
            self.rect.bottom = 300
            self.gravity = 0
        else:
            self.gravity += .5
        self.rect.y += self.gravity

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump

        else:
            self.player_index += 0.1
            if self.player_index > 2:
                self.player_index = 0

            self.image = self.player_walk[int(self.player_index)]

    def update(self):

        self.apply_gravity()
        self.player_input()
        self.animate()

class Enemy(pygame.sprite.Sprite):

    def __init__(self,type):

        super().__init__()
        if type == "snail":
            snail_surface_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_surface_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frame = [snail_surface_1, snail_surface_2]
            y_pos = 300

        elif type == "fly":
            fly_surface_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_surface_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frame = [fly_surface_1, fly_surface_2]
            y_pos = 180

        self.frame_index = 0
        self.image = self.frame[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom = (randint(800,1400),y_pos))

    def animate(self):
        self.frame_index += 0.3
        if self.frame_index > 2:
            self.frame_index = 0

        self.image = self.frame[int(self.frame_index)]

    def movement(self):
        self.rect.x -= 4

    def exterminate(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animate()
        self.movement()
        self.exterminate()

def display_score():

    curr_time = pygame.time.get_ticks() - start_time
    score = curr_time // 100
    score_surface = test_font.render('Score: '+ f'{score}', False, (64,64,64)).convert()
    score_rect = score_surface.get_rect(topleft = (30,30))
    screen.blit(score_surface, score_rect)

    return score

def check_collision():

    if pygame.sprite.spritecollide(player.sprite,enemy_group,False):
        enemy_group.empty()
        return True
    else:
        return False


pygame.init()

screen_width, screen_length = 800,400
screen = pygame.display.set_mode((screen_width,screen_length))
pygame.display.set_caption('Snail Hunter')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.05)
bg_music.play()

player = pygame.sprite.GroupSingle()
player.add(Player())

enemy_group = pygame.sprite.Group()

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_time = pygame.time.get_ticks()
                    pause = True
                    game_active = False
            if event.type == obstacle_timer:
                if randint(0,3) > 2:
                    enemy_group.add(Enemy('fly'))
                else:
                    enemy_group.add(Enemy('snail'))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not pause:  # restarts game
                    game_active = True
                    game_over = False
                    start_time = pygame.time.get_ticks()
                else:
                    game_active = True
                    pause = False

    if game_active: # renders animation
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        player.draw(screen)
        player.update()
        enemy_group.draw(screen)
        enemy_group.update()

        if check_collision():
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
