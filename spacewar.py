from pygame import *
from random import randint
class Gamesprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def draw (self):
        window.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group()
countdown = 0
countult = 0
countdown_relode = 0
zasobnik = 5
class Player(Gamesprite):
    def update(self):
        global countdown
        global zasobnik
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
        if countdown >= 60:
            if zasobnik != 0:
                if keys_pressed[K_f]:
                    self.fire()
                    countdown = 0
                    zasobnik -= 1

 

    
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.x, self.rect.y, 10)
        bullets.add(bullet)
    


pocitadlo_vybuchu = 0
class Enemy(Gamesprite):
    def update(self):
        global pocitadlo_vybuchu
        self.rect.y  += self.speed
        if self.rect.y > 490:
           pocitadlo_vybuchu += 1
           self.rect.x = randint(0, 700)
           self.rect.y = 0

class Bullet(Gamesprite):
    def update(self):
        keys_pressed = key.get_pressed()
        self.rect.y  -= self.speed
        if self.rect.y < 10:
            self.kill()




font.init()
font1 = font.SysFont("Arial", 36)
win = font1.render("YOU WIN", True, (255, 255, 255))
lose = font1.render("YOU LOSE", True, (255, 255, 255))

window = display.set_mode((700, 500))
display.set_caption("spacewar")
raketa = Player("rocket.png", 0, 450, 30)
background = transform.scale(image.load("galaxy.jpg"),(700, 500))
enemies = sprite.Group()

for I in range(5):
    x_enemy = randint(0, 700)
    nepratel = Enemy("ufo.png", x_enemy, 0, 1)
    enemies.add(nepratel)


mixer.init()
mixer_music.load("space.ogg")
mixer_music.play()
vyhra_sound = mixer.Sound("victory-1-90174.mp3")
lose_sound = mixer.Sound("losing-horn-313723.mp3")
clock = time.Clock()
FPS = 60

zivoty = 3
vyhra = False
game = True

pocitadlo_zastrelenich = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if vyhra != True:



        window.blit(background,(0, 0))
        raketa.update()
        raketa.draw()

        enemies.update()
        enemies.draw(window)

        bullets.update()
        bullets.draw(window)

        nahoda = randint(0, 1)
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            x_enemy = randint(0, 700)
            if nahoda == 0:
                nepratel = Enemy("ufo.png", x_enemy, 0, 1)   
            else:
                nepratel = Enemy("asteroid.png", x_enemy, 0, 1)
            enemies.add(nepratel)
            pocitadlo_zastrelenich += 1
        collides1 = sprite.spritecollide(raketa, enemies, False)
        for c in collides1:
            zivoty -= 1
            if zivoty == 0:
                lose_sound.play()
                window.blit(lose, (200, 200))
                mixer_music.stop()
                vyhra = True


        text_lose = font1.render("Missed: " + str(pocitadlo_vybuchu), 1, (255, 255, 255))
        window.blit(text_lose, (450, 0))
        text_win = font1.render("Shotted: " + str(pocitadlo_zastrelenich), 1, (255, 255, 255))
        window.blit(text_win, (450, 50))
        text_life = font1.render(str(zivoty), 1, (255, 255, 255))

        if pocitadlo_zastrelenich == 20:
            vyhra_sound.play()
            window.blit(win, (200, 200))
            mixer_music.stop()
            vyhra = True
        
        if pocitadlo_vybuchu == 2:
            zivoty -= 1
            pocitadlo_vybuchu = 0
            if zivoty == 0:
                lose_sound.play()
                window.blit(lose, (200, 200))
                mixer_music.stop()                   
                vyhra = True


        countdown += 1
        if zasobnik == 0:
            countdown_relode += 1
        
        if countdown_relode >= 180:
            zasobnik = 5
            countdown_relode = 0

        clock.tick(FPS) 
        display.update()