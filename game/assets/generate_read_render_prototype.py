import random


lines = 0
last_position = 3

def generate_level():
    global lines
    global last_position

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
        lines = 0
generate_level()

def read_n_render():
    list = []
    line =

    with open("game/assets/level.txt", "r") as file:
        file.readline(lines)
