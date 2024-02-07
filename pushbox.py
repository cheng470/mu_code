# -*- coding:gb18030 -*-
#推箱子游戏源代码pushbox.py

TILESIZE = 48                            # 箱子尺寸
WIDTH = TILESIZE * 11                    # 屏幕宽度
HEIGHT = TILESIZE * 9                    # 屏幕高度
# 方向字典，存储各方向对应的坐标偏移值
dirs = {"east":(1, 0), "west":(-1, 0),
        "north":(0, -1), "south":(0, 1), "none":(0, 0)}
level = 1                                # 游戏关卡值
finished = False                         # 游戏过关标记
gameover = False                         # 游戏结束标记


# 从文件读取地图数据
def loadfile(file):
    mapfile = open(file,"r")             # 打开文件
    map_array = []
    while True:
       line = mapfile.readline()         # 读取一行文本
       if line == "":                    # 读取到空行则退出
          break
       line = line.replace("\n","")      # 去掉换行符
       line = line.replace(" ","")       # 去掉空格
       map_array.append(line.split(",")) # 将文本行转换为字符列表并保存
    mapfile.close()                      # 关闭文件
    return map_array


# 载入关卡地图
def loadmap(level):
    try:
        mapdata = loadfile("maps/map" + str(level) + ".txt")
    except FileNotFoundError:
        global gameover
        gameover = True
    else:
        initlevel(mapdata)


# 初始化地图，生成游戏角色
def initlevel(mapdata):
    global walls, floors, boxes, targets, player
    walls = []                           # 墙壁列表
    floors= []                           # 地板列表
    boxes = []                           # 箱子列表
    targets = []                         # 目标点列表
    for row in range(len(mapdata)):
        for col in range(len(mapdata[row])):
            x = col * TILESIZE
            y = row * TILESIZE
            if mapdata[row][col] >= "0" and mapdata[row][col] != "1":
                floors.append(Actor("pushbox_floor", topleft=(x, y)))
            if mapdata[row][col] == "1":
                walls.append(Actor("pushbox_wall", topleft=(x, y)))
            elif mapdata[row][col] == "2":
                box = Actor("pushbox_box", topleft=(x, y))
                box.placed = False
                boxes.append(box)
            elif mapdata[row][col] == "4":
                targets.append(Actor("pushbox_target", topleft=(x, y)))
            elif mapdata[row][col] == "6":
                targets.append(Actor("pushbox_target", topleft=(x, y)))
                box = Actor("pushbox_box_hit", topleft=(x, y))
                box.placed = True
                boxes.append(box)
            elif mapdata[row][col] == "3":
                player = Actor("pushbox_right", topleft=(x, y))

loadmap(level)


# 处理键盘按下事件
def on_key_down(key):
    if finished or gameover:
        return
    if key == keys.R:
        loadmap(level)
        return
    if key == keys.RIGHT:
        player.direction = "east"
        player.image = "pushbox_right"
    elif key == keys.LEFT:
        player.direction = "west"
        player.image = "pushbox_left"
    elif key == keys.DOWN:
        player.direction = "south"
        player.image = "pushbox_down"
    elif key == keys.UP:
        player.direction = "north"
        player.image = "pushbox_up"
    else:
        player.direction = "none"
    player_move()
    player_collision()


# 移动玩家角色
def player_move():
    player.oldx = player.x
    player.oldy = player.y
    dx, dy = dirs[player.direction]
    player.x += dx * TILESIZE
    player.y += dy * TILESIZE


# 玩家角色的碰撞检测与处理
def player_collision():
    # 玩家与墙壁的碰撞
    if player.collidelist(walls) != -1:
        player.x = player.oldx
        player.y = player.oldy
        return
    # 玩家与箱子的碰撞
    index = player.collidelist(boxes)
    if index == -1:
        return
    box = boxes[index]
    if box_collision(box) == True:
        box.x = box.oldx
        box.y = box.oldy
        player.x = player.oldx
        player.y = player.oldy
        return
    sounds.fall.play()


# 箱子角色的碰撞检测与处理
def box_collision(box):
    box.oldx = box.x
    box.oldy = box.y
    dx, dy = dirs[player.direction]
    box.x += dx * TILESIZE
    box.y += dy * TILESIZE
    # 箱子与墙壁的碰撞
    if box.collidelist(walls) != -1:
        return True
    # 箱子与其他箱子的碰撞
    for bx in boxes:
        if box == bx:
            continue
        if box.colliderect(bx):
            return True
    check_target(box)
    return False


# 检测箱子是否放置在目标点上
def check_target(box):
    if box.collidelist(targets) != -1:
        box.image = "pushbox_box_hit"
        box.placed = True
    else:
        box.image = "pushbox_box"
        box.placed = False


# 判断是否过关
def levelup():
    for box in boxes:
        if not box.placed:
            return False
    return True


# 设置新的关卡
def setlevel():
    global finished, level
    finished = False
    level += 1
    loadmap(level)


# 更新游戏逻辑
def update():
    global finished
    if finished or gameover:
        return
    if levelup():
        finished = True
        sounds.win.play()
        clock.schedule(setlevel, 5)


# 绘制游戏图像
def draw():
    screen.fill((200, 255, 255))
    if gameover:
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=80, color="red")
        return
    for floor in floors:
        floor.draw()
    for wall in walls:
        wall.draw()
    for target in targets:
        target.draw()
    for box in boxes:
        box.draw()
    player.draw()
    screen.draw.text("Level " + str(level), topleft=(20, 20),
                         fontsize=30, color="black")
    if finished:
        screen.draw.text("Level Up", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=80, color="blue")