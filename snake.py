# -*- coding:gb18030 -*-
# 贪食蛇游戏源代码snake.py

import random
SIZE = 15              # 贪食蛇及食物的尺寸
WIDTH = SIZE * 30      # 屏幕宽度
HEIGHT = SIZE * 30     # 屏幕高度
finished = False       # 游戏结束标记
counter = 0            # 延迟变量，控制贪食蛇移动速度
direction = "east"     # 移动方向
length = 1             # 蛇身长度
body = []              # 蛇身对象列表
dirs = {"east":(1, 0), "west":(-1, 0),
"north":(0, -1), "south":(0, 1)}

# 创建贪食蛇头
snake_head = Actor("snake_head", (30 , 30))

# 创建食物，并随机生成坐标
food = Actor("snake_food", (150, 150))
gridx = random.randint(2, WIDTH // SIZE - 2)
gridy = random.randint(2, HEIGHT // SIZE - 2)
food.x = gridx * SIZE
food.y = gridy * SIZE


# 更新游戏逻辑
def update():
    if finished:
        return
    check_gameover()
    check_keys()
    eat_food()
    update_snake()


# 绘制游戏角色
def draw():
    screen.fill((255, 255, 255))
    if finished:
       screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=50, color="red")
    for b in body:
        b.draw()
    snake_head.draw()
    food.draw()


# 检查游戏是否结束
def check_gameover():
    global finished
    # 若贪食蛇超出窗口范围，则游戏结束
    if snake_head.left < 0 or snake_head.right > WIDTH or \
       snake_head.top < 0 or snake_head.bottom > HEIGHT:
        sounds.fail.play()
        finished = True
    # 若蛇头碰到蛇身，则游戏结束
    for n in range(len(body) - 1):
        if(body[n].x == snake_head.x and body[n].y == snake_head.y):
            sounds.fail.play()
            finished = True


# 检查方向键的按下事件，来设置蛇头移动方向
def check_keys():
    global direction
    #根据所按下的键来设置方向值，并设置蛇头的正确朝向
    if keyboard.right and direction != "west":
        direction = "east"
        snake_head.angle = 0
    elif keyboard.left and direction != "east":
        direction = "west"
        snake_head.angle = 180
    elif keyboard.up and direction != "south":
        direction = "north"
        snake_head.angle = 90
    elif keyboard.down and direction != "north":
        direction = "south"
        snake_head.angle = -90


# 检查贪食蛇是否吃到食物，并进行相应处理
def eat_food():
    global length
    if food.x == snake_head.x and food.y == snake_head.y:
        sounds.eat.play()
        length += 1
        food.x = random.randint(2, WIDTH // SIZE - 2) * SIZE
        food.y = random.randint(2, HEIGHT // SIZE - 2) * SIZE


# 更新贪食蛇
def update_snake():
    # 延缓贪食蛇移动速度
    global counter
    counter += 1
    if counter < 10:
        return
    else:
        counter = 0
	# 更新蛇头的坐标
    dx, dy = dirs[direction]
    snake_head.x += dx * SIZE
    snake_head.y += dy * SIZE
    # 更新贪食蛇的身体
    if len(body) == length:
        body.remove(body[0])
    body.append(Actor("snake_body", (snake_head.x, snake_head.y)))