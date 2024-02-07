# -*- coding:gb18030 -*-
# ��������ϷԴ����gobang.py

import random
SIZE = 40                       # ���̷���ߴ�
WIDTH = SIZE * 15               # ��Ļ���
HEIGHT = SIZE * 15              # ��Ļ�߶�
N = 0                           # ��λ��
B = 2                           # ��ɫ����
W = 1                           # ��ɫ����
S = 3                           # ����λ��
# ����ģʽ�б�
cdata = [# һ�����ӵ����
        [ N, N, N, S, B ], [ B, S, N, N, N ], [ N, N, N, S, B ], [ N, B, S, N, N ],		
        [ N, N, S, B, N ], [ N, N, B, S, N ], [ N, N, N, S, W ], [ W, S, N, N, N ],
        [ N, N, N, S, W ], [ N, W, S, N, N ], [ N, N, S, W, N ], [ N, N, W, S, N ],
        # �������ӵ����
        [ B, B, S, N, N ], [ N, N, S, B, B ], [ B, S, B, N, N ], [ N, N, B, S, B ],
        [ N, B, S, B, N ], [ N, B, B, S, N ], [ N, S, B, B, N ], [ W, W, S, N, N ],
        [ N, N, S, W, W ], [ W, S, W, N, N ], [ N, N, W, S, W ], [ N, W, S, W, N ],
        [ N, W, W, S, N ], [ N, S, W, W, N ],
        # �������ӵ����
        [ N, S, B, B, B ], [ B, B, B, S, N ], [ N, B, B, B, S ], [ N, B, S, B, B ],
        [ B, B, S, B, N ], [ N, S, W, W, W ], [ W, W, W, S, N ], [ N, W, W, W, S ],	
        [ N, W, S, W, W ], [ W, W, S, W, N ],
        # �ĸ����ӵ����
        [ S, B, B, B, B ], [ B, S, B, B, B ], [ B, B, S, B, B ], [ B, B, B, S, B ],
        [ B, B, B, B, S ], [ S, W, W, W, W ], [ W, S, W, W, W ], [ W, W, S, W, W ],
        [ W, W, W, S, W ], [ W, W, W, W, S ]]

AI_col = -1                     # ��������λ�õ��к�
AI_row = -1                     # ��������λ�õ��к�
max_level = -1                  # ����ģʽ�ȼ�
# ������Ϣ�б�
board = [[" "for i in range(15)]for j in range(15)]
chesses = []                    # �����б�
turn = "b"                      # ��ǰ���巽
last_turn = "w"                 # ��һ�����巽
gameover = False                # ��Ϸ�������


# ����������¼�
def on_mouse_down(pos, button):
    if gameover:
        return
    if turn == "b":
        if button == mouse.LEFT:             # �������������
            play(pos)
        elif button == mouse.RIGHT:          # �������Ҽ�����
            retract()


# ������Ϸ�߼�
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


# ������Ϸͼ��
def draw():
    screen.fill((210, 180, 140))
    draw_board()
    draw_chess()
    draw_text()


# ����������
def play(pos):
    col = pos[0] // SIZE
    row = pos[1] // SIZE
    if board[col][row] != " ":
        return
    chess = Actor("gobang_black", (col * SIZE + 20, row * SIZE + 20))
    chesses.append(chess)
    board[col][row] = turn
    change_side()


# ��������˫��
def change_side():
    global turn, last_turn
    last_turn = turn
    if turn == "b":
        turn = "w"
    else:
        turn = "b"


# ��һ������
def retract():
    if len(chesses) == 0:
        return
    for i in range(2):                       # ����������ö����
        chess = chesses.pop()
        col = int(chess.x - 20) // SIZE
        row = int(chess.y - 20) // SIZE
        board[col][row] = " "


