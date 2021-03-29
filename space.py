# Pygame шаблон - скелет для нового проекта Pygame

import pygame
import os
import random


class Player(pygame.sprite.Sprite):  # Класс спрайта наследуется от класса Sprite

    # Функция ( метод ) инициализации принимает в качестве параметра имя файла из которого создастся спрайт
    def __init__(self, file_name):
        pygame.sprite.Sprite.__init__(self)  # Вызываем функцию инициализации родителького класса Sprite
        img_file_ = os.path.join(IMG_FOLDER, file_name)  # Создаем путь к файлу file_name, в котором лежит картинка
        # спрайта
        player_img = pygame.image.load(img_file_)  # Создаем переменную, в которую загружаем картинку спрайта
        self.image = player_img.convert()  # Преобразуем загруженный спрайт в вид скоторым удобней работать pygame
        self.image.set_colorkey(BLACK)  # Удаляем лишние черные пиксели, что бы контур был ровный
        # Вызываем метод get_rect который тоже пришел к нам из класса Surface и он возвращает нам прямоугольник,
        # в котором находится на спрайт
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50

        self.speedx = 0
        self.shield = 100
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
        self.rect.y = random.randrange(20, 100)
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


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, l_file_name: list, x: int, y: int, size_x: int, size_y: int):
        """
             Функция ( метод ) инициализации принимает в качестве параметра список имен файлов картинок из которых
             создастся анимация спрайта, координаты x,y где будет показана анимация и размер каждого спрайта

        :param x: Кордината по х где будет показана анимация
        :param y: Координата по y где будет показана анимация
        :param size_x: Размер каждого спрайта по х
        :param size_y: Размер каждого спрайта по y
        :param l_file_name: Список имен файлов из которых создается картинка

        """

        pygame.sprite.Sprite.__init__(self)  # Вызываем функцию инициализации родителького класса Sprite

        self.size_x = size_x  # Передаем size_х в внутреннее пространство имен класса
        self.size_y = size_y  # Передаем size_y в внутреннее пространство имен класса
        self.x = x  # Передаем х в внутреннее пространство имен класса
        self.y = y  # Передаем y в внутреннее пространство имен класса

        self.l_image = []  # Список где будут лежать подготовленные для анимации спрайты

        # Создаем спсиок спрайтов, для анимации
        for file_name in l_file_name:
            img_file_ = os.path.join(IMG_FOLDER, file_name)  # Создаем путь к файлу file_name, в котором лежит картинка
            player_img = pygame.image.load(img_file_)  # Создаем переменную, в которую загружаем картинку спрайта
            image = player_img.convert()  # Преобразуем загруженный спрайт в вид скоторым удобней работать pygame
            image.set_colorkey(BLACK)  # Удаляем лишние черные пиксели, что бы контур был ровный
            # Изменяем размер каждого спрайта на нужный нам
            image_new = pygame.transform.scale(image, (self.size_x, self.size_y))
            self.l_image.append(image_new)  # Добавляем в список спрайтов, новый спрайт анимации

        self.number_sprite = 0  # Номер спрайта, который сейчас показывается в анимации

        self.image = self.l_image[self.number_sprite]  # Показываем первый спрайт
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # last_update - время, когда был показан предидущий спрайт
        self.last_update = pygame.time.get_ticks()  # Инициализация last_update, временем инициализации класса

    def update(self):  # Помним, что эта функция ( метод ) вызывается pygame постоянно

        now = pygame.time.get_ticks()  # Внутреннее время pygame, которое есть сейчас
        if now - self.last_update > 50:  # Если с момента прошлого вызова, прошло более ХХ внутренних секунд, то..
            self.last_update = now  # Запонимаем в last_update время показа спрайта
            self.number_sprite += 1  # Переходим к показу следующего спрайта
            try:  # Пробуем показаеть следующий спрайт
                self.image = self.l_image[self.number_sprite]
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y

            except IndexError:  # Если, все спрайты кончились, то убиваем экземпляр класса
                self.kill()


def draw_text(surf: pygame.Surface, text: str, size: int, x: int, y: int):
    """
        Ф-ция для выведения текста, шрифтом arial

    :param surf: Поверхность, на которой будет написан текст, как вариант screen - просто на экране
    :param text: Собственно сам текст
    :param size: Размер шрифта, для выводимого текста
    :param x: Коррдинаты, где выводить текст
    :param y:
    :return:
    """

    font_name = pygame.font.match_font('arial')  # Получить имя шрифта, для шрифта типа arial
    font = pygame.font.Font(font_name, size)  # Получить сам шрифт, по его имени и размеру
    text_surface = font.render(text, True, RED)  # Преобразовать текст в набор пикселов ( редендринг )
    text_rect = text_surface.get_rect()  # Берем rect вокруг от редендренгового текста
    text_rect.midtop = (x, y)  # Помещаем центр rect в точку (x,y)
    # На поверхность surf наносится поверхность text_surface с координатами text_rect
    surf.blit(text_surface, text_rect)


