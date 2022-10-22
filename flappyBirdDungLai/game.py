from cProfile import run
import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
running = True
# GREEN = (0, 200, 0)
GREEN = '#AEBDCA'
clock = pygame.time.Clock()
ORANGE = 'orange'
WHITE = (255,255,255)
game_color = '#395144'
soil_color = '#FFD384'

TUBE_WIDTH = 50

tube1_x = 0 + 400
tube2_x = 200 + 400
tube3_x = 400 + 400

tube1_height = randint(150,400)
tube2_height = randint(150,400)
tube3_height = randint(150,400)

RED = 'red'
BIRD_WIDTH = 35
BIRD_HEIGHT = 35
bird_x = 50
bird_y = 400

bird_drop_velocity = 0
GRAVITY = 0.5

TUBE_GAP = 150 #khoảng cách giữa 2 ống trên và dưới luôn không đổi

TUBE_VELOCITY = 3

score = 0
font = pygame.font.SysFont('sans',40)

tube1_pass = False
tube2_pass = False
tube3_pass = False

pausing = False

bg_img = pygame.image.load('./bgnew.png')
bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))
bird_img = pygame.image.load('./bird.png')
bird_img = pygame.transform.scale(bird_img,(BIRD_WIDTH,BIRD_HEIGHT))

while running:
    clock.tick(60)  #60 FPS là 60 khung nhìn trên giây
    screen.fill(GREEN)
    screen.blit(bg_img, (0,0))

    #Draw tube
    tube1_rect = pygame.draw.rect(screen,ORANGE, (tube1_x,0,TUBE_WIDTH,tube1_height))  #4 giá trị vị trí trục x, vị trí trục y, chiều rộng và chiều cao
    tube2_rect = pygame.draw.rect(screen,ORANGE, (tube2_x,0,TUBE_WIDTH,tube2_height))
    tube3_rect = pygame.draw.rect(screen,ORANGE, (tube3_x,0,TUBE_WIDTH,tube3_height))

    #Draw tube inverse
    tube1_rect_inv = pygame.draw.rect(screen,ORANGE, (tube1_x,tube1_height+TUBE_GAP,TUBE_WIDTH,HEIGHT-tube1_height-TUBE_GAP))
    tube2_rect_inv = pygame.draw.rect(screen,ORANGE, (tube2_x,tube2_height+TUBE_GAP,TUBE_WIDTH,HEIGHT-tube2_height-TUBE_GAP))
    tube3_rect_inv = pygame.draw.rect(screen,ORANGE, (tube3_x,tube3_height+TUBE_GAP,TUBE_WIDTH,HEIGHT-tube3_height-TUBE_GAP))

    #move tube to the left 
    tube1_x -= TUBE_VELOCITY  #-3px
    tube2_x -= TUBE_VELOCITY
    tube3_x -= TUBE_VELOCITY

    #Draw soil 
    soil_rect = pygame.draw.rect(screen,soil_color,(0,550,400,50))

    #Draw bird
    # bird_rect = pygame.draw.rect(screen,RED,(bird_x,bird_y,BIRD_WIDTH,BIRD_HEIGHT))
    bird_rect = screen.blit(bird_img,(bird_x,bird_y))

    #Bird falls
    bird_y += bird_drop_velocity
    bird_drop_velocity += GRAVITY  #FPS có ảnh hưởng đến gravity vì 60khung nhìn trên giây nên mỗi khung nhìn thì gravity lại thay đổi

    #Generate new tubes
    if tube1_x < -TUBE_WIDTH:
        tube1_x = 550
        tube1_height = randint(150,400)
        tube1_pass = False
    if tube2_x < -TUBE_WIDTH:
        tube2_x = 550
        tube2_height = randint(150,400)
        tube2_pass = False
    if tube3_x < -TUBE_WIDTH:
        tube3_x = 550
        tube3_height = randint(150,400)
        tube3_pass = False

    score_txt = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_txt,(150,10))
    #update score
    if tube1_x + TUBE_WIDTH <= bird_x and tube1_pass == False:
        score += 1
        tube1_pass = True
    if tube2_x + TUBE_WIDTH <= bird_x and tube2_pass == False:
        score += 1
        tube2_pass = True
    if tube3_x + TUBE_WIDTH <= bird_x and tube3_pass == False:
        score += 1
        tube3_pass = True
    
    #check collision
    for tube in [tube1_rect,tube2_rect,tube3_rect,tube1_rect_inv,tube2_rect_inv,tube3_rect_inv, soil_rect]:
        if bird_rect.colliderect(tube):
            pausing = True
            TUBE_VELOCITY = 0
            bird_drop_velocity = 0
            game_over_txt = font.render("Game Over! Score: " + str(score), True, game_color)
            press_space_txt = font.render("Press Space to continue..." , True, game_color)
            screen.blit(game_over_txt, (50,250))
            screen.blit(press_space_txt, (15,300))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #reset
                if pausing == True:
                    bird_y = 400
                    TUBE_VELOCITY = 3
                    tube1_x = 400
                    tube2_x = 600
                    tube3_x = 800
                    score = 0
                    pausing = False
                bird_drop_velocity = 0
                bird_drop_velocity -= 10
    
    pygame.display.flip()

pygame.quit()