# �������ĳһ���Ƿ��ʤ
def check_win( ):
    a = last_turn
    # �����ϵ������ж��Ƿ��γ���������
    for i in range(11):
        for j in range(11):
            if board[i][j] == a and board[i + 1][j + 1] == a and board[i + 2][j + 2] == a \
              and board[i + 3][j + 3] == a and board[i + 4][j + 4] == a :
                return True
    # �����µ������ж��Ƿ��γ���������
    for i in range(11):
        for j in range(4, 15):
            if board[i][j] == a and board[i + 1][j - 1] == a and board[i + 2][j - 2] == a \
               and board[i + 3][j - 3] == a and board[i + 4][j - 4] == a :
                return True
    # ���ϵ����ж��Ƿ��γ���������
    for i in range(15):
        for j in range(11):
            if board[i][j] == a and board[i][j + 1] == a and board[i][j + 2] == a \
               and board[i][j + 3] == a and board[i][j + 4] == a :
                return True
    # �������ж��Ƿ��γ���������
    for i in range(11):
        for j in range(15):
            if board[i][j] == a and board[i + 1][j] == a and board[i + 2][j] == a \
               and board[i + 3][j] == a and board[i + 4][j] == a :
                return True
    return False


# ��������
def AI_play():
    global AI_col, AI_row, max_level
    AI_col = -1
    AI_row = -1
    max_level = -1
    # ���������ϵ�ÿ������λ��
    for row in range(15):
        for col in range(15):
            # �Ӹߵ�����������ģʽ�б��б����ÿһ��ģʽ
            for level in range(len(cdata)-1, -1, -1):
                if level <= max_level:  # ����ǰ�ȼ�������ߵȼ�������
                    break
                if col + 4 < 15:        # ������ƥ��
                    if auto_match(row, col, level, 1, 0):
                        break
                if row + 4 < 15:        # ���ϵ���ƥ��
                    if auto_match(row, col, level, 0, 1):
                        break
                if col - 4 >= 0 and row + 4 < 15:  # �����ϵ�����ƥ��
                    if auto_match(row, col, level, -1, 1):
                        break
                if col + 4 < 15 and row + 4 < 15:  # �����ϵ�����ƥ��
                    if auto_match(row, col, level, 1, 1):
                        break
    # ��ƥ�䵽����ģʽ�����������ݱ��浽������Ϣ�б�
    if AI_col != -1 and AI_row != -1:
        board[AI_col][AI_row] = "w"
        return True
    # ��û��ƥ�䵽����ģʽ�����������һ������λ��
    while True:
        col = random.randint(0, 14)
        row = random.randint(0, 14)
        if board[col][row] == " ":
            board[col][row] = "w"
            AI_col = col
            AI_row = row
            return True
    return False


# ƥ������ģʽ
def auto_match(row, col, level, dx, dy):
    global AI_col, AI_row, max_level
    col_sel = -1                 # �ݴ�����λ�õ��к�
    row_sel = -1                # �ݴ�����λ�õ��к�
    isfind = True                # ƥ��ɹ����
    # ��ָ������ƥ������ģʽ��ƥ����Ϊ5��������dx��dy����
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
    # ��ƥ��ɹ������������ģʽ�ȼ��͵������ӵ�λ��
    if isfind:
        max_level = level
        AI_col = col_sel
        AI_row = row_sel
        return True
    return False


# ��������
def draw_chess():
    for chess in chesses:
        chess.draw()
    # Ϊ��һ���ߵ����ӻ�����ʾ��
    if len(chesses) > 0:
        chess = chesses[-1]
        rect = Rect(chess.topleft, (36, 36))
        screen.draw.rect(rect, (255, 255, 255))


# ��������
def draw_board():
    for i in range(15):
        screen.draw.line((20, SIZE * i + 20), (580, SIZE * i + 20), (0, 0, 0))
    for i in range(15):
        screen.draw.line((SIZE * i + 20, 20), (SIZE * i + 20, 580), (0, 0, 0))


#  ����������ʾ
def draw_text():
    if not gameover:
        return
    if last_turn == "b":
        text = "You Win"
    else:
        text = "You Lost"
    screen.draw.text(text, center=(WIDTH // 2, HEIGHT // 2), fontsize=100, color="red")