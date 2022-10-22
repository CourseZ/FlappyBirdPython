import pygame, sys, random  #ctrl F5 hiện ra dòng Hello từ pygame

#tạo hàm cho trò chơi
def draw_floor():
    screen.blit(floor, (floor_x_pos, 570)) #thay đổi y thành 600, tọa độ (0, 540), di chuyển lùi
    screen.blit(floor, (floor_x_pos+424, 570)) #sàn thứ 2 cộng thêm 424 bằng với trục x của màn hình 
    #tức là sẽ kế tiếp luôn sàn thứ nhất

def create_pipe():
    #tạo rect object để tý nhận biết va chạm giữa chim và ống
    random_pipe_pos = random.choice(pipe_height) #tạo vị trí ngẫu nhiên của ống, random chọn ngẫu nhiên trong list
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos-670))  #vì sao phải trừ 650, thứ nhất khi random 
    #nó sẽ ra height, và height này xét theo chiều y: height>0 sẽ đẩy xuống dưới nên khi âm thì nó sẽ chạy lên trên cao hơn
    
    return bottom_pipe, top_pipe

def move_pipe(pipes): #di chuyển ống vì khi chim di chuyển thì ống cũng cần phải di chuyển, param là những ống (pipes)
    for pipe in pipes:
        pipe.centerx -= 5  #di chuyển x sang phải thì tăng x, sang trái thì giảm x
    return pipes   #trả lại list những cái ống mới

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 644: #nếu lớn hơn height của cửa sổ game thì là ống ở dưới
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            # False True là trục x và y nếu muốn lật theo trục nào thì để là true
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): #nếu cái rect của con chim va chạm với cái ống, colliderect có sẵn trong pygame để check các object rect
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 540:
        #top nhỏ hơn -75 tức là cho đi lên 75px và bottom cho đi xuống 540, khi chạm sàn báo va chạm,
        #vì đi lên là <0 đi xuống là >0 do gốc tọa độ nằm ở góc trên bên trái
        return False
    return True

def rotate_bird(flappyBird):
    new_bird = pygame.transform.rotozoom(flappyBird, -bird_movement*3, 1)  #-bird_movement để cho nó hướng xuống, nhân 3 cho hiệu ứng r
    #rotozoom để tạo hiệu ứng xoay cho con chim, có 3 tham số,
    #tham số 1 là đối tượng xoay, tham số 2 là xoay theo chiều nào, tham số 3 là scale hình ảnh
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))  #center y vì nó bay theo trục dọc
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render("Score: " + str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (212,70))
        screen.blit(score_surface,score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (212,70))
        screen.blit(score_surface,score_rect)  #điểm kết thúc

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (212,550))
        screen.blit(high_score_surface,high_score_rect)  #điểm cao

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init() #khởi tạo pygame

size = width, height = 424, 644 # 768 thì vượn quá độ phân giải màn hình r  size ban đầu 432 768
screen = pygame.display.set_mode(size)  #set chiều dài và rộng của màn hình hiển thị game
#asset chứa hình ảnh
#sound chứa âm thanh
# và 1 cái font gốc

#khi dùng convert() thì phải set_mode ở bên trên trước để tránh gây lỗi

clock = pygame.time.Clock()  #set FPS
game_font = pygame.font.Font('04B_19.ttf', 40)  #2 đối số là tên phông chữ và cỡ chữ 40px

#tạo các biến cho trò chơi
gravity = 0.20
bird_movement = 0 #vì lúc đầu con chim chưa di chuyển
game_active = True   #game hoạt động sẽ là true,game chấm dứt là false
score = 0 #lúc bắt đầu điểm bằng 0
high_score = 0

#chèn background
bg = pygame.image.load('assets/bgSizeFill.png').convert()  
#tải hình ảnh lên, convert giúp tải hình ảnh nhanh và nhẹ
bg = pygame.transform.scale2x(bg)  #x2 hình ảnh

#chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0  #set trục x là 0

#tạo chim
#tạo rect xung quanh con chim để nhận biết vùng chọn
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
# bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
#dùng rotozoom thg bị 1 nền màu đen nên cần convert_alpha để loại bỏ điều đó
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 322))

#tạo timer cho bird để đập cánh
birdflap = pygame.USEREVENT + 1  #vì sao lại cộng 1 vì bên dưới đã tạo 1 event người dùng r, và event này dành riêng cho chim
pygame.time.set_timer(birdflap, 200)

#tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
#cái ống sẽ xuất hiện trong 1 khoảng thời gian nhất định, nên ta tạo timer , spawn có nghĩa kiểu tạo thêm ra pipe
spawnpipe = pygame.USEREVENT  #tạo sự kiên người dùng, thêm event
pygame.time.set_timer(spawnpipe, 1400)  #đặt một mốc thời gian, sau 1200ms
pipe_height = [200, 300, 400]

#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (212,322))

#chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100  #vì cái điểm tăng là 0,01
while True:
    for event in pygame.event.get():  # vòng lặp sự kiện, lấy tất cả các sự kiện pygame diễn ra
        if event.type == pygame.QUIT:  #nếu sự kiện là người chơi ấn vào nút thoát ra ngoài
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: #sự kiện khi nhấn phím
            if event.key == pygame.K_SPACE and game_active:  #nhấn space
                bird_movement = 0   #khi nhấn thì nó về 0
                bird_movement = -7  #muốn đi lên thì giảm y
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                #game đã dừng và khi ấn tiếp thì sẽ chạy lại trò chơi
                game_active = True
                pipe_list.clear()  #khi reset lại phải xóa hết những ống và chim
                bird_rect.center = (100, 322)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()  #phải vẽ lại vì load 3 hình mới

    screen.blit(bg, (0, 0))   #thêm cái gì đó vào cửa sổ background  cách trục y phía bên trái là 0, cách trục x phía bên trên là 0
    
    if game_active:
        bird_movement += gravity  #chim di chuyển trọng lực càng tăng, tạo hiệu ứng trọng lực
        rotated_bird = rotate_bird(bird)  #xoay chim
        bird_rect.centery += bird_movement #di chuyển xuống dưới tăng y
        screen.blit(rotated_bird, bird_rect) #hiển thị chim

        game_active = check_collision(pipe_list)  #kiểm tra xem có va chạm không nếu va chạm game active sẽ bằng 
        #false và vòng lặp while true tiếp theo không chạy cái này nữa

        #ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game over')

    floor_x_pos -= 1
    draw_floor()
    #sàn thứ 2 chạy xong sẽ cho sàn thứ nhất lên trên đầu nên ta dùng câu lệnh if dưới
    if(floor_x_pos <= -424):  #nhỏ hơn hoặc bằng âm của chiều rộng màn hình, vì màn thứ 2 như hàm ở trên là +424
        floor_x_pos = 0 #reset về vị trí x ban đầu ở gốc tọa độ
    #nhưng nó sẽ lùi lại cho đến hết sàn
    #để giải quyết vấn đề này chúng ta sẽ cho 2 cái sàn chạy và thế lần lượt cho nhau

    pygame.display.update()  # để hiện lên màn hình
    clock.tick(120) # FPS = 120