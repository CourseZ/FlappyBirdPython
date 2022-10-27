import pygame,sys
from random import randint

pygame.init()

WIDTH, HEIGHT = 400, 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('FLappy Bird')
clock = pygame.time.Clock()
WHITE = (255,255,255)
x_bird = 50
y_bird = 350

tube1_x = 0 + 400
tube2_x = 200 + 400
tube3_x = 400 + 400
TUBE_WIDTH = 50

tube1_height = randint(100,400)
tube2_height = randint(100,400)
tube3_height = randint(100,400)

TUBE_GAP = 150

bird_drop_velocity = 0
gravity = 0.5
tube_velocity = 3
score = 0
font = pygame.font.SysFont('san',40)
font1 = pygame.font.SysFont('san',40)

background_img = pygame.image.load('images/background.png')
background_img = pygame.transform.scale(background_img,(400,600))
bird_img = pygame.image.load('images/bird.png')
bird_img = pygame.transform.scale(bird_img,(35,35))
tube_img = pygame.image.load('./images/tube.png')
tube_inv_img = pygame.image.load('./images/tube_op.png')
# opposite : đối diện
sound = pygame.mixer.Sound('no6.wav')
sand_img = pygame.image.load('images/sand.png')
sand_img = pygame.transform.scale(sand_img,(400,30))

tube1_pass = False
tube2_pass = False
tube3_pass = False
running = True
pausing = False
while running:
    pygame.mixer.Sound.play(sound)
    clock.tick(60)
    screen.fill(WHITE)
    screen.blit(background_img,(0,0))
    #ép ảnh ống và vẽ ống
    tube1_img = pygame.transform.scale(tube_img,(TUBE_WIDTH,tube1_height))
    tube1 = screen.blit(tube1_img,(tube1_x,0))
    tube2_img = pygame.transform.scale(tube_img,(TUBE_WIDTH,tube2_height))
    tube2 = screen.blit(tube2_img,(tube2_x,0))
    tube3_img = pygame.transform.scale(tube_img,(TUBE_WIDTH,tube3_height))
    tube3 = screen.blit(tube3_img,(tube3_x,0))

    #ép ảnh ống và vẽ ống đối diện
    tube1_op_img = pygame.transform.scale(tube_inv_img,(TUBE_WIDTH,HEIGHT-tube1_height-TUBE_GAP))
    tube1_inv = screen.blit(tube1_op_img,(tube1_x,tube1_height+TUBE_GAP))
    tube2_op_img = pygame.transform.scale(tube_inv_img,(TUBE_WIDTH,HEIGHT-tube2_height-TUBE_GAP))
    tube2_inv = screen.blit(tube2_op_img,(tube2_x,tube2_height+TUBE_GAP))
    tube3_op_img = pygame.transform.scale(tube_inv_img,(TUBE_WIDTH,HEIGHT-tube3_height-TUBE_GAP))
    tube3_inv = screen.blit(tube3_op_img,(tube3_x,tube3_height+TUBE_GAP))
    
    #ống di chuyển sang trái
    tube1_x -= tube_velocity
    tube2_x -= tube_velocity
    tube3_x -= tube_velocity

    #tạo ống mới
    if tube1_x < -TUBE_WIDTH:
        tube1_x = 550
        tube1_height = randint(100,400)
        tube1_pass = False
    if tube2_x < -TUBE_WIDTH:
        tube2_x = 550
        tube2_height = randint(100,400)
        tube2_pass = False
    if tube3_x < -TUBE_WIDTH:
        tube3_x = 550
        tube3_height = randint(100,400)
        tube3_pass = False

    #vẽ cát
    sand = screen.blit(sand_img,(0,570))
    #vẽ chim và chim rơi
    bird = screen.blit(bird_img,(x_bird,y_bird))
    y_bird = y_bird + bird_drop_velocity
    bird_drop_velocity += gravity
    
    #ghi điểm
    score_txt = font.render("Score: " + str(score),True,WHITE)
    screen.blit(score_txt,(150,5))

    #cộng điểm  
    if tube1_x+TUBE_WIDTH <= x_bird and tube1_pass == False:
        score += 1
        tube1_pass = True
    if tube2_x+TUBE_WIDTH <= x_bird and tube2_pass == False:
        score += 1
        tube2_pass = True
    if tube3_x+TUBE_WIDTH <= x_bird and tube3_pass == False:
        score += 1
        tube3_pass = True

    #kiểm tra sự va chạm
    tubes = [tube1,tube2,tube3,tube1_inv,tube2_inv,tube3_inv,sand]
    for tube in tubes:
        if bird.colliderect(tube): 
            pygame.mixer.pause()
            tube_velocity = 0
            bird_drop_velocity = 0 
            pausing = True
            gane_over_txt = font.render("Game over! Score: " + str(score),True,WHITE)
            screen.blit(gane_over_txt,(65,200))
            space_txt = font.render("Press Space to continue...",True,WHITE)
            screen.blit(space_txt,(30,300))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type ==  pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_drop_velocity = 0
                bird_drop_velocity -= 7
                if pausing == True:
                    pygame.mixer.unpause()
                    x_bird = 50
                    y_bird = 350
                    tube1_x = 400
                    tube2_x = 600
                    tube3_x = 800
                    tube_velocity = 3
                    score = 0
                    pausing = False 
    pygame.display.flip()

#cho cánh chuyển động
#điểm bao nhiêu cho màn ban đêm
#high score