def f_game_over():  # Выводим заставку в конце игры
    draw_text(screen, "Deep SPACE!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "by Ivan Abakumov", 32, WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()  # После отрисовки всего, переворачиваем экран
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            # Завершение игры или по закрытию окна или по нажатию клавиши q
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


WIDTH = 480  # Размер игрового окна по шире
HEIGHT = 600  # Размер игрового окна по высоте
FPS = 60

score = 0  # Счет за каждого убитого moba дают очко
lives = 10  # Количество жизней игрока

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

number_of_enemies = random.randrange(1, 10)  # Количество врагов на экране
# Список картинок из которых будет создан анимированный спрайт-взрыв
l_bang = ['regularExplosion00.png', 'regularExplosion01.png', 'regularExplosion02.png', 'regularExplosion03.png',
          'regularExplosion04.png', 'regularExplosion05.png', 'regularExplosion06.png', 'regularExplosion07.png',
          'regularExplosion08.png']

# Настройка пути к папке img, где лежит графика для спрайтов ( папка асетов )
# __file__ магическая переменная Питона, в ней всегда находится путь с которого запущена программа
game_folder = os.path.dirname(__file__)  # Получение пути к папке где лежит игра в независимости от ОС
IMG_FOLDER = os.path.join(game_folder, 'img')  # Создаем путь к папке ing НЕ ЗАВИСИМО ОТ ИСПОЛЬЗУЕМОЙ ОС !!!
SOUND_FOLDER = os.path.join(game_folder, 'sound')  # Создаем путь к папке sound НЕ ЗАВИСИМО ОТ ИСПОЛЬЗУЕМОЙ ОС !!!

# Создаем игру и окно
pygame.init()
pygame.mixer.init()  # инициализируем звук
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Загрузка фонового изображения
img_file = os.path.join(IMG_FOLDER, 'starfield.png')  # Создаем путь к файлу file_name, в котором лежит картинка спрайта
background = pygame.image.load(img_file).convert()
# Преобразование имиджа к размеру, переданному в кортедже
background_new = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background_new.get_rect()

# Загрузка мелодий игры
shoot_sound = pygame.mixer.Sound(os.path.join(SOUND_FOLDER, 'pew.wav'))  # Звук выстрела
pygame.mixer.music.load(os.path.join(SOUND_FOLDER, 'space.wav'))  # Фоновая музычка. Для фона почему то надо делать так
pygame.mixer.music.set_volume(0.4)  # Уровень громкости 40%
pygame.mixer.music.play(loops=-1)  # Начать проигрывание, саму мызыку зациклить по кругу

all_sprites = pygame.sprite.Group()  # Создаем екземпляр класса Group в котором будут хранится наши спрайты
# Создаем экземпляр спрайта из графического файла, имя которого передаем через класс Player
player = Player('p1_jump.png')
all_sprites.add(player)  # Помещаем наш спрайт ( экземпляр класса Player ) в коробочку для хранения спрайтов
mobs = pygame.sprite.Group()  # Группа для врагов
stars = pygame.sprite.Group()  # Группа для пуль-звездочек

for i in range(number_of_enemies):  # Создаем экземпляры класса врагов и помещаем их в специальную вражую группу
    enemy = Enemy('blockerMad.png')
    all_sprites.add(enemy)  # Помещаем наш спрайт ( экземпляр класса Player ) в коробочку для хранения спрайтов
    mobs.add(enemy)

# Цикл игры

running = True
while running:
    if number_of_enemies == 0:  # Когда все мобы убиты, то выпускаем новую стаю
        number_of_enemies = random.randrange(1, 10)  # Тот же код, что и выше, который выполняется при запуске
        for i in range(number_of_enemies):
            enemy = Enemy('blockerMad.png')
            all_sprites.add(enemy)  # Помещаем наш спрайт ( экземпляр класса Player ) в коробочку для хранения спрайтов
            mobs.add(enemy)

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Добавление звездочки-пули по нажатию пробела
                star_ = Star("star.png", player.rect.x, player.rect.y)
                all_sprites.add(star_)
                stars.add(star_)
                shoot_sound.play()

    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True)
    for hit in hits:  # Могут ударить несколько mob'ов одновременно
        lives -= 1  # Каждое соударение отбирает одну жизнь
        number_of_enemies -= 1  # при ударе моб исчезает, уменьшаем счетчик кол-ва мобов на один
        if lives == 0:  # Проверка не кончились ли жизни
            player.kill()
            f_game_over()
            running = False

    # роверка не сшибла ли звездочка mob'a
    for star_ in stars:
        hits = pygame.sprite.spritecollide(star_, mobs, True)
        for hit in hits:  # Одна звездочка может убить несколько мобов
            star_.kill()  # Убрать с экрана звездочку, которая попала в моба
            # Когда звездочка убила моба, то возникает взрыв. Создаем экземпляр класса, отвечающего за взрыв
            bang = AnimatedSprite(l_bang, star_.rect.x, star_.rect.y, 70, 70)
            all_sprites.add(bang)
            score += 1  # Добавляем очки за каждого убитого моба
            number_of_enemies -= 1  # Уменьшаем счетчик оставшихся мобов

    # Обновление
    all_sprites.update()

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background_new, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, f"Вы убили {score} mob'ов", 18, WIDTH / 2, 10)
    draw_text(screen, f"Остаток жизней {lives}", 25, WIDTH / 2, HEIGHT - 35)
    pygame.display.flip()  # После отрисовки всего, переворачиваем экран

pygame.quit()
