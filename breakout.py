# -*- coding:gb18030 -*-
# ��ש����ϷԴ����breakout.py

import random
WIDTH = 640        # ��Ļ���
HEIGHT = 400       # ��Ļ�߶�
BRICK_W = 80       # ש����
BRICK_H = 20       # ש��߶�
started = False    # С������
win = False        # ��Ϸʤ�����
lost = False       # ��Ϸʧ�ܱ��
lives = 5          # ����ֵ
score = 0          # ��Ϸ����

# ��������
pad = Actor("breakout_paddle", (WIDTH // 2, HEIGHT - 30))
pad.speed = 5      # �����ƶ��ٶ�

# ����С��
ball = Actor("breakout_ball", (WIDTH // 2, HEIGHT - 47))

# ����ש���б�
bricks = []
for i in range(5):
    for j in range(WIDTH // BRICK_W):
        brick = Actor("breakout_brick")
        brick.left = j * BRICK_W
        brick.top = 30 + i * BRICK_H
        bricks.append(brick)


# ������Ϸ�߼�
def update():
    if win or lost:
        return
    pad_move()
    ball_move()
    collision_ball_bricks()
    collision_ball_pad()
    check_gameover()


# ������Ϸͼ��
def draw():
    screen.fill((255, 255, 255))
    draw_text()
    ball.draw()
    pad.draw()
    for brick in bricks:
        brick.draw()


# �ƶ�����
def pad_move():
    # �ü��̿��Ƶ����ƶ�
    if keyboard.right:
        pad.x += pad.speed
    elif keyboard.left:
        pad.x -= pad.speed
    # �����������ڴ��ڷ�Χ��
    if pad.left < 0:
        pad.left = 0
    elif pad.right > WIDTH :
        pad.right = WIDTH


# �ƶ�С��
def ball_move():
    global started, lives
    # ����Ƿ���С��
    if not started:
        if keyboard.space:
            dir = 1 if random.randint(0, 1) else -1
            ball.vx = 3 * dir
            ball.vy = -3
            started = True
        else:
            ball.x = pad.x
            ball.bottom = pad.top
            return
    # ����С������
    ball.x += ball.vx
    ball.y += ball.vy
    # ��⼰����С���봰�����ܵ���ײ
    if ball.left < 0:
        ball.vx = abs(ball.vx)
    elif ball.right > WIDTH:
        ball.vx = -abs(ball.vx)
    if ball.top < 0:
        ball.vy = abs(ball.vy)
    elif ball.top > HEIGHT:
        started = False
        lives -= 1
        sounds.miss.play()


# ��Ⲣ����С����ש�����ײ
def collision_ball_bricks():
    global score
    # ���С���Ƿ�����ש�飬��û���򷵻�
    n = ball.collidelist(bricks)
    if n == -1:
        return
    # �Ƴ������ķ���
    brick = bricks[n]
    bricks.remove(brick)
    # ������Ϸ����
    score += 100
    sounds.collide.play()
    # ����С�򷴵�����
    if  brick.left < ball.x < brick.right:     # ����ש���в��ķ���
        ball.vy *= -1
    elif ball.x <= brick.left:                 # ����ש���󲿵ķ���
        if ball.vx > 0:
            ball.vx *= -1
        else:
            ball.vy *= -1
    elif ball.x >= brick.right:                # ����ש���Ҳ��ķ���
        if ball.vx < 0:
            ball.vx *= -1
        else:
            ball.vy *= -1


# ��Ⲣ����С���뵲�����ײ
def collision_ball_pad():
    # ���С���Ƿ��������壬��û���򷵻�
    if not ball.colliderect(pad):
        return
    # ��ֱ���򷴵�
    if ball.y < pad.y:
        ball.vy = -abs(ball.vy)
        sounds.bounce.play()
    # ˮƽ���򷴵�
    if ball.x < pad.x:
        ball.vx = -abs(ball.vx)
    else:
        ball.vx = abs(ball.vx)


# �����Ϸ�Ƿ����
def check_gameover():
    global win, lost
    # �ж���Ϸ�Ƿ�ʤ��
    if len(bricks) == 0:
        sounds.win.play()
        win = True
    # �ж���Ϸ�Ƿ�ʧ��
    if lives <= 0:
        sounds.fail.play()
        lost = True


# ����������Ϣ
def draw_text():
    screen.draw.text("Live: " + str(lives) + "   Score: " + str(score),
                     bottomleft=(5, HEIGHT - 5), color="black")
    if win:
        screen.draw.text("You Win!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=50, color="red")
    elif lost:
        screen.draw.text("You Lost!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=50, color="red")