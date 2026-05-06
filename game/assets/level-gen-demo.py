import pygame
import random
import os


#game properties
scale = 2
max_x, max_y = 8 * 32, 12 * 32
screen = pygame.display.set_mode((max_x * scale, max_y * scale))
bimg0 = "game/assets/rock0.png"
bimg1 = "game/assets/rock1.png"
block_gap = 32


#game variables
c_line = 0
last_pos = None
chars = max_x // 32
lines = max_y // (32 + block_gap)
blocks = pygame.sprite.Group()
running = True

#delete the previous level file
if os.path.exists("game/assets/level.demo"):
    os.remove("game/assets/level.demo")


def generate():
    global c_line
    global last_pos

    line = []
    pos = random.randint(0, 3)

    if pos != 0:
        line.append(pos * (chars // 4) * "-")

    for char in range(chars - pos * (chars // 4)):
        chosen = random.randint(0, 4)
        if chosen == 1:
            line.append("x" + ((chars - pos * (chars // 4) - 1) - char) * "-")
            break
        else:
            line.append("-")

    if last_pos != pos:
        with open("game/assets/level.demo", "a") as f:
            f.write("".join(line) + "\n")
        c_line += 1

    last_pos = last_pos

    if c_line < lines:
        generate()
    else:
        c_line = 0
        render()

def render():

    char = 0
    def_block_height = 32
    line = 0

    with open("game/assets/level.demo", "r") as f:
        while True:
            read_char = f.read(1)
            if not read_char:
                break
            if char + 1 > chars:
                char = 0
                line += 1
            if read_char != "\n":
                if read_char == "x":
                    obj = pygame.sprite.Sprite()
                    rimg = random.randint(0, 1)
                    obj.image = pygame.image.load(f'game/assets/block{rimg}.png')
                    obj.image = pygame.transform.scale_by(obj.image, scale)
                    obj.rect = obj.image.get_rect()
                    height_diff = def_block_height - obj.rect.height
                    obj.rect.x = char * obj.rect.width
                    obj.rect.y = line * (obj.rect.height + height_diff + block_gap) * scale
                    block = obj
                    blocks.add(block)
                    print(block.rect.x, block.rect.y)
                char += 1


generate()


def quit_game():
    global running
    running = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

    screen.fill("#242424")
    blocks.draw(screen)
    pygame.display.flip()
    dt = pygame.time.Clock().tick(60) / 1000

pygame.quit()
