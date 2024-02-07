# -*- coding:gb18030 -*-
# 打字游戏源代码typing.py

import random, time
WIDTH = 640                       # 屏幕宽度
HEIGHT = 400                      # 屏幕高度
MAX_NUM = 5                       # 窗口中气球的最大数量
balloons = []                     # 气球列表
balloon_queue = []                # 命中的气球队列
win = False                       # 游戏胜利标记
lost = False                      # 游戏失败标记
score = 0                         # 游戏积分
start_time = time.perf_counter()  # 初始时间
left_time = 60                    # 倒计时


# 更新游戏逻辑
def update():
    if win or lost:
        return
    if len(balloons) < MAX_NUM:
        add_balloon()
    update_balloon()
    check_gameover()
    count_time()


# 绘制游戏图像
def draw():
    screen.fill((255, 255, 255))
    draw_text()
    for balloon in balloons:
        balloon.draw()
        # 绘制气球上的字母，若命中显示白色，否则为黑色
        if balloon.typed:
            screen.draw.text(balloon.char,center=balloon.center,color="white")
        else:
            screen.draw.text(balloon.char,center=balloon.center,color="black")


# 处理键盘按键事件
def on_key_down(key):
    if win or lost:
        return
    global score
    # 检测按键是否和气球的字符相对应
    for balloon in balloons:
        if balloon.y > 0 and str(key) == "keys." + balloon.char:
            score += 1
            balloon.typed = True
            balloon_queue.append(balloon)
            # 延迟消除气球
            clock.schedule(remove_balloon, 0.3)
            break


# 从窗口中删除气球
def remove_balloon():
    sounds.eat.play()
    balloon = balloon_queue.pop(0)
    if balloon in balloons:
        balloons.remove(balloon)


# 向窗口中添加气球
def add_balloon():
    balloon = Actor("typing_balloon", (WIDTH // 2, HEIGHT))
    balloon.x = random_location()
    balloon.vy = random_velocity()
    balloon.char = random_char()
    balloon.typed = False
    balloons.append(balloon)


# 随机生成气球的初始位置
def random_location():
    min_dx = 0
    while min_dx < 50:
        min_dx = WIDTH
        x = random.randint(20, WIDTH - 20)
        for balloon in balloons:
            dx = abs(balloon.x - x)
            min_dx = min(min_dx, dx)
    return x


# 随机生成气球的移动速度
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


# 随机生成气球上的字母
def random_char():
    charset = set()
    for balloon in balloons:
        charset.add(balloon.char)
    ch = chr(random.randint(65, 90))
    while ch in charset:
        ch = chr(random.randint(65, 90))
    return ch


# 更新气球的位置
def update_balloon():
    for balloon in balloons:
        balloon.y += balloon.vy
        if balloon.bottom < 0:
            balloons.remove(balloon)


# 游戏倒计时
def count_time():
    global left_time
    play_time = int(time.perf_counter() - start_time)
    left_time = 60 - play_time


# 检测游戏是否结束
def check_gameover():
    global win, lost
    # 判断游戏是否胜利
    if score >= 100:
        sounds.win.play()
        win = True
    # 判断游戏是否失败
    if left_time <= 0:
        sounds.fail.play()
        lost = True


# 绘制文字信息
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