# -*- coding:gb18030 -*-
# 弹跳小球游戏源代码balls.py

WIDTH = 800                         # 屏幕宽度
HEIGHT = 600                        # 屏幕高度
NUM = 10                            # 小球数量
balls = []                          # 小球角色列表

for i in range(NUM):                # 生成小球角色
    ball = Actor("breakout_ball")
    ball.x = 50 * i + 100           # 设置小球水平坐标
    ball.y = 100                    # 设置小球垂直坐标
    ball.dx = 5 + i                 # 设置小球水平速度
    ball.dy = 5 + i                 # 设置小球垂直速度
    balls.append(ball)              # 将小球角色加入列表


# 更新游戏逻辑
def update():
    for ball in balls:
        ball.x += ball.dx           # 更新小球水平坐标
        ball.y += ball.dy           # 更新小球垂直坐标
        # 若小球碰到屏幕左右边界，则水平反向
        if ball.right > WIDTH or ball.left < 0:
            ball.dx = -ball.dx
        # 若小球碰到屏幕上下边界，则垂直反向
        if ball.bottom > HEIGHT or ball.top < 0:
            ball.dy = -ball.dy


# 绘制游戏图像
def draw():
    screen.fill((255, 255, 255))    # 清空屏幕
    for ball in balls:
        ball.draw()                 # 绘制小球