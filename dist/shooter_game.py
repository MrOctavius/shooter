#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer
window = display.set_mode((700, 500))
display.set_caption("Шутер")

background = transform.scale(image.load("galaxy.jpg"),(700, 500))

font.init()
font1 = font.SysFont('Arial', 36)

number_fire = 0

rtime = False

lost = 0
stol = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self): 
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x, self.rect.top, 15)
        bullets.add(bullet)

class Enemy(GameSprite): 
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 400:

            self.rect.x = randint(10,650)
            self.rect.y = 0
            self.speed = randint(1,4)
            global lost
            lost = lost + 1
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
    


rocket = Player('rocket.png', 50, 430, 5)
bullets = sprite.Group()
sprites = sprite.Group()
asteroids = sprite.Group()

for i in range(8):
    vrag = Enemy('ufo.png', randint(0, 600), 0, randint(1, 2))
    sprites.add(vrag)

for i in range(4):
    vrag = Enemy('asteroid.png', randint(0, 650), 0, randint(1, 2))
    asteroids.add(vrag)

clock = time.Clock()
FPS = 60


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
finish = False
game = True
while game:
    if not finish:
        window.blit(background,(0, 0))
        rocket.reset()
        rocket.update()
        sprites.draw(window)
        sprites.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
    
    text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
    window.blit(text_lose, (10,40))
    
    text_stol = font1.render("Счет: " + str(stol), 1, (255, 255, 255))
    window.blit(text_stol, (10,10))
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if number_fire < 5:
                    rocket.fire()
                    kick = mixer.Sound('fire.ogg')
                    number_fire += 1
                if number_fire >= 5 and rtime == False:
                    rtime = True
                    ntime1 = timer()
    sprites_list = sprite.groupcollide(bullets, sprites, True, True)        
    for wed in sprites_list:
        vrag = Enemy('ufo.png', randint(0, 600), 0, randint(1, 2))
        sprites.add(vrag)
        stol += 1
        
    
    if stol > 10:
        finish = True
        font = font1.render("YOU WIN!!!", 1, (255, 255, 255))
        window.blit(font, (250,250))

    


    if sprite.spritecollide(rocket, sprites, True) or lost > 3:
        finish = True
        font = font1.render("YOU LOSE!!!", 1, (255, 255, 255))
        window.blit(font, (250,250))

    if rtime == True:
        ntime2 = timer()
        if ntime2 - ntime1 < 1:
            waitsecond = font1.render("WAIT...", True, (255, 255, 255))
            window.blit(waitsecond, (300, 420))
        else:
            number_fire = 0
            rtime = False

    clock.tick(FPS)
    display.update()
    
