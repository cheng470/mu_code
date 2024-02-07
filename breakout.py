# -*- coding:gb18030 -*-
# 打砖块游戏源代码breakout.py

import random
WIDTH = 640        # 屏幕宽度
HEIGHT = 400       # 屏幕高度
BRICK_W = 80       # 砖块宽度
BRICK_H = 20       # 砖块高度
started = False    # 小球发射标记
win = False        # 游戏胜利标记
lost = False       # 游戏失败标记
lives = 5          # 生命值
score = 0          # 游戏积分

# 创建挡板
pad = Actor("breakout_paddle", (WIDTH // 2, HEIGHT - 30))
pad.speed = 5      # 挡板移动速度

# 创建小球
ball = Actor("breakout_ball", (WIDTH // 2, HEIGHT - 47))

# 创建砖块列表
bricks = []
for i in range(5):
    for j in range(WIDTH // BRICK_W):
        brick = Actor("breakout_brick")
        brick.left = j * BRICK_W
        brick.top = 30 + i * BRICK_H
        bricks.append(brick)


# 更新游戏逻辑
def update():
    if win or lost:
        return
    pad_move()
    ball_move()
    collision_ball_bricks()
    collision_ball_pad()
    check_gameover()


# 绘制游戏图像
def draw():
    screen.fill((255, 255, 255))
    draw_text()
    ball.draw()
    pad.draw()
    for brick in bricks:
        brick.draw()


# 移动挡板
def pad_move():
    # 用键盘控制挡板移动
    if keyboard.right:
        pad.x += pad.speed
    elif keyboard.left:
        pad.x -= pad.speed
    # 将挡板限制在窗口范围内
    if pad.left < 0:
        pad.left = 0
    elif pad.right > WIDTH :
        pad.right = WIDTH


# 移动小球
def ball_move():
    global started, lives
    # 检测是否发射小球
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
    # 更新小球坐标
    ball.x += ball.vx
    ball.y += ball.vy
    # 检测及处理小球与窗口四周的碰撞
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


# 检测并处理小球与砖块的碰撞
def collision_ball_bricks():
    global score
    # 检测小球是否碰到砖块，若没有则返回
    n = ball.collidelist(bricks)
    if n == -1:
        return
    # 移除碰到的方块
    brick = bricks[n]
    bricks.remove(brick)
    # 增加游戏积分
    score += 100
    sounds.collide.play()
    # 设置小球反弹方向
    if  brick.left < ball.x < brick.right:     # 碰到砖块中部的反弹
        ball.vy *= -1
    elif ball.x <= brick.left:                 # 碰到砖块左部的反弹
        if ball.vx > 0:
            ball.vx *= -1
        else:
            ball.vy *= -1
    elif ball.x >= brick.right:                # 碰到砖块右部的反弹
        if ball.vx < 0:
            ball.vx *= -1
        else:
            ball.vy *= -1


# 检测并处理小球与挡板的碰撞
def collision_ball_pad():
    # 检测小球是否碰到挡板，若没有则返回
    if not ball.colliderect(pad):
        return
    # 垂直方向反弹
    if ball.y < pad.y:
        ball.vy = -abs(ball.vy)
        sounds.bounce.play()
    # 水平方向反弹
    if ball.x < pad.x:
        ball.vx = -abs(ball.vx)
    else:
        ball.vx = abs(ball.vx)


# 检测游戏是否结束
def check_gameover():
    global win, lost
    # 判断游戏是否胜利
    if len(bricks) == 0:
        sounds.win.play()
        win = True
    # 判断游戏是否失败
    if lives <= 0:
        sounds.fail.play()
        lost = True


# 绘制文字信息
def draw_text():
    screen.draw.text("Live: " + str(lives) + "   Score: " + str(score),
                     bottomleft=(5, HEIGHT - 5), color="black")
    if win:
        screen.draw.text("You Win!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=50, color="red")
    elif lost:
        screen.draw.text("You Lost!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=50, color="red")