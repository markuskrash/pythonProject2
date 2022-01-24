import math
import pygame
import random
import sqlite3

con = sqlite3.connect("identifier.sqlite")
cur = con.cursor()

all_sprites = pygame.sprite.Group()
sprites_of_hero = pygame.sprite.Group()
sprites_of_swords = pygame.sprite.Group()
sprites_of_armor = pygame.sprite.Group()
sprites_of_skills = pygame.sprite.Group()
sprites_of_level = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
all_borders = pygame.sprite.Group()
inv_borders = pygame.sprite.Group()
sprites_of_background = pygame.sprite.Group()
all_enemy = pygame.sprite.Group()
sprites_of_HAGIVAGI = pygame.sprite.Group()
sprites_of_slime = pygame.sprite.Group()
sprites_of_altar = pygame.sprite.Group()
vertical_borders_of_enemy = pygame.sprite.Group()
sprites_of_money = pygame.sprite.Group()

enemy_speed = 2

move_speed = 6
jump_speed = 18
acceleration = 1
g_acc = 1.3

levels_count = [0]
flag_level = [1]

money = {
    'gold': 1,
    'silver': 2,
    'copper': 3
}

levels = [open('level_1', 'r', encoding='utf-8').read(),
          open('level_2', 'r', encoding='utf-8').read(),
          open('level_3', 'r', encoding='utf-8').read()]

ground_width = 28
ground_height = 28

text_for_legend = [open('text_for_legend', 'r', encoding='utf-8').read(),
                   open('text_of_legend2', 'r', encoding='utf-8').read(),
                   open('text_of_legend3', 'r', encoding='utf-8').read()]

is_end = [0]
text_for_end = ["Вы умерли и не воскресили своего брата",
                "Я уверен, он был бы рад, воскресив вы его"]

text_for_win = [open('text_for_win1', 'r', encoding='utf-8').read(),
                open('text_for_win2', 'r', encoding='utf-8').read(),
                open('text_for_win3', 'r', encoding='utf-8').read()
                ]


