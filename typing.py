# -*- coding:gb18030 -*-
# ������ϷԴ����typing.py

import random, time
WIDTH = 640                       # ��Ļ���
HEIGHT = 400                      # ��Ļ�߶�
MAX_NUM = 5                       # ������������������
balloons = []                     # �����б�
balloon_queue = []                # ���е��������
win = False                       # ��Ϸʤ�����
lost = False                      # ��Ϸʧ�ܱ��
score = 0                         # ��Ϸ����
start_time = time.perf_counter()  # ��ʼʱ��
left_time = 60                    # ����ʱ


# ������Ϸ�߼�
def update():
    if win or lost:
        return
    if len(balloons) < MAX_NUM:
        add_balloon()
    update_balloon()
    check_gameover()
    count_time()


# ������Ϸͼ��
def draw():
    screen.fill((255, 255, 255))
    draw_text()
    for balloon in balloons:
        balloon.draw()
        # ���������ϵ���ĸ����������ʾ��ɫ������Ϊ��ɫ
        if balloon.typed:
            screen.draw.text(balloon.char,center=balloon.center,color="white")
        else:
            screen.draw.text(balloon.char,center=balloon.center,color="black")


# ������̰����¼�
def on_key_down(key):
    if win or lost:
        return
    global score
    # ��ⰴ���Ƿ��������ַ����Ӧ
    for balloon in balloons:
        if balloon.y > 0 and str(key) == "keys." + balloon.char:
            score += 1
            balloon.typed = True
            balloon_queue.append(balloon)
            # �ӳ���������
            clock.schedule(remove_balloon, 0.3)
            break


# �Ӵ�����ɾ������
def remove_balloon():
    sounds.eat.play()
    balloon = balloon_queue.pop(0)
    if balloon in balloons:
        balloons.remove(balloon)


# �򴰿����������
def add_balloon():
    balloon = Actor("typing_balloon", (WIDTH // 2, HEIGHT))
    balloon.x = random_location()
    balloon.vy = random_velocity()
    balloon.char = random_char()
    balloon.typed = False
    balloons.append(balloon)


# �����������ĳ�ʼλ��
def random_location():
    min_dx = 0
    while min_dx < 50:
        min_dx = WIDTH
        x = random.randint(20, WIDTH - 20)
        for balloon in balloons:
            dx = abs(balloon.x - x)
            min_dx = min(min_dx, dx)
    return x


# �������������ƶ��ٶ�
def random_velocity():
    n = random.randint(1, 100)
    if n <= 5:
        velocity = -5
    elif n <= 25:
        velocity = -4
    elif n <= 75:
        velocity = -3
    elif n <= 95:
        velocity = -2
    else:
        velocity = -1
    return velocity


# ������������ϵ���ĸ
def random_char():
    charset = set()
    for balloon in balloons:
        charset.add(balloon.char)
    ch = chr(random.randint(65, 90))
    while ch in charset:
        ch = chr(random.randint(65, 90))
    return ch


# ���������λ��
def update_balloon():
    for balloon in balloons:
        balloon.y += balloon.vy
        if balloon.bottom < 0:
            balloons.remove(balloon)


# ��Ϸ����ʱ
def count_time():
    global left_time
    play_time = int(time.perf_counter() - start_time)
    left_time = 60 - play_time


# �����Ϸ�Ƿ����
def check_gameover():
    global win, lost
    # �ж���Ϸ�Ƿ�ʤ��
    if score >= 100:
        sounds.win.play()
        win = True
    # �ж���Ϸ�Ƿ�ʧ��
    if left_time <= 0:
        sounds.fail.play()
        lost = True


# ����������Ϣ
def draw_text():
    screen.draw.text("Time: " + str(left_time),
                     bottomleft=(WIDTH - 80, HEIGHT - 10), color="black")
    screen.draw.text("Score: " + str(score),
                     bottomleft=(10, HEIGHT - 10), color="black")
    if win:
        screen.draw.text("You Win!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=50, color="red")
    elif lost:
        screen.draw.text("You Lost!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=50, color="red")