# -*- coding:gb18030 -*-
# 扫雷游戏源代码minesweep.py

import random
BOMBS = 20               # 炸弹数量
ROWS = 15                # 方块行数
COLS = 15                # 方块列数
SIZE = 25                # 方块尺寸
WIDTH = SIZE * COLS      # 屏幕宽度
HEIGHT = SIZE * ROWS     # 屏幕高度
failed = False           # 游戏失败标记
finished = False         # 游戏完成标记
blocks = []              # 方块列表

# 将所有方块添加到场景中
for i in range(ROWS):
    for j in range(COLS):
        block = Actor("minesweep_block")
        block.left = j * SIZE       # 设置方块的水平位置
        block.top = i * SIZE        # 设置方块的垂直位置
        block.isbomb = False        # 标记方块是否埋设地雷
        block.isopen = False        # 标记方块是否被打开
        block.isflag = False        # 标记方块是否插上棋子
        blocks.append(block)

# 随机打乱方块列表的次序
random.shuffle(blocks)

# 埋设地雷
for i in range(BOMBS):
    blocks[i].isbomb = True


# 更新游戏逻辑
def update():
    global finished
    if finished or failed:
        return
    # 检查是否所有没埋地雷的方块都被打开
    for block in blocks:
        if not block.isbomb and not block.isopen:
            return
    finished = True
    sounds.win.play()


# 绘制游戏图像
def draw():
    for block in blocks:
        block.draw()
    if finished:
        screen.draw.text("Finished", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=100, color="red")
    elif failed:
        screen.draw.text("Failed", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=100, color="red")


# 处理鼠标点击事件
def on_mouse_down(pos, button):
    if failed or finished:
        return
    for block in blocks:
        # 若方块被鼠标点击，且该方块未曾打开
        if block.collidepoint(pos) and not block.isopen:
            # 若鼠标右键点击方块
            if button == mouse.RIGHT:
                set_flag(block)
            # 若鼠标左键点击方块，且方块没有插上棋子
            elif button == mouse.LEFT and not block.isflag:
                if block.isbomb:
                    blow_up()
                else:
                    open_block(block)


# 为方块插上棋子
def set_flag(block):
    if not block.isflag:
        block.image = "minesweep_flag"
        block.isflag = True
    else:
        block.image = "minesweep_block"
        block.isflag = False


# 地雷爆炸后显示所有地雷
def blow_up():
    global failed
    failed = True
    sounds.bomb.play()
    for i in range(BOMBS):
        blocks[i].image = "minesweep_bomb"


# 打开方块
def open_block(bk):
    bk.isopen = True
    bombnum = get_bomb_number(bk)
    bk.image = "minesweep_number" + str(bombnum)
    if bombnum != 0:
        return
    # 若方块周围没有地雷，则递归地打开周围的方块
    for block in get_neighbours(bk):
        if not block.isopen :
            open_block(block)


# 获取某方块周围的地雷数量
def get_bomb_number(bk):
    num = 0
    for block in get_neighbours(bk):
        if block.isbomb:
            num += 1
    return num


# 获取某方块周围的所有方块
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