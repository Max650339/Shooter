from pygame import *
from random import randint
import time as tm 


init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 15:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 615:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet('bullet.png', 4, self.rect.centerx - 7, self.rect.top, 15, 20)
        bullets.add(bullet)
        fire.set_volume(0.01)
        fire.play()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(50, 550)
            global missedcount 
            missedcount += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -30:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 510:
            self.rect.y = -40
            self.rect.x = randint(50, 600)

window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
player = Player('rocket.png', 5, 300, 400, 65, 100)
monsters = sprite.Group()
enemy1 = Enemy('ufo.png', 2, randint(50, 550), 10, 80, 50)
enemy2 = Enemy('ufo.png', 1, randint(50, 550), 20, 80, 50)
enemy3 = Enemy('ufo.png', 2, randint(50, 550), 0, 80, 50)
enemy4 = Enemy('ufo.png', 1, randint(50, 550), 30, 80, 50)
enemy5 = Enemy('ufo.png', 1, randint(50, 550), 25, 80, 50)
monsters.add(enemy1)
monsters.add(enemy2)
monsters.add(enemy3)
monsters.add(enemy4)
monsters.add(enemy5)
asteroids = sprite.Group()
asteroid1 = Asteroid('asteroid.png', 2, randint(50, 600), -100, 60, 60)
asteroid2 = Asteroid('asteroid.png', 1, randint(50, 600), -100, 60, 60)
asteroid3 = Asteroid('asteroid.png', 3, randint(50, 600), -100, 60, 60)
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
bullets = sprite.Group()

game = True
clock = time.Clock()
FPS = 60
finish = False
mixer.music.load('space.ogg')
mixer.music.set_volume(0.01)
mixer.music.play()
fire = mixer.Sound('fire.ogg')
scorecount = 0
missedcount = 0
lifescount = 3
lifescolor = (77, 255, 61)
num_fire = 0
rel_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    player.shoot()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start_time = tm.time()

            if e.key == K_r:
                scorecount = 0
                missedcount = 0
                lifes = 3
                for x in monsters:
                    x.kill()
                for x in bullets:
                    x.kill()
                for x in asteroids:
                    x.kill()
                for i in range(5):
                    enemy = Enemy('ufo.png', randint(1, 2), randint(50, 550), 0, 80, 50)
                    monsters.add(enemy)
                for i in range(3):
                    asteroid = Asteroid('asteroid.png', randint(1, 3), randint(50, 600), -100, 60, 60)
                    asteroids.add(asteroid)
                player.rect.x = 300
                player.rect.y = 400
                finish = False
                    

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        score = font.SysFont("verdana", 30).render(f"Счёт: {scorecount}", True, (255, 255, 255))
        missed = font.SysFont("verdana", 30).render(f"Пропущено: {missedcount}", True, (255, 255, 255))
        lifes = font.SysFont("verdana", 70).render(f"{lifescount}", True, lifescolor)
        window.blit(score, (20, 20))
        window.blit(missed, (20, 60))
        window.blit(lifes, (600, 20))
        bullets.update()
        bullets.draw(window)

        sprites_list1 = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list2 = sprite.spritecollide(player, monsters, True)
        sprites_list3 = sprite.spritecollide(player, asteroids, True)
        if sprites_list1:
            scorecount += 1 
            enemy = Enemy('ufo.png', randint(1, 2), randint(50, 550), 0, 80, 50)
            monsters.add(enemy)
        if sprites_list2:
            lifescount -= 1
            enemy = Enemy('ufo.png', randint(1, 2), randint(50, 550), 0, 80, 50)
            monsters.add(enemy)
        if sprites_list3:
            lifescount -= 1
            asteroid = Asteroid('asteroid.png', randint(1, 3), randint(50, 600), -100, 60, 60)
            asteroids.add(asteroid)
        if scorecount >= 10:
            win = font.SysFont("verdana", 70).render("YOU WIN!", True, (255, 255, 255))
            window.blit(win, (150, 200))
            finish = True
        if missedcount >= 5:
            lose = font.SysFont("verdana", 70).render("YOU LOSE!", True, (255, 255, 255))
            window.blit(lose, (150, 200))
            finish = True
        if lifescount <= 0:
            lose = font.SysFont("verdana", 70).render("YOU LOSE!", True, (255, 255, 255))
            window.blit(lose, (150, 200))
            finish = True
        if lifescount == 3:
            lifescolor = (77, 255, 61)
        if lifescount == 2:
            lifescolor = (247, 212, 35)
        if lifescount == 1:
            lifescolor = (217, 52, 52)
        if rel_time:
            if tm.time() - start_time < 3:
                reloadtext = font.SysFont("verdana", 20).render("Идёт перезарядка...", True, (217, 52, 52))
                window.blit(reloadtext, (250, 450))
            else:
                num_fire = 0
                rel_time = False

    clock.tick(FPS)
    display.update()