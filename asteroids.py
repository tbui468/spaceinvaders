import pygame
import math
import random

WIDTH = 800
HEIGHT = 600

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Bullet:
    def __init__(self, x, y, angle):
        self.rect = pygame.Rect(x, y, 10, 10)
        speed = 5
        self.xv = math.cos(math.radians(angle)) * speed
        self.yv = -math.sin(math.radians(angle)) * speed

    def update(self):
        self.rect.x += self.xv
        self.rect.y += self.yv

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

#constants
LARGE = 100
MEDIUM = 50
SMALL = 25

class Asteroid:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        angle = random.randint(0, 359)
        speed = random.randint(3, 3 + 4 - size // 25)
        self.xv = math.cos(math.radians(angle)) * speed
        self.yv = -math.sin(math.radians(angle)) * speed

    def update(self):
        self.rect.x += self.xv
        self.rect.y += self.yv
        if self.rect.y < 0 - self.rect.h:
            self.rect.y = HEIGHT
        elif self.rect.y > HEIGHT:
            self.rect.y = 0 - self.rect.h
        if self.rect.x < 0 - self.rect.w:
            self.rect.x = WIDTH
        elif self.rect.x > WIDTH:
            self.rect.x = 0 - self.rect.w

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

    def get_size(self):
        return self.rect.w


class Ship:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("ship.png"), (50, 50))
        self.default_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.angle += 2
        if keys[pygame.K_d]:
            self.angle -= 2
        if keys[pygame.K_w]:
            rad = math.radians(self.angle) 
            xv = 5 * math.cos(rad)
            yv = -5 * math.sin(rad)
            self.rect.x += xv
            self.rect.y += yv

        #teleport top-bottom
        if self.rect.y < 0 - self.rect.h:
            self.rect.y = HEIGHT
        elif self.rect.y > HEIGHT:
            self.rect.y = 0 - self.rect.h
        if self.rect.x < 0 - self.rect.w:
            self.rect.x = WIDTH
        elif self.rect.x > WIDTH:
            self.rect.x = 0 - self.rect.w

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.default_image, self.angle)
        old_centerx = self.rect.centerx
        old_centery = self.rect.centery
        self.rect = self.image.get_rect()
        self.rect.centerx = old_centerx
        self.rect.centery = old_centery
        surface.blit(self.image, self.rect)

class Text:
    def __init__(self, text):
        font = pygame.font.Font(None, 36)
        self.text = font.render(text, True, (255, 255, 255))
        size = self.text.get_size()
        self.pos = (WIDTH // 2 - size[0] // 2, HEIGHT // 2 - size[1] // 2)

    def draw(self, surface):
        surface.blit(self.text, self.pos)

win_message = Text("You Win!")
lose_message = Text("You Lose!")

ship = Ship(400, 300)
asteroids = [Asteroid(0, 0, LARGE), Asteroid(0, 0, LARGE)]
bullets = []
run = True
message = None
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and message == None:
            b = Bullet(ship.rect.centerx, ship.rect.centery, ship.angle)
            bullets.append(b)

    if message == None:
        for a in asteroids.copy():
            a.update()
            for b in bullets.copy():
                if a.rect.colliderect(b.rect):
                    bullets.remove(b)
                    asteroids.remove(a)
                    if a.get_size() == LARGE:
                        for i in range(3):
                            asteroids.append(Asteroid(a.rect.x, a.rect.y, MEDIUM)) 
                    elif a.get_size() == MEDIUM:
                        for i in range(3):
                            asteroids.append(Asteroid(a.rect.x, a.rect.y, SMALL)) 
                    break
        for b in bullets.copy():
            b.update()
            if b.rect.x < 0 or b.rect.x > 800 or b.rect.y < 0 or b.rect.y > 600:
                bullets.remove(b) 
        ship.update()
        if len(asteroids) == 0:
            message = win_message
        for a in asteroids:
            if a.rect.colliderect(ship.rect):
                message = lose_message

    window.fill((50, 50, 50))
    ship.draw(window)
    for a in asteroids:
        a.draw(window)
    for b in bullets:
        b.draw(window)
    if message != None:
        message.draw(window)

    pygame.display.update()
    clock.tick(60)
