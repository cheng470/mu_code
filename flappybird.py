# -*- coding:gb18030 -*-
# Flappy Bird游戏源代码flappybird.py

import random
WIDTH = 138 * 4             # 窗口宽度（由四张背景图片组成）
HEIGHT = 396                # 窗口高度
GAP = 150                   # 上下水管间的缺口大小
SPEED = 3                   # 场景滚动速度
GRAVITY = 0.2               # 重力加速度
FLAP_VELOCITY = -5          # 飞扬时的初始速度
anim_counter = 0            # 小鸟动画计数器
score = 0                   # 游戏积分
score_flag = False          # 得分标记
started = False             # 游戏开始标记
backgrounds = []            # 背景图像列表

# 创建五张背景图像角色，用于循环滚动游戏场景
for i in range(5):
    backimage = Actor("flappybird_background", topleft=(i * 138, 0))
    backgrounds.append(backimage)

# 创建地面角色
ground = Actor("flappybird_ground", bottomleft=(0, HEIGHT))

# 创建上下水管角色
pipe_top = Actor("flappybird_top_pipe")
pipe_bottom = Actor("flappybird_bottom_pipe")

# 创建小鸟角色
bird = Actor("flappybird1", (WIDTH // 2, HEIGHT // 2))
bird.dead = False        # 标记小鸟是否存活
bird.vy = 0              # 设置小鸟垂直速度

# 创建GUI角色
gui_title = Actor("flappybird_title", (WIDTH // 2, 72))
gui_ready = Actor("flappybird_get_ready", (WIDTH // 2, 204 ))
gui_start = Actor("flappybird_start_button", (WIDTH // 2, 345))
gui_over = Actor("flappybird_game_over",(WIDTH // 2, HEIGHT // 2))


# 游戏逻辑更新
def update():
    if not started or bird.dead:
        return
    update_background()
    update_ground()
    update_pipes()
    fly()
    animation()
    check_collision()


# 绘制游戏角色
def draw():
    screen.fill((255, 255, 255))
    for backimage in backgrounds:
        backimage.draw()
    if not started:
        gui_title.draw()
        gui_ready.draw()
        gui_start.draw()
        return
    pipe_top.draw()
    pipe_bottom.draw()
    ground.draw()
    bird.draw()
    screen.draw.text(str(score), topleft=(30, 30), fontsize=30)
    if bird.dead:
        gui_over.draw()


# 处理鼠标点击事件
def on_mouse_down(pos):
    global started
    if bird.dead:
        return
    if started:
        bird.vy = FLAP_VELOCITY
        sounds.flap.play()
        return
    # 若点击开始按钮，初始化游戏
    if gui_start.collidepoint(pos):
        started = True
        reset_pipes()
        music.play("flappybird")


# 更新游戏场景，循环滚动背景图像
def update_background():
    for backimage in backgrounds:
        backimage.x -= SPEED
        if backimage.right <= 0:
            backimage.left = WIDTH


# 更新地面角色
def update_ground():
    ground.x -= SPEED
    if ground.right < WIDTH:
        ground.left = 0


# 更新水管角色
def update_pipes():
    pipe_top.x -= SPEED
    pipe_bottom.x -= SPEED
    if pipe_top.right < 0:
        reset_pipes()


# 重新设置上下水管出现的位置
def reset_pipes():
    global score_flag
    score_flag = True
    # 随机生成上方水管的垂直位置
    pipe_top.bottom = random.randint(50, 150)
    # 根据上方水管的垂直位置来设置下方水管的垂直位置
    pipe_bottom.top = pipe_top.bottom + GAP
    # 设置上下水管的水平位置
    pipe_top.left = WIDTH
    pipe_bottom.left = WIDTH


# 控制小鸟飞行
def fly():
    global score, score_flag
    # 当小鸟越过水管，则分数加一
    if score_flag and bird.x > pipe_top.right:
        score += 1
        score_flag = False
    # 更新小鸟坐标
    bird.vy += GRAVITY
    bird.y += bird.vy
    # 防止小鸟飞出窗口上边界
    if bird.top < 0:
        bird.top = 0


# 播放小鸟飞行的动画
def animation():
    global anim_counter
    anim_counter += 1
    if anim_counter == 2:
        bird.image = "flappybird1"
    elif anim_counter == 4:
        bird.image = "flappybird2"
    elif anim_counter == 6:
        bird.image = "flappybird3"
    elif anim_counter == 8:
        bird.image = "flappybird2"
        anim_counter = 0


# 小鸟与水管和地面的碰撞检测
def check_collision():
    if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom):
        sounds.collide.play()
        music.stop()
        bird.dead = True
    elif bird.colliderect(ground):
        sounds.fall.play()
        music.stop()
        bird.dead = True
