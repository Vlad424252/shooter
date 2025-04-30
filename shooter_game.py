#Создай собственный Шутер!
from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, speed, sizeX = 65, sizeY = 65):
        super().__init__()
        self.image = transform.scale(
            image.load(filename),
            (sizeX, sizeY)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image,(
            self.rect.x, self.rect.y
        ))
# управление ракетой
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x >= 10:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x <= 625:
            self.rect.x += self.speed
    def fire(self):
        global countFire
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE] and countFire > 30:
            bullets.add(Bullet('bullet.png', self.rect.centerx - 7, self.rect.y - 10, 10, 15, 30))
            countFire = 0
        countFire += 2

# пули
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
# враги
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint (0, 600)
            self.speed = randint (1, 5)
            lost = lost + 1

monsters = sprite.Group()
for i in range (5):
    monsters.add(Enemy('ufo.png', randint (0, 600), 15, randint (2, 5)))

asteroids = sprite.Group()
for i in range (1, 5):
    asteroids.add(Enemy('asteroid.png', randint (0, 600), 15, randint (2, 5)))

levels = [
    {"enemy_count": 10},
    {"enemy_count": 20},
    {"enemy_count": 30}
]

current_level_index = 0
def load_level(level_index):
    global monsters
    monsters.empty()
    
    level_data = levels[level_index]
    for _ in range(level_data["enemy_count"]):
        monsters.add(Enemy('ufo.png', randint (0, 600), 15, randint (2, 5)))

def check_level_complete():
    return len(monsters) == 0

# Загрузка первого уровня
load_level(current_level_index)


life = 3
lost = 0
score = 0
font.init()
font1 = font.SysFont('Arial', 34)
font2 = font.SysFont('Arial', 75)
text_lose = font1.render(
    'Пропущено:' + str(lost), 1, (255, 255, 255)
)

win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))

countFire = 0

bullets = sprite.Group()
for i in range (1):
    bullets.add(Enemy('bullet.png', randint (1, 6), 1, randint(1, 5)))

#создай окно игры
window = display.set_mode((700, 500))

#задай фон сцены
background = transform.scale(
    image.load('galaxy.jpg'),
    (700, 500)
)
#цикл игры
game = True
finish = False

# fps
clock = time.Clock()
speed = 10

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
#объекты
rocket = Player('rocket.png', 15, 400, 5)
bullet = Bullet('bullet.png', 15, 400, 5)

#отрисовка фона
while game:
    text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
    text = font1.render('Счёт:' + str(score), 1, (255, 255, 255))
    text_life = font1.render('Жизни:' + str(score), 1, (255, 255, 255))

    if not finish:
        window.blit(background, (0, 0))
        window.blit(text, (5, 30))
        window.blit(text_lose, (5, 60))
        window.blit(text_life, (5, 90))

        rocket.update()
        rocket.reset()
        rocket.fire()

        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

    # Проверка завершения уровня
        if check_level_complete():
            current_level_index += 1
            
            if current_level_index < len(levels):
                load_level(current_level_index)  # Загружаем следующий уровень
            else:
                print("Игра завершена!")
                game = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            # monster = Enemy('ufo.png', randint(80, 620), -40, randint(1, 5), 65, 65)
            # monsters.add(monster)

        collides_monsters = sprite.spritecollide(rocket, monsters, False)
        for m in collides_monsters:
            life = life - 1
            # sprite.spritecollide(rocket, monsters, True)
            m.kill()
            # monster = Enemy('ufo.png', randint(80, 620), -40, randint(1, 5), 65, 65)
            # monsters.add(monster)


        if lost >= 100 or life <= 0:
            finish = True
            window.blit(lose, (200, 200))

        if score >= 100:            
            finish = True
            window.blit(win, (200, 200))

        

    for e in event.get():
        if e.type == QUIT:
            game = False

    clock.tick(60)
    display.update()

