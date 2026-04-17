import random
import pygame

lines = 0
last_position = 3
line = 0
char_count = 0
blocks = pygame.sprite.Group()

def generate_level():
    global lines
    global last_position
    global line
    global char_count

    line = []
    block_count = 0
    char_count = 15
    line_count = 16
    position = random.randint(0, 2)



    if position == 1:
        line.append("-----")
    elif position == 2:
        line.append("----------")

    for char in range(char_count - (position * 5)):
        random_char = random.randint(0, 3)
        if random_char == 1 and block_count < 2:
            line.append("x")
            block_count += 1
        else:
            line.append("-")

    if lines == 0:
        with open("game/assets/level.txt", "a") as file:
            file.write("------xxx------\n")
        lines += 1
    else:
        if last_position != position:
            with open("game/assets/level.txt", "a") as file:
                file.write(''.join(line) + "\n")
            lines += 1


    last_position = position

    if lines < line_count:
        generate_level()
    else:
        line = lines
        lines = 0
        read_n_render()

def read_n_render():
    global line
    current_char = 1
    count = 0

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
                sprite.image = pygame.image.load("game/assets/placeholder.png")
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = current_char * sprite.rect.width
                sprite.rect.y = line * sprite.rect.height
                block = sprite
                blocks.add(block)

            current_char += 1

        for sprite in blocks:
            print(sprite)
            count += 1
    print(count)

generate_level()
