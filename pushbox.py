# -*- coding:gb18030 -*-
#��������ϷԴ����pushbox.py

TILESIZE = 48                            # ���ӳߴ�
WIDTH = TILESIZE * 11                    # ��Ļ���
HEIGHT = TILESIZE * 9                    # ��Ļ�߶�
# �����ֵ䣬�洢�������Ӧ������ƫ��ֵ
dirs = {"east":(1, 0), "west":(-1, 0),
        "north":(0, -1), "south":(0, 1), "none":(0, 0)}
level = 1                                # ��Ϸ�ؿ�ֵ
finished = False                         # ��Ϸ���ر��
gameover = False                         # ��Ϸ�������


# ���ļ���ȡ��ͼ����
def loadfile(file):
    mapfile = open(file,"r")             # ���ļ�
    map_array = []
    while True:
       line = mapfile.readline()         # ��ȡһ���ı�
       if line == "":                    # ��ȡ���������˳�
          break
       line = line.replace("\n","")      # ȥ�����з�
       line = line.replace(" ","")       # ȥ���ո�
       map_array.append(line.split(",")) # ���ı���ת��Ϊ�ַ��б�����
    mapfile.close()                      # �ر��ļ�
    return map_array


# ����ؿ���ͼ
def loadmap(level):
    try:
        mapdata = loadfile("maps/map" + str(level) + ".txt")
    except FileNotFoundError:
        global gameover
        gameover = True
    else:
        initlevel(mapdata)


# ��ʼ����ͼ��������Ϸ��ɫ
def initlevel(mapdata):
    global walls, floors, boxes, targets, player
    walls = []                           # ǽ���б�
    floors= []                           # �ذ��б�
    boxes = []                           # �����б�
    targets = []                         # Ŀ����б�
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


# ������̰����¼�
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


# �ƶ���ҽ�ɫ
def player_move():
    player.oldx = player.x
    player.oldy = player.y
    dx, dy = dirs[player.direction]
    player.x += dx * TILESIZE
    player.y += dy * TILESIZE


# ��ҽ�ɫ����ײ����봦��
def player_collision():
    # �����ǽ�ڵ���ײ
    if player.collidelist(walls) != -1:
        player.x = player.oldx
        player.y = player.oldy
        return
    # ��������ӵ���ײ
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


# ���ӽ�ɫ����ײ����봦��
def box_collision(box):
    box.oldx = box.x
    box.oldy = box.y
    dx, dy = dirs[player.direction]
    box.x += dx * TILESIZE
    box.y += dy * TILESIZE
    # ������ǽ�ڵ���ײ
    if box.collidelist(walls) != -1:
        return True
    # �������������ӵ���ײ
    for bx in boxes:
        if box == bx:
            continue
        if box.colliderect(bx):
            return True
    check_target(box)
    return False


# ��������Ƿ������Ŀ�����
def check_target(box):
    if box.collidelist(targets) != -1:
        box.image = "pushbox_box_hit"
        box.placed = True
    else:
        box.image = "pushbox_box"
        box.placed = False


# �ж��Ƿ����
def levelup():
    for box in boxes:
        if not box.placed:
            return False
    return True


# �����µĹؿ�
def setlevel():
    global finished, level
    finished = False
    level += 1
    loadmap(level)


# ������Ϸ�߼�
def update():
    global finished
    if finished or gameover:
        return
    if levelup():
        finished = True
        sounds.win.play()
        clock.schedule(setlevel, 5)


# ������Ϸͼ��
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