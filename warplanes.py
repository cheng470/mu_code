# -*- coding:gb18030 -*-
#�ɻ���ս��ϷԴ����warplanes.py

import random, time, math
WIDTH = 480                 # ��Ļ���
HEIGHT = 680                # ��Ļ�߶�
backgrounds = []            # ����ͼ���б�
backgrounds.append(Actor("warplanes_background", topleft=(0, 0)))
backgrounds.append(Actor("warplanes_background", bottomleft=(0, 0)))
hero = Actor("warplanes_hero1", midbottom=(WIDTH // 2, HEIGHT - 50))
hero.speed = 5              # ս���ƶ��ٶ�
hero.animcount = 0          # ս����������
hero.power = False          # �ӵ���ǿ���
hero.live = 5               # ����ֵ
hero.unattack = False       # �޵�״̬���
hero.ukcount = 0            # �޵�״̬����
hero.score = 0              # ��Ϸ����
gameover = False            # ��Ϸ�������
enemies = []                # �л��б�
bullets = []                # �ӵ��б�
powers = []                 # ��ǿ�����б�
# ���������б�
tweens = ["linear", "accelerate", "decelerate","accel_decel", \
          "in_elastic", "out_elastic", "in_out_elastic", \
          "bounce_end", "bounce_start", "bounce_start_end"]


# �����л�
def spawn_enemy():
    origin_x = random.randint(50, WIDTH)
    target_x = random.randint(50, WIDTH)
    tn = random.choice(tweens)
    dn = random.randint(3, 6)
    enemy = Actor("warplanes_enemy1", bottomright=(origin_x, 0))
    if random.randint(1, 100) < 20:
        enemy.image = "warplanes_enemy2"
    enemies.append(enemy)
    # ����ָ���Ļ���������ִ�л�������
    animate(enemy, tween=tn, duration=dn, topright=(target_x, HEIGHT))

# ���������ɵл���ÿ1�����һ�δ����л�������
clock.schedule_interval(spawn_enemy, 1.0)
music.play("warplanes")


# ������Ϸ�߼�
def update():
    if gameover:
        clock.unschedule(spawn_enemy)       # ֹͣ�Զ����ɵл�
        return
    update_background()
    update_hero()
    update_bullets()
    update_powerup()
    update_enemy()


# ������Ϸ�����ͽ�ɫ
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


# ������Ϸ����
def update_background():
    for backimage in backgrounds:
        backimage.y += 2
        if backimage.top > HEIGHT:
            backimage.bottom = 0


# ����ս��
def update_hero():
    move_hero()
    # ����ս�����ж���
    hero.animcount = (hero.animcount + 1) % 20
    if hero.animcount == 0:
        hero.image = "warplanes_hero1"
    elif hero.animcount == 10:
        hero.image = "warplanes_hero2"
    # �޵�״̬����
    if hero.unattack:
        hero.ukcount -= 1
        if hero.ukcount <= 0:
            hero.unattack = False
            hero.ukcount = 100


# �ƶ�ս��
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
        clock.schedule_unique(shoot, 0.1)    # �������ʱ��Ϊ0.1��
    if hero.left < 0:
        hero.left = 0
    elif hero.right > WIDTH:
        hero.right = WIDTH
    if hero.top < 0:
        hero.top = 0
    elif hero.bottom > HEIGHT:
        hero.bottom = HEIGHT


# �ӵ����
def shoot():
    sounds.bullet.play()
    bullets.append(Actor("warplanes_bullet", midbottom=(hero.x, hero.top)))
    # ��������ǿ��������������ö�ӵ�
    if hero.power:
        leftbullet = Actor("warplanes_bullet", midbottom=(hero.x, hero.top))
        leftbullet.angle = 15
        bullets.append(leftbullet)
        rightbullet = Actor("warplanes_bullet", midbottom=(hero.x, hero.top))
        rightbullet.angle = -15
        bullets.append(rightbullet)


# �����ӵ�
def update_bullets():
    for bullet in bullets:
        theta = math.radians(bullet.angle + 90)
        bullet.x += 10 * math.cos(theta)
        bullet.y -= 10 * math.sin(theta)
        if bullet.bottom < 0:
            bullets.remove(bullet)


# ������ǿ����
def update_powerup():
    for powerup in powers:
        powerup.y += 2
        if powerup.top > HEIGHT:
            powers.remove(powerup)
        elif powerup.colliderect(hero):
            powers.remove(powerup)
            hero.power = True
            clock.schedule(powerdown, 5.0)      # 5���Ӻ�ȡ����ǿЧ��
    if hero.power or len(powers) != 0:
        return
    # ���������ǿ����
    if random.randint(1, 1000) < 5:
            x = random.randint(50, WIDTH)
            powerup = Actor("warplanes_powerup", bottomright=(x, 0))
            powers.append(powerup)


# ȡ���ӵ���ǿЧ��
def powerdown():
    hero.power = False


# ���µл�
def update_enemy():
    global gameover
    for enemy in enemies:
        if enemy.top >= HEIGHT:
            enemies.remove(enemy)
            continue
        # ����Ƿ������ӵ�����
        n = enemy.collidelist(bullets)
        if n != -1:
            enemies.remove(enemy)
            bullets.remove(bullets[n])
            sounds.shooted.play()
            hero.score += 200 if enemy.image == "warplanes_enemy2" else 100
        # ����Ƿ���ײ��ս��
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


# ����ս��
def draw_hero():
    if hero.unattack:
        if hero.ukcount % 5 == 0:
            return
    hero.draw()


# ��������ֵͼ�����Ϸ����
def draw_hud():
    for i in range(hero.live):
        screen.blit("warplanes_live", (i * 35, HEIGHT - 35))
    screen.draw.text(str(hero.score), topleft=(20, 20),
                     fontname="marker_felt", fontsize=25)