# -*- coding:gb18030 -*-
# ɨ����ϷԴ����minesweep.py

import random
BOMBS = 20               # ը������
ROWS = 15                # ��������
COLS = 15                # ��������
SIZE = 25                # ����ߴ�
WIDTH = SIZE * COLS      # ��Ļ���
HEIGHT = SIZE * ROWS     # ��Ļ�߶�
failed = False           # ��Ϸʧ�ܱ��
finished = False         # ��Ϸ��ɱ��
blocks = []              # �����б�

# �����з�����ӵ�������
for i in range(ROWS):
    for j in range(COLS):
        block = Actor("minesweep_block")
        block.left = j * SIZE       # ���÷����ˮƽλ��
        block.top = i * SIZE        # ���÷���Ĵ�ֱλ��
        block.isbomb = False        # ��Ƿ����Ƿ��������
        block.isopen = False        # ��Ƿ����Ƿ񱻴�
        block.isflag = False        # ��Ƿ����Ƿ��������
        blocks.append(block)

# ������ҷ����б�Ĵ���
random.shuffle(blocks)

# �������
for i in range(BOMBS):
    blocks[i].isbomb = True


# ������Ϸ�߼�
def update():
    global finished
    if finished or failed:
        return
    # ����Ƿ�����û����׵ķ��鶼����
    for block in blocks:
        if not block.isbomb and not block.isopen:
            return
    finished = True
    sounds.win.play()


# ������Ϸͼ��
def draw():
    for block in blocks:
        block.draw()
    if finished:
        screen.draw.text("Finished", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=100, color="red")
    elif failed:
        screen.draw.text("Failed", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=100, color="red")


# ����������¼�
def on_mouse_down(pos, button):
    if failed or finished:
        return
    for block in blocks:
        # �����鱻��������Ҹ÷���δ����
        if block.collidepoint(pos) and not block.isopen:
            # ������Ҽ��������
            if button == mouse.RIGHT:
                set_flag(block)
            # ��������������飬�ҷ���û�в�������
            elif button == mouse.LEFT and not block.isflag:
                if block.isbomb:
                    blow_up()
                else:
                    open_block(block)


# Ϊ�����������
def set_flag(block):
    if not block.isflag:
        block.image = "minesweep_flag"
        block.isflag = True
    else:
        block.image = "minesweep_block"
        block.isflag = False


# ���ױ�ը����ʾ���е���
def blow_up():
    global failed
    failed = True
    sounds.bomb.play()
    for i in range(BOMBS):
        blocks[i].image = "minesweep_bomb"


# �򿪷���
def open_block(bk):
    bk.isopen = True
    bombnum = get_bomb_number(bk)
    bk.image = "minesweep_number" + str(bombnum)
    if bombnum != 0:
        return
    # ��������Χû�е��ף���ݹ�ش���Χ�ķ���
    for block in get_neighbours(bk):
        if not block.isopen :
            open_block(block)


# ��ȡĳ������Χ�ĵ�������
def get_bomb_number(bk):
    num = 0
    for block in get_neighbours(bk):
        if block.isbomb:
            num += 1
    return num


# ��ȡĳ������Χ�����з���
def get_neighbours(bk):
    nblocks = []
    for block in blocks:
        if block.isopen:
            continue
        if block.x == bk.x - SIZE and block.y == bk.y \
          or block.x == bk.x + SIZE and block.y == bk.y \
          or block.x == bk.x and block.y == bk.y - SIZE \
          or block.x == bk.x and block.y == bk.y + SIZE \
          or block.x == bk.x - SIZE and block.y == bk.y - SIZE \
          or block.x == bk.x + SIZE and block.y == bk.y - SIZE \
          or block.x == bk.x - SIZE and block.y == bk.y + SIZE \
          or block.x == bk.x + SIZE and block.y == bk.y + SIZE :
            nblocks.append(block)
    return nblocks