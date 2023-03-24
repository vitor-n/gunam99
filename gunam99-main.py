import pygame
import math

from data.scripts.core import img

# ----- setup
pygame.init()
clock = pygame.time.Clock()
screen_w = 800
screen_h = 600
screen = pygame.display.set_mode((screen_w, screen_h), 0, 32)
pygame.mouse.set_visible(False)
scale = 4


class Player:
    def __init__(self, x, y):
        self.image = img("data", "player", scale)
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(x, y))

        self.vel = 5
        self.orig_vel = self.vel
        self.health_start = 3
        self.health_remaining = 3
        self.dash = False
        self.dash_cooldown = 2000
        self.last_dash = 0
        self.on_dash = False

        self.diagonal = False

    def update(self):

        time_now = pygame.time.get_ticks()

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            if time_now - self.last_dash > self.dash_cooldown:
                self.on_dash = True
                self.vel *= 5
                self.last_dash = time_now
                self.dash_cooldown = 1000
                
        if time_now - self.last_dash > 100:
            self.on_dash = False
            self.vel = self.orig_vel

        if (key[pygame.K_a] or key[pygame.K_d]) and (key[pygame.K_w] or key[pygame.K_s]):

            if not self.diagonal:
                self.vel = round(self.vel / math.sqrt(2))
                self.diagonal = True
        else:
            self.diagonal = False
            if not self.on_dash:
                self.vel = self.orig_vel

        if key[pygame.K_a]:
            self.rect.x -= self.vel
        if key[pygame.K_d]:
            self.rect.x += self.vel
        if key[pygame.K_w]:
            self.rect.y -= self.vel
        if key[pygame.K_s]:
            self.rect.y += self.vel

        pygame.draw.rect(screen, (99, 99, 99), (self.rect.x, (self.rect.y + 40), int(self.rect.width * (self.health_remaining / self.health_start)), 8))

class Weapons:
    def __init__(self, x, y):
        self.image = img("data", "gun", 5)
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = True
        self.cooldown = 500
        self.last_shot = pygame.time.get_ticks()
        self.gun_spinning = False
        self.facing_r = True
        self.recoil = False
        self.angle = 0

    def rotate(self):
        time_now = pygame.time.get_ticks()
        angle_d = math.degrees(cursor.angle_r)
        self.angle = angle_d

        if self.gun_spinning:
            self.angle += math.sin(time_now/60) * 20

        self.image = pygame.transform.rotate(self.orig_image, -self.angle)
        self.rect = self.image.get_rect(center=(math.cos(cursor.angle_r) * 24 + player.rect.centerx,
                                                math.sin(cursor.angle_r) * 32 + player.rect.centery))

        if -angle_d >= 90 or -angle_d <= -90:
            if self.facing_r:
                self.orig_image = pygame.transform.flip(
                    self.orig_image, False, True)
                player.image = pygame.transform.flip(player.image, True, False)
                self.facing_r = False

        elif not self.facing_r:
            self.orig_image = pygame.transform.flip(
                self.orig_image, False, True)
            player.image = pygame.transform.flip(player.image, True, False)
            self.facing_r = True

    def update(self):

        time_now = pygame.time.get_ticks()
        if time_now - self.last_shot > self.cooldown:
            if pygame.mouse.get_pressed()[0]:
                self.recoil = True
                bullet = Bullets(self.rect.centerx,
                                self.rect.centery, cursor.angle_r)
                bullet_group.add(bullet)
                self.last_shot = time_now

            self.gun_spinning = False
        else: 
            self.gun_spinning = True

        self.rotate()


class Cursor:
    def __init__(self, x, y):
        self.image = img("data", "cursor", scale)
        self.rect = self.image.get_rect(center=[x, y])
        self.angle_r = math.atan2(
            y - player.rect.centery, x - player.rect.centerx)

    def update(self, x, y):
        self.rect.center = [x, y]
        self.angle_r = math.atan2(
            y - player.rect.centery, x - player.rect.centerx)


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = img("data", "bullet", 3)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.dx = math.cos(angle) * 10
        self.dy = math.sin(angle) * 10
        self.x = x + self.dx * 2
        self.y = y + self.dy * 2
        self.angle = angle

    def update(self):
        angle_d = math.degrees(self.angle) + 90
        self.image = pygame.transform.rotate(self.orig_image, -angle_d)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.x += self.dx
        self.y += self.dy
        self.rect.center = int(self.x), int(self.y)

        if self.rect.centerx > screen_w or self.rect.centerx < 0 or self.rect.centery < 0 or self.rect.centery > screen_h:
            self.kill()


bullet_group = pygame.sprite.Group()
player = Player(300, 300)
weapon = Weapons(0, 0)
cursor = Cursor(0, 0)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    x, y = pygame.mouse.get_pos()

    # ----- update
    player.update()
    weapon.update()
    cursor.update(x, y)
    bullet_group.update()

    # ----- draw
    screen.fill((255, 255, 255))
    screen.blit(player.image, player.rect)
    screen.blit(weapon.image, weapon.rect)
    screen.blit(cursor.image, cursor.rect)
    bullet_group.draw(screen)

    pygame.display.update()
    clock.tick(60)
