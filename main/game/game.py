import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, moving, time, x, y, image):
        self.rect = pygame.image.load(image).get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = moving
        self.time = time


