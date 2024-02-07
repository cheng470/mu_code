# -*- coding:gb18030 -*-
# 五子棋游戏源代码gobang.py

import random
SIZE = 40                       # 棋盘方格尺寸
WIDTH = SIZE * 15               # 屏幕宽度
HEIGHT = SIZE * 15              # 屏幕高度
N = 0                           # 空位置
B = 2                           # 黑色棋子
W = 1                           # 白色棋子
S = 3                           # 下子位置
# 走棋模式列表
cdata = [# 一个棋子的情况
        [ N, N, N, S, B ], [ B, S, N, N, N ], [ N, N, N, S, B ], [ N, B, S, N, N ],		
        [ N, N, S, B, N ], [ N, N, B, S, N ], [ N, N, N, S, W ], [ W, S, N, N, N ],
        [ N, N, N, S, W ], [ N, W, S, N, N ], [ N, N, S, W, N ], [ N, N, W, S, N ],
        # 两个棋子的情况
        [ B, B, S, N, N ], [ N, N, S, B, B ], [ B, S, B, N, N ], [ N, N, B, S, B ],
        [ N, B, S, B, N ], [ N, B, B, S, N ], [ N, S, B, B, N ], [ W, W, S, N, N ],
        [ N, N, S, W, W ], [ W, S, W, N, N ], [ N, N, W, S, W ], [ N, W, S, W, N ],
        [ N, W, W, S, N ], [ N, S, W, W, N ],
        # 三个棋子的情况
        [ N, S, B, B, B ], [ B, B, B, S, N ], [ N, B, B, B, S ], [ N, B, S, B, B ],
        [ B, B, S, B, N ], [ N, S, W, W, W ], [ W, W, W, S, N ], [ N, W, W, W, S ],	
        [ N, W, S, W, W ], [ W, W, S, W, N ],
        # 四个棋子的情况
        [ S, B, B, B, B ], [ B, S, B, B, B ], [ B, B, S, B, B ], [ B, B, B, S, B ],
        [ B, B, B, B, S ], [ S, W, W, W, W ], [ W, S, W, W, W ], [ W, W, S, W, W ],
        [ W, W, W, S, W ], [ W, W, W, W, S ]]

AI_col = -1                     # 电脑下棋位置的列号
AI_row = -1                     # 电脑下棋位置的行号
max_level = -1                  # 走棋模式等级
# 棋盘信息列表
board = [[" "for i in range(15)]for j in range(15)]
chesses = []                    # 棋子列表
turn = "b"                      # 当前走棋方
last_turn = "w"                 # 上一步走棋方
gameover = False                # 游戏结束标记


# 处理鼠标点击事件
def on_mouse_down(pos, button):
    if gameover:
        return
    if turn == "b":
        if button == mouse.LEFT:             # 点击鼠标左键下棋
            play(pos)
        elif button == mouse.RIGHT:          # 点击鼠标右键悔棋
            retract()


# 更新游戏逻辑
def update():
    global gameover
    if gameover:
        return
    if check_win():
         gameover = True
         if last_turn == "b":
             sounds.win.play()
         else:
             sounds.fail.play()
         return
    if turn == "w":
        if AI_play():
            chess = Actor("gobang_white", (AI_col * SIZE + 20, AI_row * SIZE + 20))
            chesses.append(chess)
            change_side()


# 绘制游戏图像
def draw():
    screen.fill((210, 180, 140))
    draw_board()
    draw_chess()
    draw_text()


# 玩家下棋操作
def play(pos):
    col = pos[0] // SIZE
    row = pos[1] // SIZE
    if board[col][row] != " ":
        return
    chess = Actor("gobang_black", (col * SIZE + 20, row * SIZE + 20))
    chesses.append(chess)
    board[col][row] = turn
    change_side()


# 交换下棋双方
def change_side():
    global turn, last_turn
    last_turn = turn
    if turn == "b":
        turn = "w"
    else:
        turn = "b"


# 玩家悔棋操作
def retract():
    if len(chesses) == 0:
        return
    for i in range(2):                       # 连续撤回两枚棋子
        chess = chesses.pop()
        col = int(chess.x - 20) // SIZE
        row = int(chess.y - 20) // SIZE
        board[col][row] = " "


