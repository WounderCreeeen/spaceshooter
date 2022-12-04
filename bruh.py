# Создай собственный Шутер!
from time import time as timer
from random import randint
from pygame import *
from time import sleep

win_width = 700
win_height = 500

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

score = 0
lost = 0
clock = time.Clock()
lives = 3
num_fire = 0

display.set_caption('moguss in space')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
fps = 800


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_s] and self.rect.y < win_height - 100:
            self.rect.y += self.speed
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


class Obstacle(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0


font.init()
font1 = font.SysFont(None, 80)
win = font1.render('Amogla gg wp', True, (240, 224, 29))
loss = font1.render('u ded', True, (182, 61, 27))

font2 = font.SysFont(None, 36)

ship = Player(img_hero, 5, win_height - 100, 80, 100, 100 * 60 / fps)
monsters = sprite.Group()
obstacles = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(70, win_width - 70), -100, 80, 50, randint(2, 4))
    monsters.add(monster)

for i in range(1, 3):
    ast = Obstacle(img_asteroid, randint(70, win_width - 70), -100, 80, 50, randint(2, 4))
    obstacles.add(ast)

players = sprite.Group()
players.add(ship)
bullets = sprite.Group()
finish = False
run = True
rel_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Score:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 10))

        text_lose = font2.render('Skipped:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 40))

        ship.update()
        monsters.update()

        ship.reset()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        obstacles.update()
        obstacles.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Reloading', 1, (150, 0, 0))
                window.blit(reload, (260, 240))
            else:
                num_fire = 0
                rel_time = False

        if lives == 3:
            life_color = (0, 150, 0)
        if lives == 2:
            life_color = (150, 150, 0)
        if lives == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(lives), 1, life_color)
        window.blit(text_life, (600, 100))

        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for c in sprite_list:
            monster = Enemy(img_enemy, randint(70, win_width - 70), -100, 80, 50, randint(2, 4))
            monsters.add(monster)
            score += 1

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, obstacles, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, obstacles, True)
            lives -= 1

        if lost >= 10 or lives < 1:
            window.blit(loss, (290, 200))
            mixer.music.pause()
            finish = True

        else:
            num_fire = 0
            rel_time = False

        display.update()

    time.delay(30)
    clock.tick(fps)