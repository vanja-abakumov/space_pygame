# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import os
import random


class Player(pygame.sprite.Sprite):  # Класс спрайта наследуется от класса Sprite

    # Функция ( метод ) инициализации принимает в качестве параметра имя файла из которого создастся спрайт
    def __init__(self, file_name):
        pygame.sprite.Sprite.__init__(self)  # Вызываем функцию инициализации родителького класса Sprite
        img_file = os.path.join(IMG_FOLDER, file_name)  # Создаем путь к файлу file_name, в котором лежит картинка спрайта
        player_img = pygame.image.load(img_file)  # Создаем переменную, в которую загружаем картинку спрайта
        self.image = player_img.convert()  # Преобразуем загруженный спрайт в вид скоторым удобней работать pygame
        self.image.set_colorkey(BLACK)  # Удаляем лишние черные пиксели, что бы контур был ровный
        # Вызываем метод get_rect который тоже пришел к нам из класса Surface и он возвращает нам прямоугольник,
        # в котором находится на спрайт
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT / 2

        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Enemy(Player):

    def __init__(self, file_name):

        Player.__init__(self, file_name)
        self.speedx = random.randrange(1, 10)  # при инициализации класса один раз задается случайная скорость
        self.speedy = random.randrange(1, 10)  # при инициализации класса один раз задается случайная скорость
        self.rect.x = random.randrange(20, WIDTH - 20)
        self.rect.y = random.randrange(20, HEIGHT - 20)
        self.direction_x = 1
        self.direction_y = 1

    def update(self):
        self.rect.x += self.speedx * self.direction_x
        self.rect.y += self.speedy * self.direction_y

        if self.rect.x >= WIDTH:
            self.direction_x = -1
        if self.rect.x <= 0:
            self.direction_x = 1

        if self.rect.y < 0:
            self.direction_y = 1
        if self.rect.bottom > HEIGHT:
            self.direction_y = -1


class Star(Player):
    def __init__(self, file_name, x, y):
        Player.__init__(self, file_name)
        self.rect.bottom = y
        self.rect.centerx = x + 30
        self.speedy = -6

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


WIDTH = 480
HEIGHT = 600
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

number_of_enemies = random.randrange(1, 10)

# Настройка пути к папке img, где лежит графика для спрайтов ( папка асетов )
# __file__ магическая переменная Питона, в ней всегда находится путь с которого запущена программа
game_folder = os.path.dirname(__file__)  # Получение пути к папке где лежит игра в независимости от ОС
IMG_FOLDER = os.path.join(game_folder, 'img')  # Создаем путь к папке ing НЕ ЗАВИСИМО ОТ ИСПОЛЬЗУЕМОЙ ОС !!!

# Создаем игру и окно
pygame.init()
pygame.mixer.init()  # инициализируем звук
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()  # Создаем екземпляр класса Group в котором будут хранится наши спрайты
# Создаем экземпляр спрайта из графического файла, имя которого передаем через класс Player
player = Player('p1_jump.png')
all_sprites.add(player)  # Помещаем наш спрайт ( экземпляр класса Player ) в коробочку для хранения спрайтов
mobs = pygame.sprite.Group()  # Группа для врагов
stars = pygame.sprite.Group()  # Группа для пуль-звездочек

for i in range(number_of_enemies):
    enemy = Enemy('blockerMad.png')
    all_sprites.add(enemy)  # Помещаем наш спрайт ( экземпляр класса Player ) в коробочку для хранения спрайтов
    mobs.add(enemy)

# Цикл игры
HP = 3
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                star = Star("star.png", player.rect.x, player.rect.y)
                all_sprites.add(star)
                stars.add(star)

    # Обновление
    all_sprites.update()

    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, False)
    #if hits:
    #    running = False

    # Рендеринг
    screen.fill(BLUE)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