class rules_of_game(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('fon_of_legend.jpg'), (1550, 800))

    def __init__(self, screen):
        super().__init__(sprites_of_background)
        self.image = rules_of_game.image
        self.rect = self.image.get_rect()
        self.screen = screen

    def draw(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('arial', 24)
        text_coord = 50
        for line in text.split('\n'):
            string_rendered = font.render(line, True, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)


class hero(pygame.sprite.Sprite):
    image = [pygame.image.load('h1.png')]
    image.append(pygame.image.load('h2.png'))
    image.append(pygame.image.load('h3.png'))
    image.append(pygame.image.load('h4.png'))
    image.append(pygame.image.load('h5.png'))
    image.append(pygame.image.load('h6.png'))
    image.append(pygame.image.load('hit1.png'))
    image.append(pygame.image.load('hit2.png'))
    image.append(pygame.image.load('hero_jump.png'))
    image.append(pygame.image.load('hero_jump2.png'))

    def __init__(self, x, y):
        super().__init__(sprites_of_hero, all_sprites)
        self.image = hero.image[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed_x = 0
        self.direction_x = 1
        self.is_move_x = 0
        self.braking_x = 0

        self.on_ground = 0
        self.speed_y = 0
        self.is_move_y = 0
        self.braking_y = 0

        self.anim = 0

        self.is_hit = 20

    def move_x(self, boost):
        self.anim += 1
        if self.speed_x > 0 and self.on_ground:
            self.image = hero.image[self.anim // 10 % 3]
        elif self.speed_x < 0 and self.on_ground:
            self.image = hero.image[self.anim // 10 % 3 + 3]
        elif self.direction_x > 0 and self.on_ground:
            self.image = hero.image[1]
        elif self.on_ground:
            self.image = hero.image[4]
        elif self.direction_x > 0:
            self.image = hero.image[8]
        else:
            self.image = hero.image[9]

        if self.direction_x * self.speed_x < 0:
            self.braking_x = 1
        else:
            self.braking_x = 0

        if self.is_move_x != 0:
            self.speed_x += self.direction_x * acceleration * boost
        elif self.speed_x:
            self.speed_x -= self.direction_x * acceleration * boost
            if self.speed_x * self.direction_x < 0:
                self.speed_x = 0

        if self.speed_x > move_speed:
            self.speed_x = move_speed
        if self.speed_x < -move_speed:
            self.speed_x = -move_speed

        self.rect.x += self.speed_x
        self.collision_with_borders(1)

        if self.on_ground and self.is_move_y:

            self.speed_y -= jump_speed
            self.on_ground = 0
        else:
            self.speed_y += g_acc
        self.rect.y += self.speed_y
        self.collision_with_borders(0)

    def hit(self):
        if self.is_hit <= 20:
            if self.speed_x > 0:
                self.image = hero.image[6]
            elif self.speed_x < 0:
                self.image = hero.image[7]
            elif self.direction_x > 0:
                self.image = hero.image[6]
            elif self.direction_x < 0:
                self.image = hero.image[7]

    def collision_with_borders(self, fl):
        if fl and pygame.sprite.spritecollideany(self, vertical_borders) and self.speed_x != 0:
            if self.speed_x > 0:
                self.rect.right = pygame.sprite.spritecollide(self, vertical_borders, False)[0].rect.left
            if self.speed_x < 0:
                self.rect.left = pygame.sprite.spritecollide(self, vertical_borders, False)[0].rect.right
            self.speed_x = 0
        if not fl and pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.speed_y < 0:
                self.rect.top = pygame.sprite.spritecollide(self, horizontal_borders, False)[0].rect.bottom
            if self.speed_y > 0:
                self.rect.bottom = pygame.sprite.spritecollide(self, horizontal_borders, False)[0].rect.top
            self.speed_y = 0
            self.on_ground = 1
            self.is_move_y = 0


class enemy_slime(pygame.sprite.Sprite):
    image = [pygame.image.load('slime.png')]
    image.append(pygame.image.load('slime2.png'))

    def __init__(self, x, y):
        super().__init__(sprites_of_slime, all_enemy, all_sprites)
        self.image = enemy_slime.image[1]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.speed = enemy_speed
        self.coll = 1

    def move(self):
        self.rect.x += self.speed
        self.collision_with_borders()

    def collision_with_borders(self):
        if pygame.sprite.spritecollideany(self, vertical_borders_of_enemy):
            self.speed = -self.speed
            self.coll += 1
            self.image = enemy_slime.image[self.coll % 2]
        if pygame.sprite.spritecollideany(self, sprites_of_hero):
            hero = pygame.sprite.spritecollide(self, sprites_of_hero, False)[0]
            if hero.is_hit <= 20 and (hero.rect.centerx - self.rect.centerx) * hero.direction_x < 0:
                self.kill()
            else:
                is_end[0] = 1


class enemy_HAGIVAGI(pygame.sprite.Sprite):
    image = [pygame.image.load('hagivagi1.png')]
    image.append(pygame.image.load('hagivagi2.png'))
    image.append(pygame.image.load('hagivagi3.png'))

    def __init__(self, x, y):
        super().__init__(sprites_of_HAGIVAGI, all_enemy, all_sprites)
        self.image = enemy_HAGIVAGI.image[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.coll = random.randint(0, 180)

    def collision_with_borders(self):
        self.coll += 1
        if self.coll % 300 <= 180:
            self.image = enemy_HAGIVAGI.image[0]
        elif self.coll % 300 <= 210:
            self.image = enemy_HAGIVAGI.image[1]
        elif self.coll % 300 <= 300:
            self.image = enemy_HAGIVAGI.image[2]
        if pygame.sprite.spritecollideany(self, sprites_of_hero):
            hero = pygame.sprite.spritecollide(self, sprites_of_hero, False)[0]
            if self.coll % 300 <= 180 and hero.is_hit <= 20 and (
                    hero.rect.centerx - self.rect.centerx) * hero.direction_x < 0:
                self.kill()
            if self.coll % 300 > 180:
                is_end[0] = 1


class enemy_border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites, vertical_borders_of_enemy)
        self.image = pygame.Surface([0, y2 - y1])
        self.rect = pygame.Rect(x1, y1, 1, y2 - y1)


class gh_border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([0, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 0])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class border(pygame.sprite.Sprite):
    image = pygame.image.load('ground.png')
    image1 = pygame.image.load('all_ground.png')
    image2 = pygame.image.load('l_ground.png')
    image3 = pygame.image.load('r_ground.png')

    def __init__(self, row, i, is_all, invisible=0):
        if is_all == 0:
            self.image = border.image
        elif is_all == 1:
            self.image = border.image1
        elif is_all == 2:
            self.image = border.image2
        elif is_all == 3:
            self.image = border.image3
        self.rect = self.image.get_rect()
        self.rect.x = i * ground_width
        self.rect.y = row * ground_height
        if not invisible:
            super().__init__(all_borders, all_sprites)
        else:
            super().__init__(inv_borders, all_sprites)
        gh_border(i * ground_width + 1, row * ground_height, (i + 1) * ground_width, row * ground_height)
        gh_border(i * ground_width + 1, (row + 1) * ground_height, (i + 1) * ground_width,
                  (row + 1) * ground_height)
        gh_border(i * ground_width, row * ground_height + 1, i * ground_width, (row + 1) * ground_height)
        gh_border((i + 1) * ground_width, row * ground_height + 1, (i + 1) * ground_width,
                  (row + 1) * ground_height)


class altar(pygame.sprite.Sprite):
    image = pygame.image.load('altar.png')

    def __init__(self, x, y):
        super().__init__(sprites_of_altar, all_sprites)

        self.image = altar.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def collision_with_borders(self):
        if pygame.sprite.spritecollideany(self, sprites_of_hero):
            hero = pygame.sprite.spritecollide(self, sprites_of_hero, False)[0]
            if hero.is_hit <= 20 and (hero.rect.centerx - self.rect.centerx) * hero.direction_x <= 0:
                flag_level[0] = 1


class money(pygame.sprite.Sprite):
    image = [pygame.image.load('gold.png')]
    image.append(pygame.image.load('silver.png'))
    image.append(pygame.image.load('copper.png'))

    def __init__(self, x, y, cost):
        super().__init__(sprites_of_money, all_sprites)

        self.cost = cost
        self.image = money.image[cost]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def collision_with_borders(self):
        if pygame.sprite.spritecollideany(self, sprites_of_hero):
            hero = pygame.sprite.spritecollide(self, sprites_of_hero, False)[0]
            if hero.is_hit <= 20 and (hero.rect.centerx - self.rect.centerx + 20) * hero.direction_x <= 0:
                if self.cost == 0:
                    gold_money_on_level(levels_count[0] + 1)
                if self.cost == 1:
                    silver_money_on_level(levels_count[0] + 1)
                if self.cost == 2:
                    bronze_money_on_level(levels_count[0] + 1)
                self.kill()


def gold_money_on_level(number_of_level):
    cur.execute("""UPDATE Money_on_levels SET gold_money = (gold_money + 1) WHERE id = ? """, (number_of_level,))
    con.commit()


def silver_money_on_level(number_of_level):
    cur.execute("""UPDATE Money_on_levels SET liver_money = (liver_money + 1) WHERE id = ? """,
                (number_of_level,))
    con.commit()


def bronze_money_on_level(number_of_level):
    cur.execute("""UPDATE Money_on_levels SET bronze_money = (bronze_money + 1) WHERE id = ? """,
                (number_of_level,))
    con.commit()


def count_money(number_day):
    result = cur.execute("""SELECT * FROM Money_on_levels WHERE id = ?""", (number_day,)).fetchall()
    return result


def new_game():
    cur.execute("""UPDATE Money_on_levels SET bronze_money = 0 WHERE id > 0 AND id < 4""")
    cur.execute("""UPDATE Money_on_levels SET liver_money = 0 WHERE id > 0 AND id < 4 """)
    cur.execute("""UPDATE Money_on_levels SET gold_money = 0 WHERE id > 0 AND id < 4 """)
    con.commit()


class level:
    def __init__(self, screen, n):
        lev = levels[n].split('\n')
        print(lev)
        for row in range(len(lev)):
            for i in range(len(lev[-1])):
                if lev[row][i] == '-' and (row != 0 and lev[row - 1][i] != '-'):
                    border(row, i, 0)
                elif lev[row][i] == '-' and (i != 0 and lev[row][i - 1] != '-'):
                    border(row, i, 2)
                elif lev[row][i] == '-' and (i != len(lev[row]) - 1 and lev[row][i + 1] != '-'):
                    border(row, i, 3)
                elif lev[row][i] == '-':
                    border(row, i, 1)
                if lev[row][i] == '*':
                    enemy_slime(i * ground_width - 22, row * ground_height - 22)
                if lev[row][i] == '|':
                    enemy_border(i * ground_width, row * ground_height, i * ground_width, (row + 1) * ground_height)
                if lev[row][i] == '/':
                    enemy_border(i * ground_width + 22, row * ground_height, i * ground_width + 22,
                                 (row + 1) * ground_height)
                if lev[row][i] == '!':
                    border(row, i, 3, 1)
                if lev[row][i] == 'h':
                    enemy_HAGIVAGI(i * ground_width, row * ground_height + 4)
                if lev[row][i] == 'g':
                    money(i * ground_width + 5, row * ground_height, 0)
                if lev[row][i] == 's':
                    money(i * ground_width + 5, row * ground_height, 1)
                if lev[row][i] == 'c':
                    money(i * ground_width + 5, row * ground_height, 2)
                if lev[row][i] == 'a':
                    altar(i * ground_width - 28, row * ground_height - 48)
                if lev[row][i] == 'H':
                    hero(i * ground_width - 34, row * ground_height - 54)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


if __name__ == '__main__':
    print(open('text_for_legend', 'r', encoding='utf-8').read())
    new_game()
    size = width, height = 1544, 800
    screen = pygame.display.set_mode(size)
    rules = rules_of_game(screen)
    i_text = 0
    camera = Camera()
    clock = pygame.time.Clock()
    st_time = 0
    running = True
    if flag_level[0]:
        level(screen, levels_count[0])
        flag_level[0] = 0
    our_hero = sprites_of_hero.sprites()[0]
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                i_text += 1
                if is_end[0]:
                    levels_count[0] = 0
                    flag_level[0] = 0
                    level(screen, levels_count[0])
                    our_hero = sprites_of_hero.sprites()[0]
                    is_end[0] = 0
                if flag_level[0]:
                    levels_count[0] += 1
                    flag_level[0] = 0
                    level(screen, levels_count[0])
                    our_hero = sprites_of_hero.sprites()[0]
                if our_hero.is_hit > 60:
                    our_hero.is_hit = 0
                    our_hero.speed_x = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    our_hero.is_move_y = 1
                if event.key == pygame.K_a:
                    our_hero.direction_x = -1
                    our_hero.is_move_x += 1
                if event.key == pygame.K_d:
                    our_hero.direction_x = 1
                    our_hero.is_move_x += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    our_hero.is_move_x -= 1
                if event.key == pygame.K_d:
                    our_hero.is_move_x -= 1

        if i_text >= len(text_for_legend):
            if not is_end[0]:
                if flag_level[0]:
                    count = count_money(levels_count[0] + 1)[0]

                    text_for_win[levels_count[0]][7] = f'Золотых монет - {count[1]}'
                    text_for_win[levels_count[0]][8] = f'Серебрянных монет - {count[2]}'
                    text_for_win[levels_count[0]][9] = f'Бронзовых монет - {count[3]}'
                    sprites_of_background.draw(screen)
                    rules.draw(text_for_win[levels_count[0]])
                    for sprite in all_sprites:
                        sprite.kill()
                else:
                    sprites_of_altar.draw(screen)
                    for sprite in sprites_of_altar:
                        sprite.collision_with_borders()

                    sprites_of_money.draw(screen)
                    for sprite in sprites_of_money:
                        sprite.collision_with_borders()

                    all_enemy.draw(screen)
                    for sprite in sprites_of_slime:
                        sprite.move()
                    for sprite in sprites_of_HAGIVAGI:
                        sprite.collision_with_borders()

                    our_hero.is_hit += 1
                    our_hero.hit()
                    all_borders.draw(screen)
                    sprites_of_hero.draw(screen)
                    horizontal_borders.draw(screen)
                    vertical_borders.draw(screen)
                    our_hero.move_x(1)
                    camera.update(our_hero)
                    for sprite in all_sprites:
                        camera.apply(sprite)
            else:
                sprites_of_background.draw(screen)
                rules.draw(text_for_end)
                for sprite in all_sprites:
                    sprite.kill()

        else:
            rules.rect.x = 0
            rules.rect.y = 0
            sprites_of_background.draw(screen)
            rules.draw(text_for_legend[i_text])

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