# 检查走棋某一方是否获胜
def check_win( ):
    a = last_turn
    # 从左上到右下判断是否形成五子连珠
    for i in range(11):
        for j in range(11):
            if board[i][j] == a and board[i + 1][j + 1] == a and board[i + 2][j + 2] == a \
              and board[i + 3][j + 3] == a and board[i + 4][j + 4] == a :
                return True
    # 从左下到右上判断是否形成五子连珠
    for i in range(11):
        for j in range(4, 15):
            if board[i][j] == a and board[i + 1][j - 1] == a and board[i + 2][j - 2] == a \
               and board[i + 3][j - 3] == a and board[i + 4][j - 4] == a :
                return True
    # 从上到下判断是否形成五子连珠
    for i in range(15):
        for j in range(11):
            if board[i][j] == a and board[i][j + 1] == a and board[i][j + 2] == a \
               and board[i][j + 3] == a and board[i][j + 4] == a :
                return True
    # 从左到右判断是否形成五子连珠
    for i in range(11):
        for j in range(15):
            if board[i][j] == a and board[i + 1][j] == a and board[i + 2][j] == a \
               and board[i + 3][j] == a and board[i + 4][j] == a :
                return True
    return False


# 电脑下棋
def AI_play():
    global AI_col, AI_row, max_level
    AI_col = -1
    AI_row = -1
    max_level = -1
    # 搜索棋盘上的每个下子位置
    for row in range(15):
        for col in range(15):
            # 从高到低搜索走棋模式列表中保存的每一级模式
            for level in range(len(cdata)-1, -1, -1):
                if level <= max_level:  # 若当前等级低于最高等级则跳出
                    break
                if col + 4 < 15:        # 从左到右匹配
                    if auto_match(row, col, level, 1, 0):
                        break
                if row + 4 < 15:        # 从上到下匹配
                    if auto_match(row, col, level, 0, 1):
                        break
                if col - 4 >= 0 and row + 4 < 15:  # 从右上到左下匹配
                    if auto_match(row, col, level, -1, 1):
                        break
                if col + 4 < 15 and row + 4 < 15:  # 从左上到右下匹配
                    if auto_match(row, col, level, 1, 1):
                        break
    # 若匹配到走棋模式，则将下子数据保存到棋盘信息列表
    if AI_col != -1 and AI_row != -1:
        board[AI_col][AI_row] = "w"
        return True
    # 若没能匹配到走棋模式，则随机生成一个下子位置
    while True:
        col = random.randint(0, 14)
        row = random.randint(0, 14)
        if board[col][row] == " ":
            board[col][row] = "w"
            AI_col = col
            AI_row = row
            return True
    return False


# 匹配走棋模式
def auto_match(row, col, level, dx, dy):
    global AI_col, AI_row, max_level
    col_sel = -1                 # 暂存下子位置的列号
    row_sel = -1                # 暂存下子位置的行号
    isfind = True                # 匹配成功标记
    # 沿指定方向匹配走棋模式，匹配宽度为5，方向由dx和dy决定
    for j in range(5):
        cs = board[col + j * dx][row + j * dy]
        if cs == " ":
            if cdata[level][j] == S:
                col_sel = col + j * dx
                row_sel = row + j * dy
            elif cdata[level][j] != N:
                isfind = False
                break
        elif cs == "b" and cdata[level][j] != B:
            isfind = False
            break
        elif cs == "w" and cdata[level][j] != W:
            isfind = False
            break
    # 若匹配成功，则更新走棋模式等级和电脑下子的位置
    if isfind:
        max_level = level
        AI_col = col_sel
        AI_row = row_sel
        return True
    return False


# 绘制棋子
def draw_chess():
    for chess in chesses:
        chess.draw()
    # 为上一步走的棋子绘制提示框
    if len(chesses) > 0:
        chess = chesses[-1]
        rect = Rect(chess.topleft, (36, 36))
        screen.draw.rect(rect, (255, 255, 255))


# 绘制棋盘
def draw_board():
    for i in range(15):
        screen.draw.line((20, SIZE * i + 20), (580, SIZE * i + 20), (0, 0, 0))
    for i in range(15):
        screen.draw.line((SIZE * i + 20, 20), (SIZE * i + 20, 580), (0, 0, 0))


#  绘制文字提示
def draw_text():
    if not gameover:
        return
    if last_turn == "b":
        text = "You Win"
    else:
        text = "You Lost"
    screen.draw.text(text, center=(WIDTH // 2, HEIGHT // 2), fontsize=100, color="red")