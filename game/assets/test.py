import pygame

REGENERATE_EVENT = pygame.USEREVENT + 1
blocks = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()

def regenerate_after(seconds):
    pygame.time.set_timer(REGENERATE_EVENT, seconds * 1000, loops=1)
    return sprite

while True:
    for event in pygame.event.get():
        if event.type == REGENERATE_EVENT:
            blocks.add(sprite)
            print(sprite)
            break

    regenerate_after(10)
