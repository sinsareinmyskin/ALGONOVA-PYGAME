#Create your own shooter
from random import randint
import pygame as gm

gm.init()
window = gm.display.set_mode((700, 400))
gm.display.set_caption("kebelet berak")
bg  = gm.transform.scale(gm.image.load("galaxy.jpg"), (700, 400))
fps = gm.time.Clock()

gm.mixer.init()
gm.mixer.music.load("space.ogg")
gm.mixer.music.set_volume(0.2)
gm.mixer.music.play(loops=True)
fire_sound = gm.mixer.Sound("fire.ogg")

img_monster = "asteroid.png"

gm.font.init()
font2 = gm.font.Font(None, 36)
score = 0
lost = 0

class GameSprite(gm.sprite.Sprite):
    def __init__(self, img, x, y, width, height, speed):
        gm.sprite.Sprite.__init__(self)
        self.image = gm.transform.scale(gm.image.load(img), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = gm.key.get_pressed()
        if keys[gm.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed        
        if keys[gm.K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player("rocket.png", 5, 300, 80, 100, 10)

monsters = gm.sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_monster, randint(80, 620), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

bullets = gm.sprite.Group()
gm.font.init()
font1 = gm.font.Font(None, 80)
win = font1.render("your did it", True, (255, 0, 255))
lose = font1.render("womp womp", True, (180, 0, 0))

finish = False
run = True
while run:
    for e in gm.event.get():
        if e.type == gm.QUIT:
            run = False
        elif e.type == gm.KEYDOWN:
            if e.key == gm.K_SPACE:
                sound = gm.mixer.Sound("fire.ogg")
                sound.play()
                ship.fire()
    if not finish:
        window.blit(bg, (0,0))
        
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Missed: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 50))
        bullets.update()
        bullets.draw(window)
        ship.update()
        monsters.update()
        ship.reset()
        monsters.draw(window)

        collides = gm.sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_monster, randint(80, 620), -40, 80, 50, randint(1, 3))
            monsters.add(monster)     

        if gm.sprite.spritecollide(ship, monsters, False) or lost >= 5:
            finish = True
            game = "lose"

        if score >= 10:
            finish = True
            game = "win"
    else:
        if game == "win":
            window.blit(win, (200, 200))
        elif game == "lose":
            window.blit(lose, (200, 200)) 
    gm.display.update()
    fps.tick(60)