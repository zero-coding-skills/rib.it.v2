import pygame

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
framerate = 60
maxX, maxY = pygame.display.get_surface().get_size()
print(maxX, maxY)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        image = pygame.image.load("main/game/assets/placeholder.png")
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, img, breakable, moving):
        image = pygame.image.load(img)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.breakable = breakable
        self.moving = moving

class Ground(pygame.sprite.Sprite):
    def __init__(self, x , y):
        self.image = pygame.Surface((maxX, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
ground = Ground(0, maxY)
frog = Player(maxX/2, maxY)
main_group = pygame.sprite.Group(ground, frog)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    main_group.draw()

    screen.fill("black")
    pygame.display.flip()
    dt = clock.tick(framerate)

pygame.quit()


