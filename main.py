from play import *
import pygame
from random import *
import time


lost = 0
lost1 = 0
kill = 0
kill1=0
killSTR='0'
allEnemys = []




bullets=[]
# pygame.mixer.init()
# pygame.mixer.music.load('space.ogg')
# pygame.mixer.music.play()
background = new_image(image='galaxy.jpg')







pechenki=[]
plr = new_image('rocket.png',x=0,y=-250,size=5)
lostSTR='0'
hp = new_image(image='hp_0.png', x=-275, y=10, size=1750)
fireSound = pygame.mixer.Sound('fire.ogg')
killCheck = new_text(words=killSTR, x=245, y=235)
@repeat_forever
async def doGame():
    global bullets
    global pechenki
    global lost
    global lost1
    global kill
    global kill1
    global killSTR
    global lostSTR
    plr.start_physics(can_move=False)
    if key_is_pressed('a'):
        plr.x-=5
    if key_is_pressed('d'):
        plr.x+=5
    if key_is_pressed('w'):
        bullet = new_image(image='bullet.png', x=plr.x, y=-225, size=2)
        bullets.append(bullet)
    for one_bullet in bullets:
        one_bullet.y += 5
        if one_bullet.y > 300:
            one_bullet.remove()
            bullets.remove(one_bullet)
    def c():
        pechenka = new_image(image='ufo.png', x=randint(-200, 350), y=250, size=10)
        pechenki.append(pechenka)
    async def timeSpawn():
        await timer(2)
        c()
    timeSpawn()
    for one_pechenka in pechenki:
        one_pechenka.y -= randint(1,6)
        if one_pechenka.y < -300:
            one_pechenka.hide()
            one_pechenka.remove()
            pechenki.remove(one_pechenka)
            lost+=1
            print('-',lost)
        if len(pechenki) >= 50:
            for one_pechenka in pechenki:
                one_pechenka.hide()
            pechenki.clear()
        for one_pechenka in pechenki:
            if one_pechenka.is_touching(plr):
                lost+=1
                one_pechenka.hide()
                pechenki.remove(one_pechenka)
            # if one_pechenka.is_touching(bullet):
            #      one_pechenka.hide()
    if lost1 != lost:
        if lost == 0:
            hp.image='hp_0.png'
        elif lost == 1:
            hp.image='hp_1.png'
        elif lost == 2:
            hp.image='hp_2.png'
        elif lost == 3:
            hp.image='hp_3.png'
        elif lost == 4:
            hp.image='hp_4.png'
        lost1=lost

    if kill1 != kill:
        killSTR = str(kill)
        kill1 = kill
        killCheck.words=killSTR
    if kill >= 25:
        plr.hide()
        for one_pechenka in pechenki:
            one_pechenka.hide()
            pechenki.remove(one_pechenka)





















start_program()