# -*- coding:gb18030 -*-
#飞机大战游戏源代码warplanes.py

import random, time, math
WIDTH = 480                 # 屏幕宽度
HEIGHT = 680                # 屏幕高度
backgrounds = []            # 背景图像列表
backgrounds.append(Actor("warplanes_background", topleft=(0, 0)))
backgrounds.append(Actor("warplanes_background", bottomleft=(0, 0)))
hero = Actor("warplanes_hero1", midbottom=(WIDTH // 2, HEIGHT - 50))
hero.speed = 5              # 战机移动速度
hero.animcount = 0          # 战机动画计数
hero.power = False          # 子弹增强标记
hero.live = 5               # 生命值
hero.unattack = False       # 无敌状态标记
hero.ukcount = 0            # 无敌状态计数
hero.score = 0              # 游戏积分
gameover = False            # 游戏结束标记
enemies = []                # 敌机列表
bullets = []                # 子弹列表
powers = []                 # 增强道具列表
# 缓动类型列表
tweens = ["linear", "accelerate", "decelerate","accel_decel", \
          "in_elastic", "out_elastic", "in_out_elastic", \
          "bounce_end", "bounce_start", "bounce_start_end"]


# 创建敌机
def spawn_enemy():
    origin_x = random.randint(50, WIDTH)
    target_x = random.randint(50, WIDTH)
    tn = random.choice(tweens)
    dn = random.randint(3, 6)
    enemy = Actor("warplanes_enemy1", bottomright=(origin_x, 0))
    if random.randint(1, 100) < 20:
        enemy.image = "warplanes_enemy2"
    enemies.append(enemy)
    # 根据指定的缓动类型来执行缓动操作
    animate(enemy, tween=tn, duration=dn, topright=(target_x, HEIGHT))

# 周期性生成敌机（每1秒调用一次创建敌机函数）
clock.schedule_interval(spawn_enemy, 1.0)
music.play("warplanes")


# 更新游戏逻辑
def update():
    if gameover:
        clock.unschedule(spawn_enemy)       # 停止自动生成敌机
        return
    update_background()
    update_hero()
    update_bullets()
    update_powerup()
    update_enemy()


# 绘制游戏场景和角色
def draw():
    if gameover:
        screen.blit("warplanes_gameover", (0, 0))
        return
    for backimgae in backgrounds:
        backimgae.draw()
    for enemy in enemies:
        enemy.draw()
    for powerup in powers:
        powerup.draw()
    for bullet in bullets:
        bullet.draw()
    draw_hud()
    draw_hero()


# 更新游戏场景
def update_background():
    for backimage in backgrounds:
        backimage.y += 2
        if backimage.top > HEIGHT:
            backimage.bottom = 0


# 更新战机
def update_hero():
    move_hero()
    # 播放战机飞行动画
    hero.animcount = (hero.animcount + 1) % 20
    if hero.animcount == 0:
        hero.image = "warplanes_hero1"
    elif hero.animcount == 10:
        hero.image = "warplanes_hero2"
    # 无敌状态计数
    if hero.unattack:
        hero.ukcount -= 1
        if hero.ukcount <= 0:
            hero.unattack = False
            hero.ukcount = 100


# 移动战机
def move_hero():
    if keyboard.right:
        hero.x += hero.speed
    elif keyboard.left:
        hero.x -= hero.speed
    if keyboard.down:
        hero.y += hero.speed
    elif keyboard.up:
        hero.y -= hero.speed
    if keyboard.space:
        clock.schedule_unique(shoot, 0.1)    # 射击冻结时间为0.1秒
    if hero.left < 0:
        hero.left = 0
    elif hero.right > WIDTH:
        hero.right = WIDTH
    if hero.top < 0:
        hero.top = 0
    elif hero.bottom > HEIGHT:
        hero.bottom = HEIGHT


# 子弹射击
def shoot():
    sounds.bullet.play()
    bullets.append(Actor("warplanes_bullet", midbottom=(hero.x, hero.top)))
    # 如果获得增强道具则额外添加两枚子弹
    if hero.power:
        leftbullet = Actor("warplanes_bullet", midbottom=(hero.x, hero.top))
        leftbullet.angle = 15
        bullets.append(leftbullet)
        rightbullet = Actor("warplanes_bullet", midbottom=(hero.x, hero.top))
        rightbullet.angle = -15
        bullets.append(rightbullet)


# 更新子弹
def update_bullets():
    for bullet in bullets:
        theta = math.radians(bullet.angle + 90)
        bullet.x += 10 * math.cos(theta)
        bullet.y -= 10 * math.sin(theta)
        if bullet.bottom < 0:
            bullets.remove(bullet)


# 更新增强道具
def update_powerup():
    for powerup in powers:
        powerup.y += 2
        if powerup.top > HEIGHT:
            powers.remove(powerup)
        elif powerup.colliderect(hero):
            powers.remove(powerup)
            hero.power = True
            clock.schedule(powerdown, 5.0)      # 5秒钟后取消增强效果
    if hero.power or len(powers) != 0:
        return
    # 随机生成增强道具
    if random.randint(1, 1000) < 5:
            x = random.randint(50, WIDTH)
            powerup = Actor("warplanes_powerup", bottomright=(x, 0))
            powers.append(powerup)


# 取消子弹增强效果
def powerdown():
    hero.power = False


# 更新敌机
def update_enemy():
    global gameover
    for enemy in enemies:
        if enemy.top >= HEIGHT:
            enemies.remove(enemy)
            continue
        # 检测是否碰被子弹击中
        n = enemy.collidelist(bullets)
        if n != -1:
            enemies.remove(enemy)
            bullets.remove(bullets[n])
            sounds.shooted.play()
            hero.score += 200 if enemy.image == "warplanes_enemy2" else 100
        # 检测是否碰撞到战机
        elif enemy.colliderect(hero) and not hero.unattack:
            hero.live -= 1
            if hero.live > 0:
                hero.unattack = True
                hero.ukcount = 100
                enemies.remove(enemy)
                sounds.shooted.play()
            else:
                sounds.gameover.play()
                gameover = True
                music.stop()
                time.sleep(0.5)


# 绘制战机
def draw_hero():
    if hero.unattack:
        if hero.ukcount % 5 == 0:
            return
    hero.draw()


# 绘制生命值图像和游戏积分
def draw_hud():
    for i in range(hero.live):
        screen.blit("warplanes_live", (i * 35, HEIGHT - 35))
    screen.draw.text(str(hero.score), topleft=(20, 20),
                     fontname="marker_felt", fontsize=25)