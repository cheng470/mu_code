# -*- coding:gb18030 -*-
# ̰ʳ����ϷԴ����snake.py

import random
SIZE = 15              # ̰ʳ�߼�ʳ��ĳߴ�
WIDTH = SIZE * 30      # ��Ļ���
HEIGHT = SIZE * 30     # ��Ļ�߶�
finished = False       # ��Ϸ�������
counter = 0            # �ӳٱ���������̰ʳ���ƶ��ٶ�
direction = "east"     # �ƶ�����
length = 1             # ������
body = []              # ��������б�
dirs = {"east":(1, 0), "west":(-1, 0),
"north":(0, -1), "south":(0, 1)}

# ����̰ʳ��ͷ
snake_head = Actor("snake_head", (30 , 30))

# ����ʳ��������������
food = Actor("snake_food", (150, 150))
gridx = random.randint(2, WIDTH // SIZE - 2)
gridy = random.randint(2, HEIGHT // SIZE - 2)
food.x = gridx * SIZE
food.y = gridy * SIZE


# ������Ϸ�߼�
def update():
    if finished:
        return
    check_gameover()
    check_keys()
    eat_food()
    update_snake()


# ������Ϸ��ɫ
def draw():
    screen.fill((255, 255, 255))
    if finished:
       screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=50, color="red")
    for b in body:
        b.draw()
    snake_head.draw()
    food.draw()


# �����Ϸ�Ƿ����
def check_gameover():
    global finished
    # ��̰ʳ�߳������ڷ�Χ������Ϸ����
    if snake_head.left < 0 or snake_head.right > WIDTH or \
       snake_head.top < 0 or snake_head.bottom > HEIGHT:
        sounds.fail.play()
        finished = True
    # ����ͷ������������Ϸ����
    for n in range(len(body) - 1):
        if(body[n].x == snake_head.x and body[n].y == snake_head.y):
            sounds.fail.play()
            finished = True


# ��鷽����İ����¼�����������ͷ�ƶ�����
def check_keys():
    global direction
    #���������µļ������÷���ֵ����������ͷ����ȷ����
    if keyboard.right and direction != "west":
        direction = "east"
        snake_head.angle = 0
    elif keyboard.left and direction != "east":
        direction = "west"
        snake_head.angle = 180
    elif keyboard.up and direction != "south":
        direction = "north"
        snake_head.angle = 90
    elif keyboard.down and direction != "north":
        direction = "south"
        snake_head.angle = -90


# ���̰ʳ���Ƿ�Ե�ʳ���������Ӧ����
def eat_food():
    global length
    if food.x == snake_head.x and food.y == snake_head.y:
        sounds.eat.play()
        length += 1
        food.x = random.randint(2, WIDTH // SIZE - 2) * SIZE
        food.y = random.randint(2, HEIGHT // SIZE - 2) * SIZE


# ����̰ʳ��
def update_snake():
    # �ӻ�̰ʳ���ƶ��ٶ�
    global counter
    counter += 1
    if counter < 10:
        return
    else:
        counter = 0
	# ������ͷ������
    dx, dy = dirs[direction]
    snake_head.x += dx * SIZE
    snake_head.y += dy * SIZE
    # ����̰ʳ�ߵ�����
    if len(body) == length:
        body.remove(body[0])
    body.append(Actor("snake_body", (snake_head.x, snake_head.y)))