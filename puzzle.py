# -*- coding:gb18030 -*-
# ƴͼ��ϷԴ����puzzle.py

import random
SIZE = 96             # ͼƬ��ߴ�Ϊ96
WIDTH = SIZE * 3      # ��Ļ���
HEIGHT = SIZE * 3     # ��Ļ�߶�
finished = False      # ��Ϸ�������
pics = []             # ͼƬ���б�

# ѭ������ǰ8��ͼƬ�飬�������б�
for i in range(8):
    pic = Actor("puzzle_pic" + str(i))
    pic.index = i     # ͼƬ������ֵ
    pics.append(pic)

# ��������б��е�ͼƬ�����
random.shuffle(pics)

# Ϊ�б��е�ͼƬ���ó�ʼλ��
for i in range(8):
    pics[i].left = i % 3 * SIZE
    pics[i].top = i // 3 * SIZE

# �������һ��ͼƬ��
lastpic =Actor("puzzle_pic8")
lastpic.left = 2 * SIZE
lastpic.top = 2 * SIZE


# ������Ϸ�߼�
def update():
    global finished
    if finished:
        return
    # ���ƴͼ�Ƿ����
    for i in range(8):
        pic = get_pic(i % 3, i // 3)
        if(pic == None or pic.index != i):
            return
    finished = True
    sounds.win.play()   # ����ʤ������Ч


# ������Ϸ��ɫ
def draw():
    screen.fill((255, 255, 255))
    # ����ǰ8��ͼƬ��
    for pic in pics:
        pic.draw()
    # ����Ϸ�������������һ�飬����ʾ��������
    if finished == True:
        lastpic.draw()
        screen.draw.text("Finished!", center=(WIDTH // 2, HEIGHT // 2),
                          fontsize=50, color="red")


# �����갴���¼�
def on_mouse_down(pos):
    if finished:
        return
    grid_x = pos[0] // SIZE
    grid_y = pos[1] // SIZE
    # ��ȡ��ǰ�������ͼƬ��
    thispic = get_pic(grid_x, grid_y)
    if thispic == None:
        return
    # �ж�ͼƬ���Ƿ���������ƶ�
    if grid_y > 0 and get_pic(grid_x, grid_y - 1) == None:
        thispic.y -= SIZE
        return
    # �ж�ͼƬ���Ƿ���������ƶ�
    if grid_y < 2 and get_pic(grid_x, grid_y + 1) == None:
        thispic.y += SIZE
        return
    # �ж�ͼƬ���Ƿ���������ƶ�
    if grid_x > 0 and get_pic(grid_x - 1, grid_y) == None:
        thispic.x -= SIZE
        return
    # �ж�ͼƬ���Ƿ���������ƶ�
    if grid_x < 2 and get_pic(grid_x + 1, grid_y) == None:
        thispic.x += SIZE
        return


# ��ȡĳ�����񴦵�ͼƬ�飬����Ϊ�����ˮƽ�봹ֱ����ֵ
def get_pic(grid_x, grid_y):
    for pic in pics:
        if pic.x // SIZE == grid_x and pic.y // SIZE == grid_y:
            return pic
    return None