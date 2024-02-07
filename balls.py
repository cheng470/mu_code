# -*- coding:gb18030 -*-
# ����С����ϷԴ����balls.py

WIDTH = 800                         # ��Ļ���
HEIGHT = 600                        # ��Ļ�߶�
NUM = 10                            # С������
balls = []                          # С���ɫ�б�

for i in range(NUM):                # ����С���ɫ
    ball = Actor("breakout_ball")
    ball.x = 50 * i + 100           # ����С��ˮƽ����
    ball.y = 100                    # ����С��ֱ����
    ball.dx = 5 + i                 # ����С��ˮƽ�ٶ�
    ball.dy = 5 + i                 # ����С��ֱ�ٶ�
    balls.append(ball)              # ��С���ɫ�����б�


# ������Ϸ�߼�
def update():
    for ball in balls:
        ball.x += ball.dx           # ����С��ˮƽ����
        ball.y += ball.dy           # ����С��ֱ����
        # ��С��������Ļ���ұ߽磬��ˮƽ����
        if ball.right > WIDTH or ball.left < 0:
            ball.dx = -ball.dx
        # ��С��������Ļ���±߽磬��ֱ����
        if ball.bottom > HEIGHT or ball.top < 0:
            ball.dy = -ball.dy


# ������Ϸͼ��
def draw():
    screen.fill((255, 255, 255))    # �����Ļ
    for ball in balls:
        ball.draw()                 # ����С��