import pygame
import random
import os

max_x, max_y = 500, 800
screen = pygame.display.set_mode((max_x, max_y))

scale = 1
lines = 0
last_position = 3
line = 0
char_count = 0
blocks = pygame.sprite.Group()
block_img = "game/assets/block.png"
level_img = "game/assets/map-placeholder.png"
level_1 = pygame.image.load(level_img)
level_height = level_1.get_height()
level_width = level_1.get_width()
block_gap = 64
running = True
clock = pygame.time.Clock()
frame_rate = 60


if os.path.exists("game/assets/level.txt"):
    os.remove("game/assets/level.txt")

def generate_level():
    global lines
    global last_position
    global line
    global char_count

    block_image = pygame.image.load(block_img).get_rect()
    line = []
    block_count = 0
    char_count = level_width // (block_image.width * scale)  # level_1.rect.width // block_image.width // scale
    line_count = level_height // (block_image.height * scale)  # level_1.rect.height // block_image.height // scale
    position = random.randint(0, 3)

    if position == 1:
        line.append((char_count // 4) * "-")
    elif position == 2:
        line.append(2 * (char_count // 4) * "-")
    elif position == 3:
        line.append(3 * (char_count // 4) * "-")

    for char in range(char_count - (position * 5)):
        random_char = random.randint(0, 3)
        if random_char == 1 and block_count < 1:
            line.append("x")
            block_count += 1
        else:
            line.append("-")

    if last_position != position:
        with open("game/assets/level.txt", "a") as file:
            file.write("".join(line) + "\n")
        lines += 1

    last_position = position

    if lines < line_count:
        generate_level()
    else:
        line = lines
        lines = 0
        read_n_render()

        print(
            "char count: " + str(char_count),
            "level width: " + str(level_width),
            "block width: " + str(block_image.width),
            "block width scaled: " + str(block_image.width * scale),
        )
        print(
            "line count: " + str(line_count),
            "level height: " + str(level_height),
            "block height: " + str(block_image.height),
            "block height scaled: " + str(block_image.height * scale),
        )


def read_n_render():
    global line
    current_char = 1
    default_block_height = 32

    with open("game/assets/level.txt", "r") as file:
        line = 1

        while True:
            char = file.read(1)
            if not char:
                break
            if current_char >= char_count:
                current_char = 1
                line += 1

            if char == "x":
                sprite = pygame.sprite.Sprite()
                sprite.image = pygame.image.load(block_img)
                sprite.image = pygame.transform.scale_by(sprite.image, scale)
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = current_char * sprite.rect.width
                sprite.rect.y = (-2016 + max_y) + line * sprite.rect.height * scale + block_gap * scale + default_block_height - sprite.rect.height
                block = sprite
                blocks.add(block)

            current_char += 1

generate_level()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

    screen.fill("#242424")

    blocks.draw(screen)

    pygame.display.flip()
    dt = clock.tick(frame_rate) / 1000

pygame.quit()
