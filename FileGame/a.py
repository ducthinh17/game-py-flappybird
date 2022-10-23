import pygame, sys, cv2, random

# DEF for game
def draw_floor ():
    screen.blit(floor,(floor_x_position,650))
    screen.blit(floor,(floor_x_position+432,650))
def create_pipe ():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_sureface.get_rect(midtop=(500,random_pipe_pos))
    top_pipe = pipe_sureface.get_rect(midtop=(500,random_pipe_pos -700))
    return bottom_pipe, top_pipe
def moving_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return pipes
def draw_pipe (pipes):
    for pipe in pipes:
        if pipe.bottom >=600:
            screen.blit(pipe_sureface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_sureface,False,True)        # Fale , True : (X, Y)     đảo ống
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= 75 or bird_rect.bottom >= 650:
        return False
    
    return True
def rotate_bird (bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'Main Game':
        score_sureface = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = score_sureface.get_rect(center = (218,100))
        screen.blit(score_sureface,score_rect)
    if game_state == 'Game Over':
        score_sureface = game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_sureface.get_rect(center = (218,100))
        screen.blit(score_sureface,score_rect)

        high_score_sureface = game_font.render(f'Highest point: {int(high_score)}', True,(255,255,255))
        high_score_rect = high_score_sureface.get_rect(center = (218,615))
        screen.blit(high_score_sureface,high_score_rect)
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100, size =-16, channels = 2, buffer =512)         # tối ưu file âm thanh (khớp space)
pygame.init()

screen =pygame.display.set_mode ((432,768))

clock = pygame.time.Clock()

game_font = pygame.font.Font('04B_19.ttf',40)

# to Create X

gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score =0 

# BACKGROUND + FLOOR
bg = pygame.image.load('/Users/thinhpld0/Desktop/Game_py/FileGame/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
floor =pygame.image.load('/Users/thinhpld0/Desktop/Game_py/FileGame/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_position = 0


# BIRD
bird_down = pygame.transform.scale2x(pygame.image.load('/Users/thinhpld0/Desktop/Game_py/FileGame/assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load ('/Users/thinhpld0/Desktop/Game_py/FileGame/assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load ( '/Users/thinhpld0/Desktop/Game_py/FileGame/assets/yellowbird-upflap.png').convert_alpha())
bird_list =[bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index] 


bird_rect = bird.get_rect(center= (100,384))

# Timer for Bird

birdflap = pygame.USEREVENT + 1     
pygame.time.set_timer(birdflap,200)


# Barrier

pipe_sureface =pygame.image.load('/Users/thinhpld0/Desktop/Game_py/FileGame/assets/pipe-green.png').convert()
pipe_sureface = pygame.transform.scale2x(pipe_sureface)
pipe_list = []

# Timer

spawnpipe =pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)
pipe_height =[222,333,288,300]

# Finishing senery:
game_over_surface = pygame.transform.scale2x(pygame.image.load ( '/Users/thinhpld0/Desktop/Game_py/FileGame/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center =(216,384))

# Sound
flap_sound = pygame.mixer.Sound('/Users/thinhpld0/Desktop/Game_py/FileGame/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('/Users/thinhpld0/Desktop/Game_py/FileGame/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('/Users/thinhpld0/Desktop/Game_py/FileGame/sound/sfx_point.wav')
score_sound_countdown =100

#while loop for game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 9
                flap_sound.play()
            if event.key ==pygame.K_SPACE and game_active ==False:
                game_active = True
                pipe_list.clear ()
                bird_rect.center = (100,384)
                bird_movement = 0
                score = 0

        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        
        if event.type == birdflap:
            if bird_index < 2 :
                birdflap += 1
            else:
                bird_index = 0
            bird,bird_rect = bird_animation()
        
        
    #bạckground        
    screen.blit(bg,(0,0))

    if game_active:

        #Bird
        bird_rect.centery += bird_movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)

        game_active = check_collision(pipe_list)
        screen.blit(rotated_bird,bird_rect)
        #pipe
        pipe_list = moving_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('Main Game' )
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown=100

    
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score )  
        score_display("Game Over")


        
    #floor
    floor_x_position -=1
    draw_floor()
    if floor_x_position <= -432:
        floor_x_position = 0

    pygame.display.update ()                    
    clock.tick(120)





