# -*- coding:gb18030 -*-
# Flappy Bird��ϷԴ����flappybird.py

import random
WIDTH = 138 * 4             # ���ڿ�ȣ������ű���ͼƬ��ɣ�
HEIGHT = 396                # ���ڸ߶�
GAP = 150                   # ����ˮ�ܼ��ȱ�ڴ�С
SPEED = 3                   # ���������ٶ�
GRAVITY = 0.2               # �������ٶ�
FLAP_VELOCITY = -5          # ����ʱ�ĳ�ʼ�ٶ�
anim_counter = 0            # С�񶯻�������
score = 0                   # ��Ϸ����
score_flag = False          # �÷ֱ��
started = False             # ��Ϸ��ʼ���
backgrounds = []            # ����ͼ���б�

# �������ű���ͼ���ɫ������ѭ��������Ϸ����
for i in range(5):
    backimage = Actor("flappybird_background", topleft=(i * 138, 0))
    backgrounds.append(backimage)

# ���������ɫ
ground = Actor("flappybird_ground", bottomleft=(0, HEIGHT))

# ��������ˮ�ܽ�ɫ
pipe_top = Actor("flappybird_top_pipe")
pipe_bottom = Actor("flappybird_bottom_pipe")

# ����С���ɫ
bird = Actor("flappybird1", (WIDTH // 2, HEIGHT // 2))
bird.dead = False        # ���С���Ƿ���
bird.vy = 0              # ����С��ֱ�ٶ�

# ����GUI��ɫ
gui_title = Actor("flappybird_title", (WIDTH // 2, 72))
gui_ready = Actor("flappybird_get_ready", (WIDTH // 2, 204 ))
gui_start = Actor("flappybird_start_button", (WIDTH // 2, 345))
gui_over = Actor("flappybird_game_over",(WIDTH // 2, HEIGHT // 2))


# ��Ϸ�߼�����
def update():
    if not started or bird.dead:
        return
    update_background()
    update_ground()
    update_pipes()
    fly()
    animation()
    check_collision()


# ������Ϸ��ɫ
def draw():
    screen.fill((255, 255, 255))
    for backimage in backgrounds:
        backimage.draw()
    if not started:
        gui_title.draw()
        gui_ready.draw()
        gui_start.draw()
        return
    pipe_top.draw()
    pipe_bottom.draw()
    ground.draw()
    bird.draw()
    screen.draw.text(str(score), topleft=(30, 30), fontsize=30)
    if bird.dead:
        gui_over.draw()


# ����������¼�
def on_mouse_down(pos):
    global started
    if bird.dead:
        return
    if started:
        bird.vy = FLAP_VELOCITY
        sounds.flap.play()
        return
    # �������ʼ��ť����ʼ����Ϸ
    if gui_start.collidepoint(pos):
        started = True
        reset_pipes()
        music.play("flappybird")


# ������Ϸ������ѭ����������ͼ��
def update_background():
    for backimage in backgrounds:
        backimage.x -= SPEED
        if backimage.right <= 0:
            backimage.left = WIDTH


# ���µ����ɫ
def update_ground():
    ground.x -= SPEED
    if ground.right < WIDTH:
        ground.left = 0


# ����ˮ�ܽ�ɫ
def update_pipes():
    pipe_top.x -= SPEED
    pipe_bottom.x -= SPEED
    if pipe_top.right < 0:
        reset_pipes()


# ������������ˮ�ܳ��ֵ�λ��
def reset_pipes():
    global score_flag
    score_flag = True
    # ��������Ϸ�ˮ�ܵĴ�ֱλ��
    pipe_top.bottom = random.randint(50, 150)
    # �����Ϸ�ˮ�ܵĴ�ֱλ���������·�ˮ�ܵĴ�ֱλ��
    pipe_bottom.top = pipe_top.bottom + GAP
    # ��������ˮ�ܵ�ˮƽλ��
    pipe_top.left = WIDTH
    pipe_bottom.left = WIDTH


# ����С�����
def fly():
    global score, score_flag
    # ��С��Խ��ˮ�ܣ��������һ
    if score_flag and bird.x > pipe_top.right:
        score += 1
        score_flag = False
    # ����С������
    bird.vy += GRAVITY
    bird.y += bird.vy
    # ��ֹС��ɳ������ϱ߽�
    if bird.top < 0:
        bird.top = 0


# ����С����еĶ���
def animation():
    global anim_counter
    anim_counter += 1
    if anim_counter == 2:
        bird.image = "flappybird1"
    elif anim_counter == 4:
        bird.image = "flappybird2"
    elif anim_counter == 6:
        bird.image = "flappybird3"
    elif anim_counter == 8:
        bird.image = "flappybird2"
        anim_counter = 0


# С����ˮ�ܺ͵������ײ���
def check_collision():
    if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom):
        sounds.collide.play()
        music.stop()
        bird.dead = True
    elif bird.colliderect(ground):
        sounds.fall.play()
        music.stop()
        bird.dead = True
