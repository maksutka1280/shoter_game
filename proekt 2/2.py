from pygame import *
'''Необхідні класи'''

# клас-батько для спрайтів


class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#стінки
class  Wall(sprite.Sprite):
    def __init__(self, x = 0, y = 0, width = 10, height = 10, color = (100, 255, 100)):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

walls = [
    Wall(100, 0, 10, 350),
    Wall(100, 0, 600, 10),
    Wall(190, 100, 10, 600),
    Wall(190, 250, 70, 10, (156, 0, 0))
]

# клас-спадкоємець для спрайту-гравця (керується стрілками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# клас-спадкоємець для спрайта-ворога (переміщюється сам)


class Enemy(GameSprite):
    direction = "left"


    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Enemy2(Enemy):
    def set_route(self, route):
        self.route = route
        self.max_points = len(route) - 1
        self.point = len(route)
        self.steps = 0

    def update(self):
        if self.steps == 0:
            self.point += 1
            if self.point > self.max_points:
                self.point = 0

            self.speed_x = self.route[self.point][0]
            self.speed_y = self.route[self.point][1]
            self.steps = self.route[self.point][2]

        self.rect.x += self.speed_x 
        self.rect.y +=  self.speed_y
        self.steps -= 1
class Enemy3(Enemy):

    def update(self):
        pass

# Ігрова сцена:
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load(
    "background.jpg"), (win_width, win_height))

# Персонажі гри:
player = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)
monster2 = Enemy2('cyborg.png', win_width - 80, 280, 2)
new_route = [
    [-3, -1, 70], #швидкість по горизонталі, по вертикалі, кроки
    [-3,  1, 70],
    [ 3,  1, 70],
    [ 3,  -1, 70]
]
monster2.set_route(new_route)




game = True
finish = False
clock = time.Clock()
FPS = 60

# музика
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

mixer.music.set_volume(0.05)

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monster.update()
        monster2.update()

        player.reset()
        monster.reset()

        final.reset()

        monster2.reset()

        for w in walls:
            w.reset()
        
        if sprite.collide_rect(player , monster):
            kick.play()
            finish = True
        if sprite.collide_rect(player , monster2):
            kick.play()
            finish = True

        if sprite.collide_rect(player , final):
            money.play()
            finish = True
        
        for w in walls:
            if sprite.collide_rect(w , player):
                kick.play()
                finish = True
                break

    display.update()
    clock.tick(FPS)