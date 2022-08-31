import pygame, random

#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
def bird_animation():
    new_bird = birds[animation]
    new_bird_rect = new_bird.get_rect(center = (80, bird_hb.centery))
    return new_bird, new_bird_rect
#звуки
pygame.mixer.music.load("c418-key.mp3")
pygame.mixer.music.play(-1)
point = pygame.mixer.Sound('sound/point.wav')
die = pygame.mixer.Sound('sound/die.wav')
hit = pygame.mixer.Sound('sound/hit.wav')
wing = pygame.mixer.Sound('sound/wing.wav')

pygame.display.set_caption('flappy bird')
window = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
bg = pygame.image.load('images/background.png')
base = pygame.image.load('images/base.png')

bird_mid = pygame.image.load('images/bluebird.png')
bird_up = pygame.image.load('images/bluebird-up.png')
bird_down = pygame.image.load('images/bluebird-down.png')
birds = [bird_mid, bird_up, bird_down]
animation = 0
bird = birds[animation]
bird_hb = bird.get_rect(center = (50,256))

pipe = pygame.image.load('images/pipe.png')
pipe_flip = pygame.transform.flip(pipe, False, True)
msg = pygame.image.load('images/message.png')
msg_hb = msg.get_rect(center = (144,256))
base_x = 0
gravity = 0.2
speed = 0
pipe_x = 300
pipe_y = 350
height = [280, 300, 350, 400]
game_active = False
score = 0
birdka = pygame.USEREVENT
pygame.time.set_timer(birdka, 80)

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            quit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE and game_active:
                speed = 0
                speed -= 5
                wing.play()
            
            if i.key == pygame.K_SPACE and game_active == False:
                game_active = True
                bird_hb.center = (50, 256)
                pipe_x = 300
                pipe_y = 350    
                speed = 0
                score = 0
        if i.type == birdka:
            if animation < 2:
                animation += 1
            else:
                animation = 0
  
    bird, bird_hb = bird_animation()

    bird_flip = pygame.transform.rotozoom(bird, -speed*4,1)
    window.blit(bg, (0,0))

    if game_active:
        #птичка
        window.blit(bird_flip, bird_hb)
        speed += gravity
        bird_hb.centery += speed
        #трубы (столкновение = смерть)
        pipe_hb = pipe.get_rect(midtop = (pipe_x, pipe_y))
        window.blit(pipe, pipe_hb)

        pipe_hb2 = pipe_flip.get_rect(midbottom = (pipe_x, pipe_y - 150))
        window.blit(pipe_flip, pipe_hb2)
        pipe_x -= 2
        if pipe_x <= -50:
            pipe_x = 300
            pipe_y = random.choice(height)

    

        #условия проигрыша
        if bird_hb.colliderect(pipe_hb) or bird_hb.colliderect(pipe_hb2):
            hit.play()
            game_active = False
        if bird_hb.top <= 0 or bird_hb.bottom >= 450:
            die.play()
            game_active = False
        base_x -= 1
        if base_x <= -20:
            base_x = 0

        if pipe_hb.centerx == 50:
            score += 1
            point.play()
    else:
        window.blit(msg, msg_hb) 
        
    font = pygame.font.Font('04B_19.TTF', 75)
    text = font.render(str(score), True, (250, 250, 250))
    window.blit(text, (130,30))
    #земля (соприкосновение = смерть)
    window.blit(base, (base_x,450))
    
    pygame.display.update()
    clock.tick(120)
    

